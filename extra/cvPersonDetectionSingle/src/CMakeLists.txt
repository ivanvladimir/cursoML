find_package(OpenMP)
if (OPENMP_FOUND)
    set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
endif()
set ( CMAKE_MODULE_PATH ../../../../etc/cmake )
set ( HEAD_DETECTOR_SRCS head_detector.cpp helper.cpp)
set ( PERSON_RECOGNITION_INCLUDE_DIRS ../include )
set ( FLYCAPTURE_INCLUDE_PATH /usr/include/flycapture )
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ../../bin)
include_directories( ${FLYCAPTURE_INCLUDE_PATH} )
include_directories( ${PERSON_RECOGNITION_INCLUDE_DIRS} )
find_package( GTK2 REQUIRED )
include_directories( ${GTK2_INCLUDE_DIRS} )
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable( head_detector ${HEAD_DETECTOR_SRCS} )
target_link_libraries( head_detector  ${GTK2_LIBRARIES} ${OpenCV_LIBS} gthread-2.0) 
