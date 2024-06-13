# Real-Time 3D Animation With Facial Landmark Detection

This is a project that aims at exploring various methods to animate a character based on video/camera footage without any physical landmarks (Markers) on the subject's face. <br> <br>
Currently, this implementation uses the **Single Shot Scale-Invariant Face Detector (S3FD) [1]** for tracking 3D landmarks in an image/video. You can use DLIB or Blazeface instead of S3FD.

## Architecture
The current architecture for this project is as shown below. Instead of simply using an OpenCV classifier, I am using a DL library [Face Alignment](https://github.com/1adrianb/face-alignment) which is Open Source and widely used for 2D/3D landmark detection.


## References
[1] https://openaccess.thecvf.com/content_ICCV_2017/papers/Zhang_S3FD_Single_Shot_ICCV_2017_paper.pdf <br>
[2] 
