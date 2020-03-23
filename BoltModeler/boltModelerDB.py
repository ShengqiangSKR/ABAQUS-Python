# -*- coding: utf-8 -*-
from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class BoltModelerDB(AFXDataDialog):
    
    #ID列表
    [
	ID_CREATE_GEO,
    ID_GENERATE_MSH,
    ID_ADD_ONE,
    ID_HIDE
    ]=range(AFXDataDialog.ID_LAST, AFXDataDialog.ID_LAST+4)
    #
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'BoltModeler',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
        
        #映射功能
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CREATE_GEO, BoltModelerDB.OnCreateGeo)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_GENERATE_MSH, BoltModelerDB.OnGenerateMsh)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_ADD_ONE, BoltModelerDB.OnGetAsb)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_HIDE, BoltModelerDB.OnHideDatum)
        #
            
        GroupBox_1 = FXGroupBox(p=self, text='Create Bolt', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        HFrame_1 = FXHorizontalFrame(p=GroupBox_1, opts=LAYOUT_FILL_X, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        VFrame_3 = FXVerticalFrame(p=HFrame_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        fileName = os.path.join(thisDir, 'BoltSize.PNG')
        icon = afxCreatePNGIcon(fileName)
        FXLabel(p=VFrame_3, text='', ic=icon)
        VFrame_1 = FXVerticalFrame(p=HFrame_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        AFXTextField(p=VFrame_1, ncols=14, labelText='Bolt Name: ', tgt=form.bolt_nameKw, sel=0)
        GroupBox_2 = FXGroupBox(p=VFrame_1, text='Bolt Size', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        VFrame_4 = FXVerticalFrame(p=GroupBox_2, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        HFrame_3 = FXHorizontalFrame(p=VFrame_4, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        AFXTextField(p=HFrame_3, ncols=6, labelText='r1: ', tgt=form.r1Kw, sel=0)
        HFrame_4 = FXHorizontalFrame(p=HFrame_3, opts=0, x=0, y=0, w=0, h=0,
            pl=4, pr=4, pt=0, pb=0)
        AFXTextField(p=HFrame_3, ncols=6, labelText='d1: ', tgt=form.d1Kw, sel=0)
        HFrame_5 = FXHorizontalFrame(p=VFrame_4, opts=LAYOUT_FILL_X, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        AFXTextField(p=HFrame_5, ncols=6, labelText='r2: ', tgt=form.r2Kw, sel=0)
        HFrame_6 = FXHorizontalFrame(p=HFrame_5, opts=0, x=0, y=0, w=0, h=0,
            pl=4, pr=4, pt=0, pb=0)
        AFXTextField(p=HFrame_5, ncols=6, labelText='d2: ', tgt=form.d2Kw, sel=0)
        #增加一个生成几何功能的按键
        hf_as=FXHorizontalFrame(p=VFrame_1, opts=LAYOUT_RIGHT, x=0, y=0, w=0, h=0, pl=5, pr=0, pt=0, pb=0)
        FXButton(p=hf_as, text='Create', ic=None, tgt=self, sel=self.ID_CREATE_GEO, x=0, y=0, w=0, h=0, pl=5, pr=5, pt=1, pb=1)
        #结束
        
        GroupBox_4 = FXGroupBox(p=VFrame_1, text='Mesh Setting', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        VFrame_5 = FXVerticalFrame(p=GroupBox_4, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0)
        AFXTextField(p=VFrame_5, ncols=8, labelText='Seed Size:      ', tgt=form.seed_sizeKw, sel=0)
        ComboBox_2 = AFXComboBox(p=VFrame_5, ncols=0, nvis=1, text='Element Type: ', tgt=form.elem_typeKw, sel=0)
        ComboBox_2.setMaxVisible(10)
        ComboBox_2.appendItem(text='C3D8R')
        ComboBox_2.appendItem(text='C3D8I')
        #增加一个划分网格的按键
        hf_as1=FXHorizontalFrame(p=VFrame_1, opts=LAYOUT_RIGHT, x=0, y=0, w=0, h=0, pl=5, pr=0, pt=0, pb=0)
        FXButton(p=hf_as1, text='Mesh', ic=None, tgt=self, sel=self.ID_GENERATE_MSH, x=0, y=0, w=0, h=0, pl=5, pr=5, pt=1, pb=1)
        #结束
        
        GroupBox_5 = FXGroupBox(p=VFrame_1, text='Add One', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        AFXTextField(p=GroupBox_5, ncols=9, labelText='Bolt Load [N]: ', tgt=form.bolt_loadKw, sel=0)
        frame = AFXVerticalAligner(GroupBox_5, 0, 0,0,0,0, 0,0,0,0)

        # Model combo
        # Since all forms will be canceled if the  model changes,
        # we do not need to register a query on the model.
        #
        #做一些修改
        #删除以下几行
        #self.RootComboBox_3 = AFXComboBox(p=frame, ncols=0, nvis=1, text='Model:', #tgt=form.modelNameKw, sel=0)
        #self.RootComboBox_3.setMaxVisible(10)
        #names = mdb.models.keys()
        #names.sort()
        
        #for name in names:
            #self.RootComboBox_3.appendItem(name)
            
            
        #if not form.modelNameKw.getValue() in names:
        
        
        #form.modelNameKw.setValue( names[0] )
        #结束
        msgCount = 7
        form.modelNameKw.setTarget(self)
        form.modelNameKw.setSelector(AFXDataDialog.ID_LAST+msgCount)
        msgHandler = str(self.__class__).split('.')[-1] + '.onComboBox_3PartsChanged'
        exec('FXMAPFUNC(self, SEL_COMMAND, AFXDataDialog.ID_LAST+%d, %s)' % (msgCount, msgHandler) )

        # Parts combo
        #
        self.ComboBox_3 = AFXComboBox(p=frame, ncols=0, nvis=1, text='Bolt:', tgt=form.partNameKw, sel=0)
        self.ComboBox_3.setMaxVisible(10)
        #增加一个位置设置的按键
        self.pickHandler=boltModelerDBPickHandler(form, form.nodestupleKw, 'Pick the node', NODES, MANY)
        hf_as1=FXHorizontalFrame(p=VFrame_1, opts=LAYOUT_RIGHT, x=0, y=0, w=0, h=0, pl=5, pr=0, pt=0, pb=0)
        FXButton(p=hf_as1, text='Hide', ic=None, tgt=self, sel=self.ID_HIDE, x=0, y=0, w=0, h=0, pl=5, pr=5, pt=1, pb=1)
        FXButton(p=hf_as1, text='Add', ic=None, tgt=self, sel=self.ID_ADD_ONE, x=0, y=0, w=0, h=0, pl=5, pr=5, pt=1, pb=1)
        #结束
        self.form = form
        #getdir(self.pickHandler)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def show(self):

        AFXDataDialog.show(self)

        # Register a query on parts
        #
        self.currentModelName = getCurrentContext()['modelName']
        self.form.modelNameKw.setValue(self.currentModelName)
        mdb.models[self.currentModelName].parts.registerQuery(self.updateComboBox_3Parts)
        #增加注册查找,切换模型时更新部件状态
        registerCurrentContext(self.updateComboBox_3Parts)

        

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def hide(self):

        AFXDataDialog.hide(self)

        mdb.models[self.currentModelName].parts.unregisterQuery(self.updateComboBox_3Parts)
        unregisterCurrentContext(self.updateComboBox_3Parts)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def onComboBox_3PartsChanged(self, sender, sel, ptr):

        self.updateComboBox_3Parts()
        return 1

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def updateComboBox_3Parts(self):
        
        #修改程序
        self.currentModelName = getCurrentContext()['modelName']
        self.form.modelNameKw.setValue(self.currentModelName)
        #结束
        modelName = self.form.modelNameKw.getValue()

        # Update the names in the Parts combo
        #
        self.ComboBox_3.clearItems()
        names = mdb.models[modelName].parts.keys()
        names.sort()
        for name in names:
            self.ComboBox_3.appendItem(name)
        if names:
            if not self.form.partNameKw.getValue() in names:
                self.form.partNameKw.setValue( names[0] )
        else:
            self.form.partNameKw.setValue('')
        
        self.resize( self.getDefaultWidth(), self.getDefaultHeight() )
    
    #增加按键对应的功能
    def OnCreateGeo(self, sender, sel, ptr):
        self.form.cmd.setMethod('creatGeometry')
        self.form.issueCommands()
        return None
    
    def OnGenerateMsh(self, sender, sel, ptr):
        self.form.cmd.setMethod('generateMsh')
        self.form.issueCommands()
        return None
        
    def OnGetAsb(self, sender, sel, ptr):
        #进行模块切换
        switchModule('Load')
        #self.form.cmd.setMethod('getAsb')
        #self.form.issueCommands()
        self.pickHandler.activate()
        return None
    
    def OnHideDatum(self, sender, sel, ptr):
        #隐藏不需要的参考面
        self.form.cmd.setMethod('hideDatum')
        self.form.issueCommands()
        return None
    
    
    
    
    #?如何根据关键字，更改当前显示部件
    def updateCurrentObj(self):
        modelName = self.form.modelNameKw.getValue()
        partName=self.form.partNameKw.getValue()
        p = mdb.models[modelName].parts[partName]
        vpName = session.currentViewportName
        session.viewports[vpName].setValues(displayedObject=p)
        
class boltModelerDBPickHandler(AFXProcedure):

        count = 0

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def __init__(self, form, keyword, prompt, entitiesToPick, numberToPick):
            self.form = form
            self.keyword = keyword
            self.prompt = prompt
            self.numberToPick = ONE # Enum value
            self.entitiesToPick = entitiesToPick
            #增加一些额外的关键字
            self.node1=self.form.node1Kw
            self.node2=self.form.node2Kw
            self.node3=self.form.node3Kw
            
            AFXProcedure.__init__(self, form.getOwner())
            
            
            
            boltModelerDBPickHandler.count += 1
            self.setModeName('boltModelerDBPickHandler%d' % (boltModelerDBPickHandler.count) )

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def getFirstStep(self):
            #初始化所有关键字
            self.node1.setValueToDefault()
            self.node2.setValueToDefault()
            self.node3.setValueToDefault()
            #结束
            
            boltModelerDBPickHandler.count=1
            self.prompt='Pick the first node'
            self.step1=AFXPickStep(self, self.node1, self.prompt, 
            AFXPickStep.NODES,self.numberToPick, sequenceStyle=TUPLE)
            return self.step1            
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def getNextStep(self, previousStep):
                if previousStep == self.step1:
                    boltModelerDBPickHandler.count+=1
                    self.prompt='Pick the second node'
                    self.step2=AFXPickStep(self, self.node2, self.prompt, 
                    AFXPickStep.NODES,self.numberToPick, sequenceStyle=TUPLE)
                    return self.step2
                elif previousStep == self.step2:
                    boltModelerDBPickHandler.count+=1
                    self.prompt='Pick the third node'
                    self.step3=AFXPickStep(self, self.node3, self.prompt, 
                    AFXPickStep.NODES,self.numberToPick, sequenceStyle=TUPLE)
                    return self.step3
                elif previousStep == self.step3:
                    self.makeDecision()
                    return None
        def getLoopStep(self):
            return self.step1
        
        def makeDecision(self):
            self.verifyCurrentKeywordValues()
            self.form.cmd.setMethod('modiPos')
            self.form.issueCommands()
            self.getLoopStep()
        
        def deactivate(self):

            #AFXProcedure.deactivate(self)
            #if  self.numberToPick == ONE and self.keyword.getValue() and self.keyword.getValue()[0]!='<':
                #sendCommand(self.keyword.getSetupCommands() + '\nhighlight(%s)' % self.keyword.getValue() )
            #if self.node!=None:
               #AFXProcedure.deactivate(self)
            #writemessage('ok',1)
            #self.form.cmd.setMethod('mainFunc')
            #self.form.issueCommands()
            AFXProcedure.deactivate(self)


                
#增加一些函数
def writemessage(text,box):
    mw=getAFXApp().getAFXMainWindow()
    if box:
        mw.writeToMessageArea('/'+len(text)*'-'+8*'-'+'\\')
        mw.writeToMessageArea('|'+(len(text)+8)*' '+'|')
        mw.writeToMessageArea('|'+4*' '+text+4*' '+'|')
        mw.writeToMessageArea('|'+(len(text)+8)*' '+'|')
        mw.writeToMessageArea('\\'+len(text)*'-'+8*'-'+'/')
    else:
        mw.writeToMessageArea(text)
def getdir(name):
    fo = open("dir_info_202019.txt", "w")
    seq = dir(name)
    for i in seq:
        fo.write( i+'\n' )
    fo.close()
    return None  