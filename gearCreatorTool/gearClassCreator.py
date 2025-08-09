# Created based on the Python For Maya: Artist Friendly Programming course on Udemy by Dhruv Govil
# Link to Udemy course: https://www.udemy.com/course/python-for-maya

# Last revised: 2024/07/22

# Description: This script procedurally generates geometries in the shape of a gear.
# You can specify the number of teeth that the gear should have.


from maya import cmds

class Gear(object):
    """
    This is a Gear object that lets us create and modify a gear
    """

    def __init__(self):
        """
        The __init__ method lets us set default values
        """
        self.transform = None
        self.extrude = None
        self.constructor = None


    def createGear(self, teeth=10, length=0.3):
        """
        This method creates a gear
        """
        spans = teeth * 2

        self.transform, self.constructor = cmds.polyPipe(subdivisionsAxis=spans)
        sideFaces = range(spans*2, spans*3, 2)

        cmds.select(clear=True)
        for face in sideFaces:
            cmds.select(f'{self.transform}.f[{face}]', add=True)

        self.extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]


    def changeTeeth(self, teeth=10, length=0.3):
        """
        This method modifies the teeth of a gear without creating a new gear
        """
        spans = teeth*2

        cmds.polyPipe(self.constructor, edit=True, subdivisionsAxis=spans)

        sideFaces = range(spans*2, spans*3, 2)
        faceNames = []

        for face in sideFaces:
            faceName = f'f[{face}]'
            faceNames.append(faceName)

        cmds.setAttr(f'{self.extrude}.inputComponents', len(faceNames), *faceNames, type="componentList")

        cmds.polyExtrudeFacet(self.extrude, edit=True, ltz=length)