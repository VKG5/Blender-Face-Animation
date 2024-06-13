import bpy
import cv2 as cv
import numpy as np

# Adding a dummy cube to see working
def addCube(initialSize = 1, coordsXYZ = (0, 0, 0), scaleXYZ = (1, 1, 1), frame = 1):
    bpy.ops.mesh.primitive_cube_add(size = initialSize, location = coordsXYZ, scale = scaleXYZ)
    bpy.context.active_object.name = f"Cube.frame_{frame}_landmark"

def addTracker(Type='PLAIN_AXES', Alignment='WORLD', coordsXYZ = (0, 0, 0), scaleXYZ = (1, 1, 1), boneIndex = 1):
    bpy.ops.object.empty_add(type = Type, align = Alignment, location = coordsXYZ, scale = scaleXYZ)
    bpy.context.active_object.name = f"Tracker_{boneIndex}"

# Function for clearing up the scene
def deleteAll():
    for obj in bpy.data.objects:
        if("Tracker_" in obj.name):
            # Deselect all
            bpy.ops.object.select_all(action='DESELECT')

            bpy.data.objects[obj.name].select_set(True)
                
            bpy.ops.object.delete() 
            
    for collection in bpy.data.collections:
        if "_frame" in collection.name:
            bpy.data.collections.remove(collection)

    # Purging to keep the scene clear
    bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
    
## Makes the selected object active in the viewport
def selectedActive(name):
    changeMode('OBJECT')
    
    # Deselecting everything in case nothing was selected
    bpy.ops.object.select_all(action='DESELECT')
    
    ## Selecting the armature in outliner
    obj = bpy.data.objects[f'{name}']
    bpy.context.view_layer.objects.active = obj
    
    ## Making selected object active in Viewport
    bpy.context.active_object.select_set(True)
    
    return obj

## Changing modes/context in Blender
def changeMode(curr):
    ## Checking the current active mode and setting it to object
    if(f'{curr}' not in bpy.context.mode.upper()):
            # Setting mode to OBJECT in case we are in any other mode
            bpy.ops.object.mode_set(mode=f'{curr}')
            return
    return 

def recenter_and_scale_keypoints(keypoints, scale_factor):
    # Convert keypoints to a NumPy array for easier manipulation
    keypoints_array = np.array(keypoints)

    # Step 1: Re-center the keypoints
    center = np.mean(keypoints_array[:, 1:], axis=0)
    centered_keypoints = keypoints_array[:, 1:] - center

    # Step 2: Scale the XYZ values
    scaled_keypoints = centered_keypoints * scale_factor

    # Combine frame numbers and scaled keypoints
    result_keypoints = np.column_stack((keypoints_array[:, 0], scaled_keypoints + center))

    return result_keypoints

def reset_keypoints_to_origin_and_scale(keypoints, scale = 0.5):
    # Recalculate the centroid
    centroid = np.mean(keypoints, axis=0)

    # Translate all points so that the centroid is at the origin
    recentered_data = keypoints - centroid

    scaled_data = recentered_data * scale

    return scaled_data

def clearConstraint():
    armature = selectedActive('Armature')

    # Check if valid and correct type
    if armature and armature.type == 'ARMATURE':
        # Switching to Pose Mode for getting bones
        changeMode('POSE')

        # Iterate over all bones in the armature
        for bone in armature.pose.bones:
            # Clear all constraints from the bone
            for const in bone.constraints:
                bone.constraints.remove(const)

        print("Cleared all constraints!")

        # Switching to Pose Mode for getting bones
        changeMode('OBJECT')

    else:
        print('\'Armature\' object not present or valid!')