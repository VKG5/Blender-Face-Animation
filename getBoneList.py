# Class for processing the bones
# Using a 68-Point Landmark detection to animate our model
# Further changes will be required to use a higher count model
import bpy
import re

def checkEndNumber(s):
    """
    Check if the string ends with a number.
    
    Parameters:
    s (str): The string to check.

    Returns:
    bool: True if the string ends with a number, False otherwise.
    """
    return bool(re.search(r'\d+$', s))

def extractEndNumber(s):
    """
    Extract the number from the end of a string.

    Parameters:
    s (str): The string to extract the number from.

    Returns:
    int or None: The extracted number if present, otherwise None.
    """
    match = re.search(r'\d+$', s)
    return int(match.group()) if match else None

def getBoneList(armatureName = "Armature"):
    """
    Get the bone list which will be animated.

    Parameters:
    armatureName (str) : Name of the armature that should be used for animation.

    Returns:
    int or None: The extract bone list from given armature.
    """
    boneList = {}
    for bone in bpy.data.armatures[armatureName].bones:
        name = bone.name

        if(checkEndNumber(name)):
            ## Debugging
            #print(f"\'{extractEndNumber(name)}\'", end = ", ")
            
            # Only add to list if not None
            id = extractEndNumber(name)
            if(id or id >= 0):
                # Jawline - 0-16
                if(id <= 16):
                    id = abs(16 - id + 0)

                boneList[name] = id

    return boneList