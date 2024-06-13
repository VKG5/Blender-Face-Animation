import bpy
import math
from mathutils import Matrix, Vector

# Custom Libraires
#from . import getBoneList as boneList
boneList = bpy.data.texts['getBoneList.py'].as_module()

#from . import basicFuncs as basicFuncs
basicFuncs = bpy.data.texts['basicFuncs.py'].as_module()

bonesDict = boneList.getBoneList() 

## Converting coordinates to local space
def convertCoords(coords, boneMatrix):
    blender_coords = Vector(coords)
    
    local_coords = boneMatrix @ blender_coords
    
    return local_coords

def getArmature(name):
    return basicFuncs.selectedActive(name)

def generateFrame(face_landmarks, index):
    # Getting the armature object
    armature = getArmature('Armature')

    # Chaning mode to pose
    basicFuncs.changeMode('POSE')

    initialMatrix = {}

    for boneName in bonesDict:
        ## Debugging
        # print(f"Initial Matrix: {initialMatrix}")
        
        # Setting the frame
        bpy.context.scene.frame_set(index)
        
        ## Deselecting all selected bones
        #bpy.ops.pose.select_all(action='DESELECT')

        ## Getting the current bone
        bone = armature.pose.bones.get(boneName)

        ## Debugging
        # print(boneName, face_landmarks[bonesDict[boneName]], index)
        # print(boneName, face_landmarks[bonesDict[boneName]], bonesDict[boneName], index, bool(bone))

        if bone:
            # Coords
            coords = (float(face_landmarks[bonesDict[boneName]][0]), 
                      float(face_landmarks[bonesDict[boneName]][1]), 
                      float(face_landmarks[bonesDict[boneName]][2]))

            if(boneName not in initialMatrix):
                    initialMatrix[boneName] = bone.matrix.inverted()

            ## Debugging
            #print(f"Original Coords: {coords}")

            coords = convertCoords(coords, initialMatrix[boneName])

            ## Debugging
            #print(f"Converted Coords: {coords}")
                
            bone.location = coords

            # Keyframe the head location
            bone.keyframe_insert(data_path="location")
    
    basicFuncs.changeMode('OBJECT')

    ## Debugging
    print(f"Generated frame: {index}")

def generateObjAnimation(face_landmarks, index):
    # Deselecting everything
    bpy.ops.object.select_all(action='DESELECT')

    # Chaning mode to object
    basicFuncs.changeMode('OBJECT')

    for i, data in enumerate(face_landmarks):
        # Setting the frame
        bpy.context.scene.frame_set(index)

        # Get the empty object by name
        trackerName = f"Tracker_{i}"
        tracker = bpy.data.objects.get(trackerName)

        # If tracker exists
        if(tracker):
            ## Debugging
            #print(f"Tracker: {tracker.name}, Location: {data}")
             
            tracker.location = (data[0], data[1], data[2])

            # Insert a keyframe
            tracker.keyframe_insert(data_path="location", frame=index)
        
def linkArmature():
    # Getting the armature object
    armature = getArmature('Armature')

    # Chaning mode to pose
    basicFuncs.changeMode('POSE')

    for boneName in bonesDict:
        ## Getting the current bone
        bone = armature.pose.bones.get(boneName)

        # If the bone is valid
        if(bone):
            ## Debugging
            #print(bone.name, bonesDict[boneName])

            trackerName = f"Tracker_{bonesDict[boneName]}"
            tracker = bpy.data.objects.get(trackerName)

            # If tracker is valid, attach the bone
            if(tracker):
                # Checking if the same constraint already exists or not
                # If yes, remove
                exists = bone.constraints.get(trackerName)
                if exists:
                    bone.constraints.remove(exists)

                #print(tracker.name, tracker.location)
                # Add a Copy Location constraint to the bone
                constraint = bone.constraints.new('COPY_LOCATION')

                # Setting properties
                constraint.name = trackerName
                constraint.target = tracker
                constraint.influence = 0.5
                constraint.owner_space = 'WORLD'
                constraint.target_space = 'LOCAL'

                # Maintain original offset
                constraint.use_offset = False

                print("Successfully linked the armature!")

            else:
                print(f"Tracker: {trackerName} NOT FOUND!")

        else:
            print(f"Bone: {boneName} NOT FOUND!")
    
    # Chaning mode to object
    basicFuncs.changeMode('OBJECT')
