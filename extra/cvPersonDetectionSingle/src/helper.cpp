#include "Track.hpp"
#include "Hungarian.hpp"
#include "helper.hpp"


bool contains(cv::Rect A, cv::Rect B)
{
     return B.x > A.x && 
	  B.y > A.y && 
	  (B.x + B.width) <= (A.x + A.width) &&
	  (B.y + B.height) <= (A.y + A.height);
}

void validateRects(std::vector<cv::Rect>& faces)
{
     for(int i = 0; i < faces.size(); i++)
     {
	  for (int j = i + 1 ; j < faces.size(); j++)
	       if(contains(faces[i], faces[j]))
	       {
		    faces.erase(faces.begin() +  i );
		    i--;
	       }
	       else if(contains(faces[j], faces[i]))
	       {
		    faces.erase(faces.begin() +  j );
		    j--;
	       }
     }
}

bool find(const std::vector<int> A, int value)
{
     for(int i = 0; i < A.size(); i++)
	  if(A[i] == value)
	       return true;

     return false;
}

float trackRectOverlap(Track A, cv::Rect B)
{
     cv::Rect intersection = A.estimated_rect & B;
     
     return -1 * (intersection.width * intersection.height);
}


void newTracks(std::vector<cv::Rect>& faces, std::vector<Track>& tracks)
{
     if(!tracks.size())
	  for(int i = 0; i < faces.size(); i++)
	  {
	       Track a = Track();
	       a.doPrimPred(faces[i]);
	       tracks.push_back(a);
	  }
}

void checkRects(cv::Mat frame, std::vector<cv::Rect>& faces, std::vector<Track>& tracks, int& n)
{
     if(faces.size() && tracks.size())
     {	
	  Hungarian <Track, cv::Rect> hao (tracks, faces, &trackRectOverlap);
	  std::vector<int> assigned_rects = hao.hungarianAlgorithm();
	  for(int i = 0; i < assigned_rects.size(); i++)
	  {
	       if(assigned_rects[i] >= 0)
	       {
		    if((faces[assigned_rects[i]] & tracks[i].getPrediction()).area() > 0)
			 tracks[i].refresh(faces[assigned_rects[i]]);

		    if(tracks[i].valueInRange(tracks[i].coef, MIN_COEF_CONST, MAX_COEF_CONST) && 
			!tracks[i].objNum)
		    {
			 n++;
			 tracks[i].setObjNum(n);
		    }
	       }
	  }
	  for(int i = 0; i < faces.size(); i++)
	       if(!find(assigned_rects, i))
	       {
		    Track a = Track();
		    a.doPrimPred(faces[i]);
		    tracks.push_back(a);
	       }
     }
     else
	  newTracks(faces, tracks);
}

void deleteTracksUnmod(std::vector<Track>& tracks)
{
     for(int i = 0; i < tracks.size(); i++)
     {
	  if(!tracks[i].mod)
	  {
	       tracks[i].coef--;
	       if(tracks[i].coef < MIN_COEF_CONST)
	       {
		    tracks.erase(tracks.begin() + i);
	       }
	  }
     }
}

void modAllTracks(int attribute, int value, std::vector<Track>& tracks)
{
     switch(attribute)
     {
     case 0:
	  for(int i = 0; i < tracks.size(); i++)
	  {
	       tracks[i].mod = value;
	  }
	  break;
     case 1:
	  for(int i = 0; i < tracks.size(); i++)
	  {
	       tracks[i].rev = value;
	  }
	  break;
     }
}
