# ABAQUS-Python
ABAQUS is a powerful FEA software, widely used in automotive industry, you can find more information here:
[wiki-SIMULIA](https://en.wikipedia.org/wiki/Abaqus)

The codes comes from my daily work. And I will use some simple models for instance to show the fuctions.

## The Scripts May Includes:
1) Pre & Post processing ( Parametric modeling, automatic post-processing);  
2) How to generate the report (ppt or pptx) automatically;  
3) How to write the results to an excel file.

## Some Hints
1) I will finish the upload slowly.
2) As long as i am still an CAE engineer, i will upload more scripts.

### Introduction
### 1-SURFIO
This is a script for surface definition format transformation between abaqus and hypermesh.

(in hypermesh, the surface is defined by "element ID, element surface ID", but in abaqus, internal set was used to cover all elements with the same elem surface ID.) 

##So, if you want to use the inp file generated by abaqus in hypermesh, you will find a lot of sets, which is meanless. This script is for this purpose.

stat:
1) ABAQUS -> HYPERMESH     (finished)
2) hypermesh -> ABAQUS     (ongoing)

### 2-BoltModeler （webinar）
This is a abaqus GUI, and it has several fuctions.(boltfuc is necessary for this GUI)
1) Automatically create a bolt (3D geometry) by several params, as below:
![image](https://github.com/ShengqiangSKR/ABAQUS-Python/tree/master/BoltModeler/Logo/Size.PNG)
2) Automatically mesh the bolt, the user can change the element type and elem size.
3) Automatically find the contact surface, tie surface and bolt load surface, then finish the surface definiton.
（the initial tie length is 1/2 of the body length）
4）Automatically create 3 steps bolt load by a given value.
5) You can use 3-point location method to add a bolt to the assembly.(I got this idea from HyperMesh~) 
![image](https://github.com/ShengqiangSKR/ABAQUS-Python/tree/master/BoltModeler/3pointLoc.gif)

### 3-boltfuc
This is a kernel module, you can use the bolt model build up functions in your own scripts by importing this module.




shengqiang_du@163.com
