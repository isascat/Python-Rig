"""
Dino dragon rig setup
main module
"""

from rigLib.base import control
from rigLib.base import module

from rigLib.rig import spine
from rigLib.rig import neck
from rigLib.rig import ikChain
from rigLib.rig import leg
from rigLib.rig import arm
# from rigLib.rig import headParts

from rigLib.utils import joint
 
from . import project
from . import Dino_deform

import maya.cmds as mc
 
sceneScale = project.sceneScale
mainProjectPath = project.mainProjectPath
  
modelFilePath = '%s/%s/model/%s_model.mb'
builderSceneFilePath = '%s/%s/builder/%s_builder.mb'
  
rootJnt = 'root1_jnt'
headJnt = 'head1_jnt'
chestJnt = 'spineChest_ctl'
pelvisJnt = 'pelvis'
neckloc = 'neck_loc'
jawJnt = 'jaw1_jnt'
  
def build( characterName ):
     
    """
    main function to build character rig
    """
     
    # new scene
    mc.file( new = True, f = True )
     
    # import builder scene
    modelFile = builderSceneFilePath % ( mainProjectPath, characterName, characterName )
    mc.file( modelFile, i = 1 )
       
    # make base
    baseRig = module.Base( characterName = characterName, scale = sceneScale, mainCtrlAttachObj = headJnt )
     
    # mainCtrlAttachObj = headJnt
     
    # import model
    modelFile = modelFilePath % ( mainProjectPath, characterName, characterName )
    mc.file( modelFile, i = 1 )
     
    # parent model
    modelGrp = '%s_model_grp' % characterName
    mc.parent( modelGrp, baseRig.modelGrp )
      
    # parent skeleton
    mc.parent( rootJnt, baseRig.jointsGrp )
      
    # deform setup
    Dino_deform.build( baseRig, characterName )
      
    # control setup
    makeControlSetup( baseRig )
     
    # delete build objects
     
    builderGrp = 'builder_grp'
    mc.delete( builderGrp )
     
     
def makeControlSetup( baseRig ):
       
    """
    make control setup
    """
      
#     # adjust orientation of feet
#     mc.setAttr( 'l_hand1_jnt.jo', 138.28570432475698, -48.90539524404269, -30.284152362844438 )
#     mc.setAttr( 'r_hand1_jnt.jo', 138.28570432475684, -48.905395244042566, -30.28415236284434 )
#       
    # spine
      
    spineJoints = ['hip','spine1_jnt', 'spine2_jnt', 'spine3_jnt', 'spine4_jnt']
      
    spineRig = spine.build( 
                          spineJoints = spineJoints,
                          rootJnt = rootJnt,
                          spineCurve = 'spine_crv',
                          bodyLocator = 'body_loc',
                          chestLocator = 'chest_loc',
                          pelvisLocator = 'pelvis_loc',
                          prefix = '',
                          rigScale = sceneScale,
                          baseRig = baseRig
                          )
      
    # neck
       
    neckJoints = ['neck1', 'neck2', 'neck3', 'neck4', 'neck5', 'neck6']
       
    neckRig = neck.build( 
                      neckJoints = neckJoints,
                      headJnt = headJnt,
                      chestJnt = chestJnt,
                      neckloc = neckloc,
                      neckCurve = 'neck_crv',
                      prefix = 'neck',
                      rigScale = sceneScale,
                      baseRig = baseRig
                      )
       
    mc.parentConstraint( spineJoints[-2], neckRig['baseAttachGrp'], mo = 1 )
    mc.parentConstraint( spineRig['bodyCtrl'].C, neckRig['bodyAttachGrp'], mo = 1 )
       
    # tail
        
    tailJoints = joint.listHierarchy( 'tail01' )
        
    tailRig = ikChain.build( 
                  chainJoints = tailJoints,
                  chainCurve = 'tail_crv',
                  prefix = 'tail',
                  rigScale = sceneScale,
                  smallestScalePercent = 0.1,
                  fkParenting = False,
                  baseRig = baseRig
                  )
        
    mc.parentConstraint( pelvisJnt, tailRig['baseAttachGrp'], mo = 1 )
        
    # tongue
        
    tongueJoints = joint.listHierarchy( 'tongue1' )
        
    tongueRig = ikChain.build( 
                  chainJoints = tongueJoints,
                  chainCurve = 'tongue_crv',
                  prefix = 'tongue',
                  rigScale = sceneScale * 0.1,
                  smallestScalePercent = 0.3,
                  fkParenting = True,
                  baseRig = baseRig
                  )
        
    mc.parentConstraint( jawJnt, tongueRig['baseAttachGrp'], mo = 1 )
        
    # left arm
      
    legJoints = ['lShoulder','lArm','lForearm','lHand','lHand_02']
    topToeJoints = ['l_Thumb_01', 'l_Index_01', 'l_Mid_01']
 
     
    lArmRig = arm.build( 
              legJoints = legJoints,
              topToeJoints = topToeJoints,
              pvLocator = 'l_arm_pole_vector_loc',
              scapulaJnt = '',
              prefix = 'l_arm',
              rigScale = sceneScale,
              baseRig = baseRig
              )
      
    mc.parentConstraint( spineJoints[-1], lArmRig['baseAttachGrp'], mo = 1 )
    mc.parentConstraint( spineRig['bodyCtrl'].C, lArmRig['bodyAttachGrp'], mo = 1 )
      
      
    # right arm
      
    legJoints = ['rShoulder','rArm','rForearm','rHand','rHand_02']
    topToeJoints = ['r_Thumb_01', 'r_Index_01', 'r_Mid_01']
      
    rArmRig = arm.build( 
              legJoints = legJoints,
              topToeJoints = topToeJoints,
              pvLocator = 'r_arm_pole_vector_loc',
              scapulaJnt = '',
              prefix = 'r_arm',
              rigScale = sceneScale,
              baseRig = baseRig
              )
      
    mc.parentConstraint( spineJoints[-2], rArmRig['baseAttachGrp'], mo = 1 )
    mc.parentConstraint( spineRig['bodyCtrl'].C, rArmRig['bodyAttachGrp'], mo = 1 )
      

    # left leg
       
    legJoints = ['lThigh', 'lShin', 'lAnkle','lFoot','lFoot_2']
    topToeJoints = ['l_ToeIn_01', 'l_ToeMid_01', 'l_ToeOut_01']
       
    lLegRig = leg.build( 
              legJoints = legJoints,
              topToeJoints = topToeJoints,
              pvLocator = 'l_leg_pole_vector_loc',
              scapulaJnt = '',
              prefix = 'l_leg',
              rigScale = sceneScale,
              baseRig = baseRig
              )
       
    mc.parentConstraint( spineJoints[-2], lLegRig['baseAttachGrp'], mo = 1 )
    mc.parentConstraint( spineRig['bodyCtrl'].C, lLegRig['bodyAttachGrp'], mo = 1 )
       
    # right leg
        
    legJoints = ['rThigh', 'rShin', 'rAnkle','rFoot','rFoot_2']
    topToeJoints = ['r_ToeIn_01', 'r_ToeMid_01', 'r_ToeOut_01']
           
    lLegRig = leg.build( 
              legJoints = legJoints,
              topToeJoints = topToeJoints,
              pvLocator = 'r_leg_pole_vector_loc',
              scapulaJnt = '',
              prefix = 'r_leg',
              rigScale = sceneScale,
              baseRig = baseRig
              )
       
    mc.parentConstraint( spineJoints[-2], lLegRig['baseAttachGrp'], mo = 1 )
    mc.parentConstraint( spineRig['bodyCtrl'].C, lLegRig['bodyAttachGrp'], mo = 1 )      
#     # head parts
#       
#     muzzleJoints = ['muzzle1_jnt', 'muzzle2_jnt']
#       
#     headParts.build( 
#                   headJnt = headJnt,
#                   jawJnt = jawJnt,
#                   muzzleJoints = muzzleJoints,
#                   leftEyeJnt = 'l_eye1_jnt',
#                   rightEyeJnt = 'r_eye1_jnt',
#                   prefix = 'headParts',
#                   rigScale = sceneScale,
#                   baseRig = baseRig
#                   )

