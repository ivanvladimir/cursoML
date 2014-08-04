#ifndef HELPER_HPP
#define HELPER_HPP

#include "opencv2/objdetect/objdetect.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/video/tracking.hpp>

bool contains(cv::Rect A, cv::Rect B);
void validateRects( std::vector<cv::Rect>& faces );
bool find( const std::vector<int> A, int value );
float trackRectOverlap(Track A, cv::Rect B);
void newTracks( std::vector<cv::Rect>& faces, std::vector<Track>& tracks);
void checkRects(cv::Mat frame, std::vector<cv::Rect>& faces, std::vector<Track>& tracks, int& n);
void deleteTracksUnmod(std::vector<Track>& tracks);
void modAllTracks(int attribute, int value, std::vector<Track>& tracks);
#endif
