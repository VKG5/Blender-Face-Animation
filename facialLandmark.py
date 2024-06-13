## Importing Libraries
import face_alignment
import numpy as np
import cv2 as cv
import bpy
import os

## Custom Libraires
#from . import animateFace as animFace
animFace = bpy.data.texts['animateFace.py'].as_module()

#from . import basicFuncs as basicFuncs
basicFuncs = bpy.data.texts['basicFuncs.py'].as_module()

## Getting path
#dir = os.path.dirname(bpy.data.filepath)
dir = os.path.dirname(os.path.realpath(__file__))

## GLOBAL VARIABLES
deviceType = 'cuda'

## Function for detecting the landmark in given image/frame
def detectLandmarks(img, scale = 1.0, type = face_alignment.LandmarksType.THREE_D, detector = 'sfd'):
    ## Debugging
    #print("Starting landmark detection")

    # For down-scaling the frames
    scaleFac = scale

    # Setting the Face Alignment Model and API
    fa = face_alignment.FaceAlignment(type, device = deviceType, face_detector = detector)
    
    # Downscale the frame
    img = cv.resize(img, None, fx = scaleFac, fy = scaleFac)
    
    # Detect facial landmarks in the image
    preds = fa.get_landmarks(img)

    if(preds):
        ## Debugging
        #print(f"Landmarks detected : {preds}\n")

        return img, preds
    
    else:
        print("Failed to predict landmarks")

        return img, None

def drawCV(img, face_landmarks, index):
    cv.circle(img, (int(face_landmarks[index][0]), int(face_landmarks[index][1])), 3, (255, 255, 0), -1)  # Red circles for landmarks
    cv.putText(img, str(index), 
                (int(face_landmarks[index][0]) - 5, int(face_landmarks[index][1]) - 5), 
                cv.FONT_HERSHEY_SIMPLEX, 
                0.25, 
                (255, 255, 255), 
                1)
    
def openCVMain(typeInp = 'Image', path = "D:/Programs/Python/TCD/Data/assets/aflw-test.jpg"):
    data = []

    # Image Input
    if(typeInp == 'Image'):
        img = cv.imread(path, cv.IMREAD_COLOR)
        
        ## By default the image is imported as BGR
        #img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        #cv.imshow("Base", img)

        #cv.waitKey(0)

        try:
            print("Starting landmark detection")

            # For down-scaling the frames
            scaleFac = 1.0

            # Setting the Face Alignment Model and API
            fa = face_alignment.FaceAlignment(face_alignment.LandmarksType.THREE_D, device = deviceType, face_detector = 'sfd')
            
            # Downscale the frame
            img = cv.resize(img, None, fx = scaleFac, fy = scaleFac)
            
            # Detect facial landmarks in the image
            preds = fa.get_landmarks(img)

            # Debugging
            #print(f"Landmarks detected : {preds}\n")

            # Checking if we have non-null array
            if preds is not None:
                # Iterating over each landmark each frame
                for face_landmarks in preds:
                    index = 0
                    ## TODO : SCALE THE LANDMARKS TO BE NORMALIZED FOR ANIMATION
                    for x, y, z in face_landmarks:
                        #drawCV(img, face_landmarks, index)
                        #basicFuncs.addCube(coordsXYZ = (x, y, z), scaleXYZ = (3, 3, 3))

                        index += 1

                    data.append((face_landmarks, 1))

            # Display the resulting frame
            #cv.imshow('3D Facial Landmark Detection', img)
                        
            # Saving the image
            #cv.imwrite("D:/Programs/Python/TCD/Data/assets/Output.jpg", img)
            
            # Debugging
            print("Successfully detected landmarks!")

            return data, 1

        except:
            print("Failed to predict landmarks!")    

    # Video input
    else:
        try:
            print("Starting landmark detection")

            # For down-scaling the frames
            scaleFac = 0.5

            # Setting the Face Alignment Model and API
            fa = face_alignment.FaceAlignment(face_alignment.LandmarksType.THREE_D, device = deviceType, face_detector = 'sfd')
            
            cap = None 

            try:
                # Initialize your camera or video capture source
                if(typeInp == 'Camera'):
                    cap = cv.VideoCapture(0)

                elif(typeInp == 'Video'):
                    cap = cv.VideoCapture("D:/Programs/Python/TCD/Data/assets/Demo.mp4")

                # Debugging
                print("Caught camera feed")

            except:
                print("Failed to capture camera feed")

            # Frame Count
            currFrame = 1

            # For writing video
            fourcc = cv.VideoWriter_fourcc(*'mp4v')
            out = cv.VideoWriter('output.mp4', fourcc, 20.0, (1280, 720))

            # Looping over the input frames
            while True:
                # Read a frame from the camera
                ret, frame = cap.read()

                if not ret:
                    print("Failed to read frames!")
                    break
                
                # Get the current frame number
                currFrame += 1

                # Downscale the frame
                frame = cv.resize(frame, None, fx = scaleFac, fy = scaleFac)

                # Detect facial landmarks in the image
                preds = fa.get_landmarks(frame)

                # Checking if we have non-null array
                if preds is not None:
                    # Iterating over each landmark each frame
                    for idx, face_landmarks in enumerate(preds):
                        # ## TODO : SCALE THE LANDMARKS TO BE NORMALIZED FOR ANIMATION
                        for x, y, z in face_landmarks:
                            cv.circle(frame, 
                                      (int(x), int(y)), 
                                      3, 
                                      (255, 255, 0), 
                                      -1)
                            
                            # basicFuncs.addCube(coordsXYZ = (x, y, z), scaleXYZ = (1, 1, 1))
                
                            # cv.putText(frame, str(index), 
                            #            (int(x) + 5, int(y) - 5), 
                            #            cv.FONT_HERSHEY_SIMPLEX, 0.5,
                            #            (0, 0, 255), 
                            #            2)

                        data.append((face_landmarks, currFrame))

                # Write the frame
                out.write(frame)

                # Display the resulting frame
                cv.imshow('3D Facial Landmark Detection', frame)

                # Exit the loop when 'q' is pressed
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
            
            # Release the camera and close OpenCV windows
            cap.release()
            cv.destroyAllWindows()
            
            # Debugging
            print("Successfully detected landmarks!") 

            return data, currFrame

        except:
            print("Failed to predict landmarks!")     

def processAnimation():
    # typeInp : Video, Camera or Image
    processedData, numFrames = openCVMain(typeInp="Video")
    finalData = []

    ## Debugging
    print(f"Number of frames to generate : {numFrames}")
    print("Generating Animation...")

    # Clearing the scene for previous data
    basicFuncs.deleteAll()
    
    ## Recentring the data and scaling it for proper measures
    for values in processedData:
        ## Debugging
        # print(f'Original Data: {values[0]}, Type: {type(values[0])}')

        ## Plotting cubes
        centeredData = basicFuncs.reset_keypoints_to_origin_and_scale(values[0], scale = 0.5)

        ## Debugging
        # print(f'Centered Data: {centeredData}, Type: {type(centeredData[0])}')
        
        finalData.append(centeredData)
    
    ## For generating initial trackers
    for data in finalData:
        index = 0
        for x, y, z in data:
            ## Visualization
            #basicFuncs.addCube(coordsXYZ = (x, y, z), scaleXYZ = (3, 3, 3))
            basicFuncs.addTracker(coordsXYZ = (x, y, z), scaleXYZ = (3, 3, 3), boneIndex = index)

            ## Debugging
            #print(x, y, z)

            index += 1
        break

    if(processedData):
        for i, tup in enumerate(processedData):
            ## Debugging
            print(f"Generating Frame: {tup[1]}")
            #print(f"OG Data: {tup[0]}, Processed Data: {finalData[i]}")
        
            # Generating Animation
            #animFace.generateObjAnimation(finalData[i], tup[1])

        print("Successfully generated animation!")
            
    else:
        print("Failed to parse video")

    print("Process Completed...")
    
def linkAnimation():
    # Clearing existing constraints
    basicFuncs.clearConstraint()

    # Linking the animated points to the bones
    animFace.linkArmature()

processAnimation()
#linkAnimation()