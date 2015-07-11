
#include "opencv2/objdetect/objdetect.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/video/tracking.hpp>

#include <iostream>
#include <stdio.h>
#include <time.h>
#include <string>

#define MAX_COEF_CONST 30
#define MIN_COEF_CONST 9

#define S_OBJ "P #"
 
class Track
{
public:
     cv::KalmanFilter kalman_filter;
     
     cv::Mat prediction;
     cv::Mat processNoise;
     cv::Mat estimated;

     cv::Mat_<float> state;
     cv::Mat_<float> measurement;

     cv::Point predicted_position;
     cv::Rect predicted_rect;
     cv::Rect estimated_rect;

     int coef, mod, rev, objNum, r, g, b;
     std::string name;
     
     Track()
	  {
	       mod = rev = objNum = coef = 0;
	       r = rand() % 255;
	       g = rand() % 255;
	       b = rand() % 255;
	       
	       // initialize dynamic model parameters
	       kalman_filter = cv::KalmanFilter(6, 4, 0);
	       state = cv::Mat_<float>(6, 1); /* (x, y, w, h, Vx, Vy) */
	       measurement = cv::Mat_<float>(4, 1);
	       processNoise = cv::Mat(6, 1, CV_32F);	 
	       setParameters();
	       
	  }
     
     cv::Rect getPrediction()
	  {
	       return predicted_rect;
	  }
     
     cv::Rect getEstimation()
	  {
	       return estimated_rect;
	  }
     
     void setStatePost(cv::Rect object)
	  {
	       state.at<float>(0) = object.x + object.width / 2;
	       state.at<float>(1) = object.y - object.height / 2;
	       state.at<float>(2) = object.width;
	       state.at<float>(3) = object.height;
	       state.at<float>(4) = 0;
	       state.at<float>(5) = 0;
	       state.copyTo(kalman_filter.statePost);
	  }
		
     void setParameters()
	  {  
	       // set dynamic model parameters
	       measurement.setTo(cv::Scalar(0));
	       kalman_filter.transitionMatrix = *(cv::Mat_<float>(6, 6) <<  
						  1, 0, 0, 0, 0.1,   0,         //x pixel position
						  0, 1, 0, 0,   0, 0.1,	        //y pixel position
						  0, 0, 1, 0,   0,   0,		//w rectangle width
						  0, 0, 0, 1,   0,   0,		//h rectangle height
						  0, 0, 0, 0,   1,   0,		//vx velocity in x
						  0, 0, 0, 0,   0,   1);	//vy velocity in y
	       
	       setIdentity(kalman_filter.measurementMatrix);
	       setIdentity(kalman_filter.processNoiseCov, cv::Scalar::all(1e-3)); 
	       setIdentity(kalman_filter.measurementNoiseCov, cv::Scalar::all(1e-3)); 
	       setIdentity(kalman_filter.errorCovPost, cv::Scalar::all(.1));
	  }
		
     void refresh(cv::Rect object)
	  {
	       // add new measurements
	       measurement(0) = object.x + object.width/2;
	       measurement(1) = object.y - object.height/2;
	       measurement(2) = object.width;
	       measurement(3) = object.height;

	       // Kalman filter's prediction phase
	       prediction = kalman_filter.predict();
	       predicted_rect = cv::Rect(prediction.at<float>(0), prediction.at<float>(1), 
				    prediction.at<float>(2), prediction.at<float>(3));

	       // Kalman filter's correction phase
	       estimated = kalman_filter.correct(measurement);
	       estimated_rect = cv::Rect((int)estimated.at<float>(0) - (int)(estimated.at<float>(2)/2),
					  (int)estimated.at<float>(1) + (int)(estimated.at<float>(3)/2),
					  (int)estimated.at<float>(2), (int)estimated.at<float>(3));

	       mod = 1;
	       coef++;
	       if(valueInRange(coef, MIN_COEF_CONST ,MAX_COEF_CONST))
	       {
		    rev = 1;
		    if(coef == MAX_COEF_CONST)
			 coef--;
	       }
	  }
		
     void doPrimPred(cv::Rect object)
	  {	
	       setStatePost(object);

	       // prediction phase
	       prediction = kalman_filter.predict();
	       // get prior (predicted) rectangle 
	       predicted_rect = cv::Rect(prediction.at<float>(0), prediction.at<float>(1), 
				       prediction.at<float>(2), prediction.at<float>(3));

	       // add new measurements to the dynamic model
	       measurement(0) = object.x + object.width / 2;
	       measurement(1) = object.y - object.height / 2;
	       measurement(2) = object.width;
	       measurement(3) = object.height;

	       // correction phase
	       estimated = kalman_filter.correct(measurement);
	       estimated_rect = cv::Rect((int)estimated.at<float>(0) - (int)(estimated.at<float>(2)/2), 
					 (int)estimated.at<float>(1) + (int)(estimated.at<float>(3)/2),	
					 (int)estimated.at<float>(2), (int)estimated.at<float>(3));
	       mod = 1;
	  }

     void setObjNum(int ObNu)
	  {
	       objNum = ObNu;
	       std::stringstream sstm;
	       sstm << S_OBJ << ObNu;
	       name = sstm.str();
	  }
     
     bool valueInRange(int value, int min, int max)
	  { 
	       return (value >= min) && (value <= max); 
	  }
		
		
     bool rectOverlap(cv::Rect A, cv::Rect B)
	  {
	       bool xOverlap = valueInRange(A.x, B.x, B.x + B.width) ||
		    valueInRange(B.x, A.x, A.x + A.width);

	       bool yOverlap = valueInRange(A.y, B.y, B.y + B.height) ||
		    valueInRange(B.y, A.y, A.y + B.height);

	       return xOverlap && yOverlap;
	  }
		
     bool isNotNull(cv::Rect obj)
	  {
	       return !(obj.width == 0 || obj.height == 0);
	  }		
};

