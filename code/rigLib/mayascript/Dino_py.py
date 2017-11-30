import rigLib

reload(rigLib.base.control)
spine = rigLib.base.control.Control(prefix = 'spine1')

reload(rigLib.base.module)

m = rigLib.base.module.Base( characterName = 'Dino_model')