# -*- coding: utf-8 -*-
#Done by WeSeeTech Ruler
#2020.2.15
#You can follow my Github :-)
#https://github.com/ShengqiangSKR
#
from abaqus import *
from abaqusConstants import *
from caeModules import *
from bolt_fuc import *
import numpy as np
import os

def mainFunc(bolt_name
            ,r1
            ,d1
            ,r2
            ,d2
            ,seed_size
            ,elem_type
            ,bolt_load
            ,modelName
            ,partName
            ,nodestuple=''
            ,node1=None
            ,node2=None
            ,node3=None):
    print(str(node1.coordinates))
    print(str(node2.coordinates))
    print(str(node3.coordinates))
    return None
    
    
def creatGeometry(bolt_name
                 ,r1
                 ,d1
                 ,r2
                 ,d2
                 ,seed_size
                 ,elem_type
                 ,bolt_load
                 ,modelName
                 ,partName
                 ,nodestuple=''
                 ,node1=None
                 ,node2=None
                 ,node3=None):
    """
    按下【create】键后执行的操作
    """
    bolt=SimpleBolt(bolt_name,r1,d1,r2,d2)
    print('Step1: initialization...')
    bolt.createGeom()
    print('Step2: generate 3D geometry...')
    bolt.makePartion()
    print('Step3: make the partition...')
    bolt.getSurfSet()
    print('Step4: define the surfaces and sets...')
    #将模型上浮至当前视图
    p = mdb.models[modelName].parts[bolt_name]
    vpName = session.currentViewportName
    session.viewports[vpName].setValues(displayedObject=p)
    print('Complete geometric setup!')
    return None

def generateMsh(bolt_name
               ,r1
               ,d1
               ,r2
               ,d2
               ,seed_size
               ,elem_type
               ,bolt_load
               ,modelName
               ,partName
               ,nodestuple=''
               ,node1=None
               ,node2=None
               ,node3=None): 
    """
    按下【mesh】键后执行的操作
    """ 
    #根据字符串生成一个常量
    e_type=SymbolicConstant(elem_type)
    bolt=SimpleBolt(bolt_name)
    bolt.generateMesh(elem_type=e_type,sed_size=seed_size)
    vpName = session.currentViewportName
    session.viewports[vpName].partDisplay.setValues(mesh=ON)
    return None  

def modiPos(bolt_name
           ,r1
           ,d1
           ,r2
           ,d2
           ,seed_size
           ,elem_type
           ,bolt_load
           ,modelName
           ,partName
           ,nodestuple=''
           ,node1=None
           ,node2=None
           ,node3=None): 
    """
    1.根据三点，形成一个临时datum_axis
    将螺栓装配至模型，并生成三个step，用以加载螺栓力
    """ 
    m=mdb.models[modelName]
    a = m.rootAssembly
    vpName = session.currentViewportName
    session.viewports[vpName].assemblyDisplay.setValues(mesh=ON)
    #形成临时datunm axis
    tmp_point1=a.DatumPointByCoordinate(coords=node1.coordinates)
    tmp_point2=a.DatumPointByCoordinate(coords=node2.coordinates)
    tmp_point3=a.DatumPointByCoordinate(coords=node3.coordinates)
    d = a.datums
    tmp_axis=a.DatumAxisByThreePoint(point1=d[tmp_point1.id]
                                    ,point2=d[tmp_point2.id]
                                    ,point3=d[tmp_point3.id])
    #导入螺栓
    p = m.parts[partName]
    #获得命名序号
    name_list=a.instances.keys()
    ord=[]
    for item in name_list:
        if partName in item:
            try:
                _=int(item.split('-')[-1]) 
                ord.append(_)
            except:
                continue
    ord.sort()
    if ord==[]:
        num=1
    else:
        num=ord[-1]+1
    #命名
    bolt_instance_name=partName+'-'+str(num)
    bolt=a.Instance(name=bolt_instance_name, part=p, dependent=ON)
    #共轴约束
    d11=bolt.datums
    instance_datum_id=d11.keys()[-2]
    a.EdgeToEdge(movableAxis=d11[instance_datum_id], fixedAxis=d[tmp_axis.id], flip=OFF)
    #转化为绝对坐标
    bolt.ConvertConstraints()
    #删除临时参考点及参考轴
    #del tmp_axis
    #del tmp_point1
    #del tmp_point2
    #del tmp_point3
    del (a.features[tmp_axis.name]
        ,a.features[tmp_point1.name]
        ,a.features[tmp_point2.name]
        ,a.features[tmp_point3.name])
    #获得目标坐标
    dest_coord,_=getcent(node1.coordinates,node2.coordinates,node3.coordinates)
    dest_coord1=dest_coord.reshape(-1,)
    dest_coord=[dest_coord1[0,0],dest_coord1[0,1],dest_coord1[0,2]]
    
    #进行平移
    instance_datum_id=d11.keys()[-1]
    vector_move=np.array(dest_coord)-np.array(d11[instance_datum_id].pointOn)
    a.translate(instanceList=(bolt_instance_name, ), vector=tuple(vector_move))
    
    #可选操作，加载
    boltload(model_name=modelName,bolt_name=bolt_instance_name
            ,bolt_force=bolt_load,datum_axis_id=d11.keys()[-2])
    #
    return None  

def hideDatum(bolt_name
               ,r1
               ,d1
               ,r2
               ,d2
               ,seed_size
               ,elem_type
               ,bolt_load
               ,modelName
               ,partName
               ,nodestuple=''
               ,node1=None
               ,node2=None
               ,node3=None): 
    """
    按下【hide】键后执行的操作
    """ 
    print('This Function is not aviliable in this demo')
    print('You can modify this fuction in boltModeler_kernel.py')
    print('shengqiang.du@weseetch.com   <- any other technical issue, ask him for help~')
    return None 
    
#common function
def boltload(model_name
            ,bolt_name
            ,bolt_force
            ,datum_axis_id
            ,stp1_name='Step-pretension'
            ,stp2_name='Step-applyLoad'
            ,stp3_name='Step-fixPos'):
    """
    螺栓加载,如存在step，则使用之前的，如不存在，则新创建
    三步式加载
    """
    m=mdb.models[model_name]
    a = m.rootAssembly
    stp=m.steps
    if len(stp.keys())<=3:
        stp1=m.StaticStep(name=stp1_name, previous='Initial', initialInc=0.2, nlgeom=ON)
        stp2=m.StaticStep(name=stp2_name, previous=stp1_name, initialInc=0.1, nlgeom=ON)
        stp3=m.StaticStep(name=stp3_name, previous=stp2_name, initialInc=0.2, nlgeom=ON)
    #创建载荷
    stps_name=stp.keys()
    bolt_instance=a.instances[bolt_name]
    region = bolt_instance.surfaces['bolt_load']
    d11=bolt_instance.datums
    bolt_load=m.BoltLoad(name='BoltLoad-'+bolt_name,createStepName=stps_name[1]
    ,region=region,magnitude=0.01,boltMethod=ADJUST_LENGTH,datumAxis=d11[datum_axis_id])
    #step2
    bolt_load.setValuesInStep(stepName=stps_name[2], magnitude=bolt_force, boltMethod=APPLY_FORCE)
    #step3
    bolt_load.setValuesInStep(stepName=stps_name[3],boltMethod=FIX_LENGTH)
    return None
    
#common function
def getcent(pt1,pt2,pt3):
    """
    利用numpy计算三维空间中任意三点构成的圆的圆心及半径
    pt1,pt2,pt3分别为满足右手定则的三点
    """
    a=np.array(pt1)
    b=np.array(pt2)
    c=np.array(pt3)
    ab=b-a
    ac=c-a
    abac=np.array([ab,ac])
    abac=np.transpose(abac)
    x=np.dot(np.transpose(abac),abac)
    x=np.mat(x)
    y=np.array([np.dot(ab,np.transpose(ab))/2,np.dot(ac,np.transpose(ac))/2])
    y=np.mat(y)
    w=x.I*y.T
    o=np.mat(abac)*w+np.mat(a).T
    oa=np.linalg.norm(o.T-a)
    ob=np.linalg.norm(o.T-b)
    oc=np.linalg.norm(o.T-c)
    r=(oa+ob+oc)/3
    return o,r     