from abaqusGui import *
from abaqusConstants import ALL
import osutils, os


###########################################################################
# Class definition
###########################################################################

class BoltModeler_plugin(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='mainFunc',
            objectName='boltModeler_kernel', registerQuery=False)
        pickedDefault = ''
        self.bolt_nameKw = AFXStringKeyword(self.cmd, 'bolt_name', True, '')
        self.r1Kw = AFXFloatKeyword(self.cmd, 'r1', True)
        self.d1Kw = AFXFloatKeyword(self.cmd, 'd1', True)
        self.r2Kw = AFXFloatKeyword(self.cmd, 'r2', True)
        self.d2Kw = AFXFloatKeyword(self.cmd, 'd2', True)
        self.seed_sizeKw = AFXFloatKeyword(self.cmd, 'seed_size', True)
        self.elem_typeKw = AFXStringKeyword(self.cmd, 'elem_type', True)
        self.bolt_loadKw = AFXFloatKeyword(self.cmd, 'bolt_load', True)
        self.modelNameKw = AFXStringKeyword(self.cmd, 'modelName', True)
        self.partNameKw = AFXStringKeyword(self.cmd, 'partName', True)
        self.nodestupleKw = AFXTupleKeyword(self.cmd, 'nodestuple', True)
        self.node1Kw=AFXObjectKeyword(self.cmd, 'node1', True)
        self.node2Kw=AFXObjectKeyword(self.cmd, 'node2', True)
        self.node3Kw=AFXObjectKeyword(self.cmd, 'node3', True)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import boltModelerDB
        return boltModelerDB.BoltModelerDB(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        for kw1,kw2,d in self.radioButtonGroups.values():
            try:
                value = d[ kw1.getValue() ]
                kw2.setValue(value)
            except:
                pass
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Register the plug-in
#
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
    buttonText='BoltModeler', 
    object=BoltModeler_plugin(toolset),
    messageId=AFXMode.ID_ACTIVATE,
    icon=None,
    kernelInitString='import boltModeler_kernel',
    applicableModules=ALL,
    version='0.9',
    author='Du Shengqiang',
    description='WeSee Tech.',
    helpUrl='http://www.weseetech.com/'
)
