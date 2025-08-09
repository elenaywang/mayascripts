# Created based on the Python For Maya: Artist Friendly Programming course on Udemy by Dhruv Govil
# Link to Udemy course: https://www.udemy.com/course/python-for-maya

# Last revised: 2024/06/29

# Description: This script renames objects within a Maya scene for easy identification
# by appending a suffix that specifies what type of object it is.


from maya import cmds

SUFFIXES = {
    "mesh": "geo",
    "joint": "jnt",
    "camera": None,
    "ambientLight": "lgt"
}

DEFAULT_SUFFIX = "grp"


def rename(selection=False):
    """
    This function will rename any objects to have the correct suffix.
    Args:
        selection: Whether or not we use the current selection.

    Returns:
        A list of all the objects we operated on.
    """

    objects = cmds.ls(selection=selection, dag=True, long=True)

    # this function cannot run if there is no selection and no objects
    if selection and not objects:
        raise RuntimeError("You don't have anything selected!")
        
    objects.sort(key=len, reverse=True)

    for obj in objects:
        shortName = obj.split("|")[-1]
        
        children = cmds.listRelatives(obj, children=True, fullPath=True) or []
        
        if len(children) == 1:
            child = children[0]
            objType = cmds.objectType(child)
        else:
            objType = cmds.objectType(obj)
            
        suffix = SUFFIXES.get(objType, DEFAULT_SUFFIX)

        if not suffix:
            continue

        if obj.endswith(suffix):
            continue
            
        newName = f"{shortName}_{suffix}"
        cmds.rename(obj, newName)

        index = objects.index(obj)
        objects[index] = obj.replace(shortName, newName)

    return objects