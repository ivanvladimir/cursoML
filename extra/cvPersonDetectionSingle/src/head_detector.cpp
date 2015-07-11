/**                                                                              
 * @brief Agent for HOG-based head detection and tracking. 
 *
 * Gibran Fuentes Pineda <gibranfp@turing.iimas.unam.mx>
 * Detector and tracker by Rogelio Romero Cordero
 * IIMAS, UNAM 
 * Created on December 2013
 * (Stand alone versio) Ivan Vladimir Meza Ruiz
 */
#include <fstream>
#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>

#include <sys/stat.h>
#include <stdio.h>
#include <errno.h>
#include <unistd.h>
#include <dirent.h>

//Command line option parser
#include <getopt.h>

//Glib, for threading (GThread)
#include <glib.h>

//Libreria GTK contiene los objetos y funciones para crear la interfaz gráfica de usuario
#include <gtk/gtk.h>

//OpenCV
#include "opencv2/objdetect/objdetect.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/gpu/gpu.hpp"

// Head tracking functions
#include "Hungarian.hpp"
#include "Track.hpp"
#include "helper.hpp"
#include "head_detector.h"

// Macros
#define MOD 0
#define REV 1 

// Camera calibration
#define PIXEL_AREA_IN_METERS 25000
#define PIXEL_X_IN_METERS 500
#define PIXEL_Y_IN_METERS 500
#define WEBCAM_FXD 1.238503573725841e+03
#define WEBCAM_FYD 1.302505846378349e+03
#define WEBCAM_CXD 7.972776269632043e+02
#define WEBCAM_CYD 6.090797111796013e+02
#define KINECT_FXD 1.0 / 5.9421434211923247e+02
#define KINECT_FYD 1.0 / 5.9104053696870778e+02
#define KINECT_CXD 3.3930780975300314e+02
#define KINECT_CYD 2.4273913761751615e+02


// General parameters
#define MAX_WAITING_TIME 1000000
#define MAX_STRING_LENGTH 1000
#define SLEEP_TIME 10000
#define SMALL_SLEEP_TIME 1000

// detection and tracking parameters
#define MAX_TRACKING_TRIES 25
#define XYZ_ERROR_THRESHOLD 0.4

// Webcam parameters
#define DEFAULT_WEBCAM_DEVICE_NUMBER 0
#define WEBCAM_WIDTH 640
#define WEBCAM_HEIGHT 480

// error status
#define CAMERA_ERROR -101

// success status
#define HEAD_TRACKED 1

// fail status
#define HEAD_NOT_TRACKED 0

//Global variables
// webcam
cv::VideoCapture device_capture;

// kinect
static int kinect_flag;

// head detection
cv::gpu::HOGDescriptor gpu_hog;
double hitThreshold = 1.4;
int groupThreshold = 4;
double scale = 1.04; 
static GMutex *capture_mutex;


/**
 * @brief Prints help in screen.
 */
void usage(void)
{
     std::cout << "usage: head_detector [options]\n"
	       << "General Options:\n"
	       << "   -h, --help\t\t\t\tPrints this help\n"
	       << "   -k, --kinect\t\t\t\tUse Kinect sensor"
	       << "   -w, --webcam\t\t\t\tWebcam device number (default 0)\n"
	       << "Head Detector Options:\n"
	       << "   -a, --scale\t\t\t\tCoefficient of the detection window increase (default 1.04)\n"
	       << "   -g, --group\t\t\t\tCoefficient to regulate the similarity threshold (default 3)\n"
	       << "   -i, --window_sigma\t\t\t\tGaussian smoothing window parameter (default -1)\n" 
	       << "   -l, --levels\t\t\t\tMaximum number of detection window increases (default 48)\n"
	       << "   -n, --norm\t\t\t\tL2-Hys normalization method shrinkage (default 0.2)\n"
	       << "   -t, --threshold\t\t\t\tThreshold for the distance between features and\n"
	       << "                 \t\t\t\tSVM classifying plane (default 1.1)\n"
	       << std::endl;
}

/*
 * Comparison function for sorting objects by nearness.
 */
bool cmpNear(const PositionXYZ& a, const PositionXYZ& b)
{
     double a_dist = sqrt(a.at(0) * a.at(0) + a.at(1) * a.at(1) + a.at(2) * a.at(2));
     double b_dist = sqrt(b.at(0) * b.at(0) + b.at(1) * b.at(1) + b.at(2) * b.at(2));
     
     return a_dist < b_dist;
}

/**
 * @brief Roughly estimates X, Y, Z world values in meters from pixel position and detection size
 */
PositionXYZ compute_position_webcam(cv::Mat& frame, cv::Rect& detection) 
{
     PositionXYZ position;

     float origin_x = frame.cols / 2;
     float origin_y = frame.rows / 2;

     float x = (detection.x + detection.width / 2) - origin_x;
     float y = (detection.y + detection.height / 2) - origin_y;
     float z = (float) PIXEL_AREA_IN_METERS / (detection.width * detection.height);

     position.push_back((float) (x * z) / PIXEL_X_IN_METERS);// - WEBCAM_CXD) * z * WEBCAM_FXD);
     position.push_back((float) (y * z) / PIXEL_Y_IN_METERS);// - WEBCAM_CYD) * z * WEBCAM_FYD);
     position.push_back(z);

     return position;
}

/**
 * @brief Estimates world X, Y, Z coordinates from depth values and pixel positions
 */
PositionXYZ compute_position_kinect(cv::Mat depth_map, cv::Rect detection) 
{
     PositionXYZ position;
     
     cv::Rect head((int) (detection.x + detection.width / 3), 
		   (int) (detection.y + detection.height / 3), 
		   (int) (detection.width / 3), 
		   (int) (detection.height / 3));
     cv::Mat head_depth = depth_map(head);
     
     unsigned int sum_depth = 0;
     unsigned int nonzero = 0;
     for (int i = 0; i < head_depth.cols; ++i){
	  unsigned char *ptr = (unsigned char *)(head_depth.data + i * head_depth.step);
	  for (int j = 0; j < head_depth.rows; ++j){
	       unsigned short int depth_value = head_depth.at<unsigned short int>(i, j);
	       if (depth_value != 0){
		    sum_depth +=  depth_value;
		    nonzero++;
	       }
	  }
     }
     
     int mean_depth;
     if (nonzero != 0)
	  mean_depth = (int) sum_depth / nonzero;
     
     float meters = (float) mean_depth / 1000;
     float x = ((detection.x + detection.width / 2) - KINECT_CXD) * meters * KINECT_FXD;
     float y = ((detection.y + detection.height / 2) - KINECT_CYD) * meters * KINECT_FYD;
     float z = meters;

     position.push_back(x);
     position.push_back(y);
     position.push_back(z);
     
     return position;
}

/**
 * @brief Grabs frames from the kinect
 */
void captureKinect(void)
{
     cv::Mat frame;
     cv::Mat depth_map;
     for (;;){
	  if (g_mutex_trylock(capture_mutex) == TRUE){
	       // grabbing frame
	       if (!device_capture.grab())
		    std::cerr << "head_detector: Capture from Kinect didn't work" << std::endl;
	       device_capture.retrieve( frame, CV_CAP_OPENNI_BGR_IMAGE );
	       device_capture.retrieve( depth_map, CV_CAP_OPENNI_DEPTH_MAP );
	       g_mutex_unlock(capture_mutex);
	       gdk_threads_enter ();
	       cv::imshow("head_detector: Stand Alone", frame);
	       gdk_threads_leave ();
	  }
	  usleep(SLEEP_TIME);
     }
}

/**
 * @brief Grabs frames from the webcam
 */
void captureWebcam(void)
{
     cv::Mat frame;
     for (;;){
	  if (g_mutex_trylock(capture_mutex) == TRUE){
	       // grabbing frame
	       if (!device_capture.grab())
		    std::cerr << "head_detector: Capture from CAM didn't work" << std::endl;

	       device_capture.retrieve(frame, 0);  
	       g_mutex_unlock(capture_mutex);
	       gdk_threads_enter ();
	       cv::imshow("head_detector: Stand alone", frame);
	       gdk_threads_leave ();
	  }
	  usleep(SLEEP_TIME);
     }
}

/**
 * @brief Tracks the head of a person
 */
int trackHeadWebcam(Positions& positions)
{    
     // wait when webcam is busy
     int waiting_time = 0;
     while (g_mutex_trylock(capture_mutex) == FALSE){
     	  if (waiting_time > MAX_WAITING_TIME){
	       std::cerr << "head_detector: Camera cannot be accessed" << std::endl;
     	       return CAMERA_ERROR;
	  }
     	  waiting_time++;
     	  usleep(SMALL_SLEEP_TIME);
     }

     std::vector<Track> tracks;
     int head_tracked = HEAD_NOT_TRACKED;
     int tracked_head_number = 0;
     int tries = 0;
     while(!head_tracked && tries < MAX_TRACKING_TRIES)
     {
	  cv::Mat frame, gs, eqgs;
	  std::vector<cv::Rect> detections;

	  // grabbing frame
	  if (!device_capture.grab()){
	       std::cerr << "head_detector: Capture from CAM " <<  " didn't work" << std::endl;
	       return CAMERA_ERROR;
	  }
	  device_capture.retrieve(frame, 0);  

	  // upload images to GPU
	  cv::gpu::GpuMat gpu_img, gpu_gray;
	  gpu_img.upload(frame);

	  // convert image to grayscale
	  cv::gpu::cvtColor(gpu_img, gpu_gray, CV_BGR2GRAY);

	  // detect heads
	  gpu_hog.detectMultiScale(gpu_gray, detections, hitThreshold, cv::Size(8, 8), cv::Size(0, 0), 
				   scale, groupThreshold);
	  
	  // draw detections
	  for (std::vector<cv::Rect>::iterator it = detections.begin(); it != detections.end(); ++it)
	       cv::rectangle(frame, *it, cv::Scalar(255,255,0));
	  
	  // delete duplicated detections
	  validateRects(detections);
	  
	  // assign detections to tracks
	  checkRects(frame, detections, tracks, tracked_head_number);
	  
	  // delete old tracks
	  deleteTracksUnmod(tracks);
	       
	  // marl all tracks as unmodified
	  modAllTracks(MOD, 0, tracks);
	  
	  // checks if there are valid tracks
	  for (std::vector<Track>::iterator it = tracks.begin(); it != tracks.end(); it++)
	       if ((*it).valueInRange((*it).coef, MIN_COEF_CONST, MAX_COEF_CONST)) {
		    positions.push_back(compute_position_webcam(frame, (*it).estimated_rect));
	  	    cv::rectangle(frame, (*it).estimated_rect, cv::Scalar(0,0,255));
	       }
	  
	  std::sort(positions.begin(), positions.end(), cmpNear); // sort by nearness
	  if (!positions.empty()){
	       Positions::iterator it = positions.begin();
	       std::cout << "head_detector: " << positions.size() << " --> [";
	       for (int i = 0; i < positions.size(); ++i){
		    std::cout << "[" << it->at(0) << ", " << it->at(1) << ", " << it->at(2) << "]";
		    if (i + 1 < positions.size())
			 std::cout << ", ";
		    ++it;
	       }
	       std::cout << "] " << std::endl;
	       head_tracked = HEAD_TRACKED;
	  }
	  
	  gdk_threads_enter ();
	  cv::imshow("head_detector: Stand alone", frame);
	  gdk_threads_leave ();

	  tries++;
     }
     g_mutex_unlock(capture_mutex);

     return head_tracked;
}

/**
 * @brief Tracks the head of a person
 */
int trackHeadKinect(Positions& positions)
{    
     // wait when webcam is busy
     int waiting_time = 0;
     while (g_mutex_trylock(capture_mutex) == FALSE){
     	  if (waiting_time > MAX_WAITING_TIME){
	       std::cerr << "head_detector: Camera cannot be accessed" << std::endl;
     	       return CAMERA_ERROR;
	  }
     	  waiting_time++;
     	  usleep(SMALL_SLEEP_TIME);
     }

     std::vector<Track> tracks;
     int head_tracked = HEAD_NOT_TRACKED;
     int tracked_head_number = 0;
     int tries = 0;
     while(!head_tracked && tries < MAX_TRACKING_TRIES)
     {
	  cv::Mat frame, gs, eqgs;
	  std::vector<cv::Rect> detections;

	  // grabbing frame
	  if (!device_capture.grab()){
	       std::cerr << "head_detector: Capture from CAM " <<  " didn't work" << std::endl;
	       return CAMERA_ERROR;
	  }

	  cv::Mat depth_map;
	  device_capture.retrieve( frame, CV_CAP_OPENNI_BGR_IMAGE );
	  device_capture.retrieve( depth_map, CV_CAP_OPENNI_DEPTH_MAP );

	  // upload images to GPU
	  cv::gpu::GpuMat gpu_img, gpu_gray;
	  gpu_img.upload(frame);

	  // convert image to grayscale
	  cv::gpu::cvtColor(gpu_img, gpu_gray, CV_BGR2GRAY);

	  // detect heads
	  gpu_hog.detectMultiScale(gpu_gray, detections, hitThreshold, cv::Size(8, 8), cv::Size(0, 0), 
				   scale, groupThreshold);
	  
	  // draw detections
	  for (std::vector<cv::Rect>::iterator it = detections.begin(); it != detections.end(); ++it)
	       cv::rectangle(frame, *it, cv::Scalar(255,255,0));
	  
	  // delete duplicated detections
	  validateRects(detections);
	  
	  // assign detections to tracks
	  checkRects(frame, detections, tracks, tracked_head_number);
	  
	  // delete old tracks
	  deleteTracksUnmod(tracks);
	       
	  // marl all tracks as unmodified
	  modAllTracks(MOD, 0, tracks);

	  // checks if there are valid tracks
	  for (std::vector<Track>::iterator it = tracks.begin(); it != tracks.end(); it++)
	       if ((*it).valueInRange((*it).coef, MIN_COEF_CONST, MAX_COEF_CONST)) {
		    PositionXYZ xyz_depth = compute_position_kinect(depth_map, (*it).estimated_rect);
		    //PositionXYZ xyz_rgb = compute_position_webcam(frame, (*it).estimated_rect);
		    //if (std::abs(xyz_depth.at(2) - xyz_rgb.at(2)) < XYZ_ERROR_THRESHOLD)
		    //{
		    positions.push_back(xyz_depth);
		    cv::rectangle(frame, (*it).estimated_rect, cv::Scalar(0,0,255));
		    //}
	       }
	  
	  std::sort(positions.begin(), positions.end(), cmpNear); // sort by nearness
	  if (!positions.empty()){
	       Positions::iterator it = positions.begin();
	       std::cout << "head_detector: " << positions.size() << " --> [";
	       for (int i = 0; i < positions.size(); ++i){
		    std::cout << "[" << it->at(0) << ", " << it->at(1) << ", " << it->at(2) << "]";
		    if (i + 1 < positions.size())
			 std::cout << ", ";
		    ++it;
	       }
	       std::cout << "] " << std::endl;
	       head_tracked = HEAD_TRACKED;
	  }

	  gdk_threads_enter ();
	  cv::imshow("head_detector: Stand alone", frame);
	  gdk_threads_leave ();

	  tries++;
     }
     g_mutex_unlock(capture_mutex);

     return head_tracked;
}


/**                                                                              
 * @brief Runs head tracker and recognizer as a standalone program using the webcam
 */
void trackerWebcamStandalone(int device_number)
{
 
     // open webcam
     device_capture.open(device_number);     
     if(!device_capture.isOpened())
     {
     	  std::cerr << "head_detector: Could not open webcam /dev/video" << device_number << std::endl;     
     	  exit(EXIT_FAILURE);
     }

     // set webcam size
     device_capture.set(CV_CAP_PROP_FRAME_WIDTH, WEBCAM_WIDTH);
     device_capture.set(CV_CAP_PROP_FRAME_HEIGHT, WEBCAM_HEIGHT);

     // track and recognize heads
     int tracked_head_number = 0;
     std::vector<Track> tracks;
     Positions positions;
     cv::namedWindow("head_detector: Standalone tracker", 1);
     while(true)
     {
	  std::vector<cv::Rect> detections;
	  cv::Mat frame, gs, eqgs;
	
	  // grabbing frame
	  if (!device_capture.grab()){
	       std::cerr << "head_detector: Capture from Webcam didn't work" << std::endl;
	       exit(EXIT_FAILURE);
	  }

	  device_capture.retrieve(frame, 0);  

	  // upload images to GPU
	  cv::gpu::GpuMat gpu_img, gpu_gray;
	  gpu_img.upload(frame);

	  // convert image to grayscale
	  cv::gpu::cvtColor(gpu_img, gpu_gray, CV_BGR2GRAY);

	  // detect heads
	  gpu_hog.detectMultiScale(gpu_gray, detections, hitThreshold, cv::Size(8, 8), cv::Size(0, 0), 
				   scale, groupThreshold);

	  
	  // draw detections
	  for (std::vector<cv::Rect>::iterator it = detections.begin(); it != detections.end(); ++it)
	       cv::rectangle(frame, *it, cv::Scalar(255,255,0));

	  // delete duplicated detections
	  validateRects(detections);
	  
	  // assign detections to tracks
	  checkRects(frame, detections, tracks, tracked_head_number);
	  
	  // delete old tracks
	  deleteTracksUnmod(tracks);
	  
	  // marl all tracks as unmodified
	  modAllTracks(MOD, 0, tracks);

	  // checks if there are valid tracks
	  for (std::vector<Track>::iterator it = tracks.begin(); it != tracks.end(); it++)
	       if ((*it).valueInRange((*it).coef, MIN_COEF_CONST, MAX_COEF_CONST)) {
		    positions.push_back(compute_position_webcam(frame, (*it).estimated_rect));
	  	    cv::rectangle(frame, (*it).estimated_rect, cv::Scalar(0,0,255));
	       }
	  
	  std::sort(positions.begin(), positions.end(), cmpNear); // sort by nearness
	  if (!positions.empty()){
	       Positions::iterator it = positions.begin();
	       std::cout << "head_detector: " << positions.size() << " --> [";
	       for (int i = 0; i < positions.size(); ++i){
		    std::cout << "[" << it->at(0) << ", " << it->at(1) << ", " << it->at(2) << "]";
		    if (i + 1 < positions.size())
			 std::cout << ", ";
		    ++it;
	       }
	       std::cout << "] " << std::endl;
	  }
	  positions.clear();
	  cv::imshow("head_detector: Standalone tracker", frame);
	  cv::waitKey(1);
     }
}

/**                                                                              
 * @brief Runs head tracker and recognizer as a standalone program using the Kinect sensor
 */
void trackerKinectStandalone(void)
{
     device_capture.open(CV_CAP_OPENNI);     
     if(!device_capture.isOpened())
     {
	  std::cerr << "head_detector: Could not open the Kinect sensor" << std::endl;     
     	  exit(EXIT_FAILURE);
     }

     // track and recognize heads
     int tracked_head_number = 0;
     std::vector<Track> tracks;
     Positions positions;
     cv::namedWindow("head_detector: Standalone tracker", 1);
     while(true)
     {
	  std::vector<cv::Rect> detections;
	  cv::Mat frame, gs, eqgs;
	
	  // grabbing frame
	  if (!device_capture.grab()){
	       std::cerr << "head_detector: Capture from Webcam didn't work" << std::endl;
	       exit(EXIT_FAILURE);
	  }

	  cv::Mat depth_map;
	  device_capture.retrieve( frame, CV_CAP_OPENNI_BGR_IMAGE );
	  device_capture.retrieve( depth_map, CV_CAP_OPENNI_DEPTH_MAP );

	  // upload images to GPU
	  cv::gpu::GpuMat gpu_img, gpu_gray;
	  gpu_img.upload(frame);

	  // convert image to grayscale
	  cv::gpu::cvtColor(gpu_img, gpu_gray, CV_BGR2GRAY);

	  // detect heads
	  gpu_hog.detectMultiScale(gpu_gray, detections, hitThreshold, cv::Size(8, 8), cv::Size(0, 0), 
				   scale, groupThreshold);

	  
	  // draw detections
	  for (std::vector<cv::Rect>::iterator it = detections.begin(); it != detections.end(); ++it)
	       cv::rectangle(frame, *it, cv::Scalar(255,255,0));

	  // delete duplicated detections
	  validateRects(detections);
	  
	  // assign detections to tracks
	  checkRects(frame, detections, tracks, tracked_head_number);
	  
	  // delete old tracks
	  deleteTracksUnmod(tracks);
	  
	  // marl all tracks as unmodified
	  modAllTracks(MOD, 0, tracks);

	  // checks if there are valid tracks

	  for (std::vector<Track>::iterator it = tracks.begin(); it != tracks.end(); it++)
	       if ((*it).valueInRange((*it).coef, MIN_COEF_CONST, MAX_COEF_CONST)) {
		    PositionXYZ xyz_depth = compute_position_kinect(depth_map, (*it).estimated_rect);
		    PositionXYZ xyz_rgb = compute_position_webcam(frame, (*it).estimated_rect);
		    if (std::abs(xyz_depth.at(2) - xyz_rgb.at(2)) < XYZ_ERROR_THRESHOLD)
		    {
			 positions.push_back(xyz_depth);
			 cv::rectangle(frame, (*it).estimated_rect, cv::Scalar(0,0,255));
		    }
	       }

	  std::sort(positions.begin(), positions.end(), cmpNear); // sort by nearness
	  if (!positions.empty()){
	       Positions::iterator it = positions.begin();
	       std::cout << "head_detector: " << positions.size() << " --> [";
	       for (int i = 0; i < positions.size(); ++i){
		    std::cout << "[" << it->at(0) << ", " << it->at(1) << ", " << it->at(2) << "]";
		    if (i + 1 < positions.size())
			 std::cout << ", ";
		    ++it;
	       }
	       std::cout << "] " << std::endl;
	  }
	  positions.clear();
	  cv::imshow("head_detector: Standalone tracker", frame);
	  cv::waitKey(1);
     }
}

/**
 *==============================
 * @brief Main function
 *==============================
 */
int main(int argc, char **argv)
{
     //Variables for getopt
     int op;
     static int standalone_flag=1;
     int option_index = 0;
     char *output;
     
     static struct option long_options[] =
     	  {
	       {"block_size", required_argument, 0, 'a'},
	       {"bins", required_argument, 0, 'b'},
	       {"cell_size", required_argument, 0, 'c'},
	       {"window_size", required_argument, 0, 'd'},
	       {"block_stride", required_argument, 0, 'e'},
	       {"window_stride", required_argument, 0, 'f'},
	       {"group", required_argument, 0, 'g'},
	       {"help", no_argument, 0, 'h'},
	       {"sigma", required_argument, 0, 'i'},
	       {"hys", required_argument, 0, 'j'},
	       {"kinect", no_argument, &kinect_flag, 1},
	       {"levels", required_argument, 0, 'l'},
	       {"gamma", required_argument, 0, 'm'},
	       {"padding", required_argument, 0, 'p'},
	       {"threshold", required_argument, 0, 't'},
	       {"webcam", required_argument, 0, 'w'},
     	       {0, 0, 0, 0}
     	  };

     std::vector<float> detector(head_48x48, head_48x48 + sizeof(head_48x48) / sizeof(head_48x48[0]));
     int device_number = DEFAULT_WEBCAM_DEVICE_NUMBER;
     cv::Size winSize(48,48);
     cv::Size blockSize(16, 16);
     cv::Size blockStride(8, 8);
     cv::Size cellSize(8, 8);
     int nbins = 9;
     bool gammaCorrection = false;
     int nlevels = cv::gpu::HOGDescriptor::DEFAULT_NLEVELS;
     double winSigma = cv::gpu::HOGDescriptor::DEFAULT_WIN_SIGMA;
     double L2HysThreshold = 0.2;

     //Command-line option parser
     while((op = getopt_long( argc, argv, "a:b:c:d:e:f:g:hi:j:kl:m:p:st:w:", long_options, 
			      &option_index)) != -1){
     	  int this_option_optind = optind ? optind : 1;
     	  switch (op)
     	  {
	  case 0:
	  case 'a':
	       scale = std::atof(optarg);
	       std::cout << "head_detector: Scale set to " << scale << std::endl;
     	       break;
	  case 'g':
     	       groupThreshold = std::atoi(optarg);
	       std::cout << "head_detector: Group threshold set to " << groupThreshold << std::endl;
     	       break;
	  case 'h':
     	       usage();
     	       exit(EXIT_SUCCESS);
	  case 'i':
     	       winSigma = std::atof(optarg);
	       std::cout << "head_detector: Window sigma set to " << winSigma << std::endl;
     	       break;
	  case 'j':
     	       L2HysThreshold = std::atof(optarg);
	       std::cout << "head_detector: L2 threshold set to " << L2HysThreshold << std::endl;
     	       break;
	  case 'k':
	       kinect_flag = 1;
	       break;
	  case 'l':
	       nlevels = std::atoi(optarg);
	       std::cout << "head_detector: Number of levels set to " << nlevels << std::endl;
     	       break;
	  case 'm':
	       gammaCorrection = true;
	       break;
	  case 't':
     	       hitThreshold = std::atof(optarg);
	       std::cout << "head_detector: Hit threshold set to " << hitThreshold << std::endl;
     	       break;
	  case 'w':
	       device_number = std::atoi(optarg);
	       std::cout << "head_detector: Webcam device number set to " << device_number << std::endl;
     	       break;
	  case '?':
	       std::cerr << "Error: Unknown options.\n"
			 << "Try `head_detector --help' for more information.\n";
     	       exit(EXIT_FAILURE);

     	  default:
     	       abort ();
     	  }
     }
     
     gpu_hog = cv::gpu::HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins, winSigma, 
				      L2HysThreshold, gammaCorrection, nlevels);
     gpu_hog.setSVMDetector(detector);

     if (standalone_flag){
	  std::cout << "head_detector: Running standalone";
	  if (kinect_flag){
	       std::cout << " with the Kinect sensor" << std::endl;
	       trackerKinectStandalone();
	  }
	  else{
	       std::cout << " with webcam /dev/video" << device_number << std::endl;
	       trackerWebcamStandalone(device_number);
	  }
     }
     return 1;
}
