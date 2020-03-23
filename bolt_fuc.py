# -*- coding: utf-8 -*-
#Done by WeSeeTech Ruler
#2020.2.14
#You can follow my Github :-)
#https://github.com/ShengqiangSKR

from abaqus import *
from abaqusConstants import *
from caeModules import *
import sys

#螺栓建模的功能
#在本例中，我们建立一个螺栓的类，并在实际工程中对它进行实例化

class SimpleBolt():
    
    """
    这是一个螺栓的类:
     
     参数-> 
      prt_name:螺栓名称     
      r1:螺头半径
      d1:螺头高度
      r2:螺杆半径
      d2:螺杆长度
      t :螺纹长度
      
    """
    __model_name='Model-1'# <-类变量
    
    def __init__(self,prt_name='',r1=30,d1=15,r2=20,d2=60,t=0.5):
        
        #格式检查，保证输入数值的正确性
        try:
            type(r1).__name__=='int' or type(r1).__name__=='float'
            type(d1).__name__=='int' or type(d1).__name__=='float'
            type(r2).__name__=='int' or type(r2).__name__=='float'
            type(d2).__name__=='int' or type(d2).__name__=='float'
        except:
            raise Exception,'Input ValueError'   
        self.r1=r1
        self.d1=d1
        self.r2=r2
        self.d2=d2
        self.t=t
        #对螺栓进行命名的自适应策略
        if prt_name=='':
            self.prt_name='bolt_{}_{}_{}_{}'.format(r1,d1,r2,d2)
        else:
            self.prt_name=prt_name
        return None
    
    @staticmethod
    def queryInfo():
        """
        对当前的模型进行信息核查
        """
        return None
    
    @property
    def detailInfo():
        """
        获得参数信息
        """
        return None
    
    def createGeom(self):
        """
        根据给定参数，建立几何模型
        """
        #进入模型
        m=mdb.models[SimpleBolt.__model_name]
        #草图模块
        s=m.ConstrainedSketch(name='__profile__', sheetSize=200.0)
        g,v,d,c=s.geometry,s.vertices,s.dimensions,s.constraints
        s.setPrimaryObject(option=STANDALONE)
        s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.0, self.r1))
        #防止名称挤占
        try:
            p = m.Part(name=self.prt_name
                       ,dimensionality=THREE_D
                       ,type=DEFORMABLE_BODY)
        except:
            p = m.Part(name=self.prt_name+'_copy1'
                       ,dimensionality=THREE_D
                       ,type=DEFORMABLE_BODY)
            self.prt_name=self.prt_name+'_copy1'
        p = m.parts[self.prt_name]
        #几何拉伸
        p.BaseSolidExtrude(sketch=s, depth=self.d1+self.d2)
        s.unsetPrimaryObject()
        del m.sketches['__profile__']# <-删除草图
        f, e = p.faces, p.edges
        t = p.MakeSketchTransform(sketchPlane=f[1]
                                 ,sketchUpEdge=e[0]
                                 ,sketchPlaneSide=SIDE1
                                 ,sketchOrientation=RIGHT
                                 ,origin=(0.0, 0.0, self.d1+self.d2))
        s = m.ConstrainedSketch(name='__profile__'
                               ,sheetSize=222.89
                               ,gridSpacing=5.57
                               ,transform=t)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=SUPERIMPOSE)
        p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
        s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.0, self.r1))# <-头半径
        s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.0, self.r2))# <-身半径
        f, e = p.faces, p.edges
        p.CutExtrude(sketchPlane=f[1]
                    ,sketchUpEdge=e[0]
                    ,sketchPlaneSide=SIDE1
                    ,sketchOrientation=RIGHT
                    ,sketch=s
                    ,depth=self.d2
                    ,flipExtrudeDirection=OFF)
        s.unsetPrimaryObject()
        del m.sketches['__profile__']
        return None
    
    def makePartion(self):
        """
        根据给定参数，对实体进行剖分，便于生成结构化网格
        """
        m=mdb.models[SimpleBolt.__model_name]
        p=m.parts[self.prt_name]
        #三个主平面形成的参考面
        p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.0)
        p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=0.0)
        p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=self.d1)
        #螺纹长度参考面/螺栓载荷参考面
        if self.t==0.5:
            p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.5*self.d2+self.d1)
            p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.25*self.d2+self.d1)
        else:
            p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=self.d1+self.d2-self.t)
            p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.5*(self.d2-self.t)+self.d1)
        #进行剖分
        c=p.cells
        f=p.faces
        p.PartitionCellByExtendFace(extendFace=f[0], cells=c)
        #
        c=p.cells
        d1=p.datums
        p.PartitionCellByDatumPlane(datumPlane=d1[d1.keys()[0]], cells=c)
        #以下同理
        c=p.cells
        p.PartitionCellByDatumPlane(datumPlane=d1[d1.keys()[1]], cells=c)
        c=p.cells
        p.PartitionCellByDatumPlane(datumPlane=d1[d1.keys()[2]], cells=c)
        c=p.cells
        p.PartitionCellByDatumPlane(datumPlane=d1[d1.keys()[3]], cells=c)
        c=p.cells
        p.PartitionCellByDatumPlane(datumPlane=d1[d1.keys()[4]], cells=c)
        return None
    
    def getSurfSet(self):
        """
        根据对螺栓的一般定义，生成Surface以及Set集合
        """
        m=mdb.models[SimpleBolt.__model_name]
        p=m.parts[self.prt_name]
        f=p.faces
        datum_feature=p.features
        #bolt load
        load_offset=datum_feature['Datum plane-5'].offset
        innerface=f.getByBoundingBox(zMin=load_offset-0.01
                                    ,zMax=load_offset+0.01)
        p.Surface(name='bolt_load',side1Faces=innerface)
        #contact face
        _tempshell=f.getByBoundingBox(zMin=self.d1-0.01
                                     ,zMax=self.d1+0.01)
        _tempinner=f.getByBoundingCylinder((0,0,self.d1-0.01)
                                          ,(0,0,self.d1+0.01)
                                          ,self.r1-0.5)
        p.Surface(name='_',side1Faces=_tempshell)
        p.Surface(name='__',side1Faces=_tempinner)
        p.SurfaceByBoolean(name='contact_face'
                          ,surfaces=(p.surfaces['_'],p.surfaces['__'])
                          ,operation=DIFFERENCE)
        del p.surfaces['_']
        del p.surfaces['__']
        del _tempshell
        del _tempinner
        #tie face
        dis=self.r2
        t_offset=datum_feature['Datum plane-4'].offset
        tag_point=(self.d1+self.d2+t_offset)/2
        targ_f=f.getClosest(coordinates=((dis,dis,tag_point)
                                        ,(-dis,dis,tag_point)
                                        ,(dis,-dis,tag_point)
                                        ,(-dis,-dis,tag_point),))
        tiefaces=f.findAt(( targ_f[targ_f.keys()[0]][1],)
                         ,( targ_f[targ_f.keys()[1]][1],)
                         ,( targ_f[targ_f.keys()[2]][1],)
                         ,( targ_f[targ_f.keys()[3]][1],))
        p.Surface(name='tie_face',side1Faces=tiefaces)
        #central axis
        p.DatumAxisByCylFace(face=targ_f[targ_f.keys()[0]][0])
        p.features.changeKey(fromName='Datum axis-1', toName='central_axis')
        #org point
        p.DatumPointByCoordinate(coords=(0.0, 0.0, self.d1))
        p.features.changeKey(fromName='Datum pt-1', toName='org_pt')
        #solid set
        c=p.cells
        p.Set(cells=c, name='solid')
        return None        
    
    def generateMesh(self
                    ,elem_type=C3D8I
                    ,sed_size='auto'):
        """
        根据给定参数，对实体进行网格划分
        """
        m=mdb.models[SimpleBolt.__model_name]
        p=m.parts[self.prt_name]
        c=p.cells
        solid_set=p.sets['solid']
        p.setMeshControls(regions=c, technique=STRUCTURED)
        elemType1 = mesh.ElemType(elemCode=elem_type
                                 ,elemLibrary=STANDARD
                                 ,secondOrderAccuracy=OFF #<-二阶精度
                                 ,distortionControl=DEFAULT)
        p.setElementType(regions=solid_set,elemTypes=(elemType1,))
        #进行种子布局
        if sed_size=='auto':
            calculated_size=p.getPartSeeds(DEFAULT_SIZE)
        else:
            calculated_size=sed_size
        p.seedPart(size=calculated_size, deviationFactor=0.1, minSizeFactor=0.1)
        p.generateMesh()
        return None


#the codes below will be running if this file is used as a script       
if __name__=='__main__':
    pass  # <- try to modify this

