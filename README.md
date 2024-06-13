# Real-Time 3D Animation With Facial Landmark Detection

This is a project that aims at exploring various methods to animate a character based on video/camera footage without any physical landmarks (Markers) on the subject's face. <br> <br>
Currently, this implementation uses the **Single Shot Scale-Invariant Face Detector (S3FD) [1]** for tracking 3D landmarks in an image/video. You can use DLIB or Blazeface instead of S3FD.

## Architecture
The current architecture for this project is as shown below. Instead of simply using an OpenCV classifier, I am using a DL library [Face Alignment](https://github.com/1adrianb/face-alignment) which is Open Source and widely used for 2D/3D landmark detection.

Using S3FD, we get 68 landmarks, out of which I've used all. Though it may be a good option to use every 3rd or 2nd marker to avoid jittering (Which is apparent in my implementation). A detailed list of the bones I'm using can be found below, with their relevant names, also indicating location.

<div align="center">

  | Label          | Index |
|----------------|-------|
| chin_8         | 8     |
| l_jaw_0        | 16    |
| l_jaw_1        | 15    |
| l_jaw_2        | 14    |
| l_jaw_3        | 13    |
| l_jaw_4        | 12    |
| l_jaw_5        | 11    |
| l_jaw_6        | 10    |
| l_jaw_7        | 9     |
| r_jaw_16       | 0     |
| r_jaw_15       | 1     |
| r_jaw_14       | 2     |
| r_jaw_13       | 3     |
| r_jaw_12       | 4     |
| r_jaw_11       | 5     |
| r_jaw_10       | 6     |
| r_jaw_9        | 7     |
| l_eyebrow_26   | 26    |
| l_eyebrow_25   | 25    |
| l_eyebrow_24   | 24    |
| l_eyebrow_23   | 23    |
| l_eyebrow_22   | 22    |
| r_eyebrow_17   | 17    |
| r_eyebrow_18   | 18    |
| r_eyebrow_19   | 19    |
| r_eyebrow_20   | 20    |
| r_eyebrow_21   | 21    |
| nose_27        | 27    |
| nose_28        | 28    |
| nose_29        | 29    |
| nose_30        | 30    |
| nose_35        | 35    |
| nose_34        | 34    |
| nose_31        | 31    |
| nose_32        | 32    |
| nose_33        | 33    |
| l_eye_45       | 45    |
| l_eye_44       | 44    |
| l_eye_43       | 43    |
| l_eye_42       | 42    |
| l_eye_47       | 47    |
| l_eye_46       | 46    |
| r_eye_36       | 36    |
| r_eye_37       | 37    |
| r_eye_38       | 38    |
| r_eye_39       | 39    |
| r_eye_40       | 40    |
| r_eye_41       | 41    |
| l_outerLips_54 | 54    |
| l_outerLips_53 | 53    |
| l_outerLips_52 | 52    |
| outerLips_51   | 51    |
| outerLips_57   | 57    |
| r_outerLips_48 | 48    |
| r_outerLips_49 | 49    |
| r_outerLips_50 | 50    |
| r_outerLips_59 | 59    |
| r_outerLips_58 | 58    |
| l_outerLips_55 | 55    |
| l_outerLips_56 | 56    |
| l_innerLips_64 | 64    |
| l_innerLips_63 | 63    |
| innerLips_62   | 62    |
| r_innerLips_60 | 60    |
| r_innerLips_61 | 61    |
| r_innerLips_67 | 67    |
| innerLips_66   | 66    |
| l_innerLips_65 | 65    |
</div> 
<br>

I have decided to use Deep Learning since it has more accuracy than your generic OpenCV model and it can be refactored for a certain purpose.

<div align="center">
<img src="/Images/existing.png" width="720"/>
    <br>
    This screenshot represents the current pipeline that I am using. OpenCV is being used to get the camera feed and passing it into facealignment using numpy arrays (For consistent results).
</div> 
<br>

Like I said before, using other models will require you to modify the armature and code accordingly, but everything is modular and properly tagged. The main file is "[facialLandmark.py](/facialLandmark.py)". This file calls all other files and runs the relevant scripts/modules.

## How to Use?
- [ ] Add-on (Or Extension as per Blender 4.2)

I haven't been able to puch too much time in this, but I will surely be making a simple to use add-on (Yeah, still sounds better to me) for the same. The functions are already in place, in case you want to go ahead and make your own, feel free to do so :D

But coming back to how to use it right now?
<ol>
  <li>Copy all the files into a the text editor in a blender file</li>
  <li>Change the paths if you're using a video at <br><br>
      
      59 : def openCVMain(typeInp = 'Image', path = "D:/Programs/Python/TCD/Data/assets/aflw-test.jpg"):
      or
      138 : cap = cv.VideoCapture("D:/Programs/Python/TCD/Data/assets/Demo.mp4")
      
  </li>
  <li>Alternatively, you can pass an "Image", "Camera" or "Video" while calling the <br><br>

      processedData, numFrames = openCVMain(typeInp="Video")

  main function. This automatically switches the input type for OpenCV!
  </li>
  <li>And ofc, you will need to change the output path at line
  
      109 : #cv.imwrite("D:/Programs/Python/TCD/Data/assets/Output.jpg", img)
      or
      151 : out = cv.VideoWriter('output.mp4', fourcc, 20.0, (1280, 720))
      
  </li>
  <li>Important Note! You need to have the armature named "Armature" in the .blend file you're using. Again, I'm planning to fix this later :)</li>
</ol>

## Results


## References
[1] https://openaccess.thecvf.com/content_ICCV_2017/papers/Zhang_S3FD_Single_Shot_ICCV_2017_paper.pdf <br>
