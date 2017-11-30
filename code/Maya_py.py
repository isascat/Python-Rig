import rigLib
reload(rigLib)
help(rigLib)
help(rigLib.rig)
from DinoRig import Dino
import DinoRig
import maya.cmds as mc

characterName = 'Dino'
DinoRig.Dino.build(characterName)


#save skin Weight
reload(DinoRig.Dino_deform)
geoList = mc.ls(sl=1)
DinoRig.Dino_deform.saveSkinWeights(characterName,geoList)

import rigTools
reload(rigTools)
help(rigTools)
from rigTools import bSkinSaver
bSkinSaver.showUI()
