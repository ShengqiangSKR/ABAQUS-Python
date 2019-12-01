# !/usr/bin/python
# -*-coding: UTF-8-*-
# Du. Shengqiang
# 

import os
import sys
import copy

# path definition
#thisPath = os.path.abspath(__file__)
#thisDir = os.path.dirname(thisPath)

#修改以下定义
#1.原始inp名称，将其放在工作目录下
filename='Job-single.inp' 
#2.输出文件名称
outPutFileName='Job-single_modify.inp'
#以下无需修改

def FormatTrans(data=[],datatype='',to='',output=''):

    # keyword to = HYPERMESH or ABAQUS
    id_aba,id_hm=TitleMatch(data=data, symbol='*Surface, type=ELEMENT,', datatype = datatype)
    if to=='HYPERMESH':
        idall=id_aba
        del id_hm
        newdata= copy.deepcopy(data)
        appenddata_dict={}
        for idx in idall:
            #获得组成该面的S类型
            newdata,stype=FindDefBlow(data=newdata,st=idx)
            #对所有S类型对应的单元进行查找
            #indexdic format -> {'S2':45}
            indexdict=FindDefUp(data=newdata,st=idx,ref=stype)
            indexcp=sorted(indexdict.items(), key=lambda d: d[1], reverse=False)
            #print(indexcp)
            #对数据进行重写
            newrow=[]#单个面的所有组成信息 -> 45, S2```
            for i in range(len(indexcp)):
                try:
                    #_a=indexcp[i][1]+1
                    #_b=indexcp[i+1][1]
                    #print(_a,_b)
                    _numberow=newdata[indexcp[i][1]+1:indexcp[i+1][1]]
                except:
                    _numberow = newdata[indexcp[i][1] + 1:idx]
                #abaqus keyword 支持用generate的方法生成更加简洁的序列，需要区分这种情况
                if newdata[indexcp[i][1]][-8:]=='generate':
                    for txt in _numberow:
                        lbdata=txt.split(',')
                        if len(lbdata[-1])==0:
                                del lbdata[-1]
                    #按第三位递进
                        for n in range(int(lbdata[0]),int(lbdata[1])+1,int(lbdata[2])):
                            newlb = str(n) + ', ' + indexcp[i][0]
                            newrow.append(newlb)
                #以下是常规情况
                else:
                    for txt in _numberow:
                        labellist=txt.split(',')
                        if len(labellist[-1])==0:
                            del labellist[-1]
                        for lb in labellist:
                            newlb=lb+', '+indexcp[i][0]
                            newrow.append(newlb)
            #print(newrow)
            appenddata_dict[idx]= newrow           
            #需要替换掉原来的内容或者生成新的文件
            #1.去除internal set定义行,将其转换为None，方便后续删除
            newdata[indexcp[0][1]:idx]=[None]*(idx-indexcp[0][1])
        #2.将整个list拆开
        print('Start Main Process!~')
        idall.insert(0,-1)
        split_id=idall
        block_all=[]
        print('Step1: Seperate Source Data into Blocks')
        for count_ in range(len(split_id)-1):
            block=newdata[split_id[count_]+1:split_id[count_+1]+1]
            block_all.append(block)
        block_all.append(newdata[split_id[-1]+1:])
        if len(appenddata_dict.values())==len(block_all)-1:
            print('Len Match')
        FinalData=[]
        appenddata_cp=sorted(appenddata_dict.items(), key=lambda d: d[0], reverse=False)
        #print(block_all[-2])
        #print(appenddata_cp[-2][1])
        print('Step2: Join Blocks together')
        for i in range(len(appenddata_cp)):
            FinalData += block_all[i]+appenddata_cp[i][1]         
        FinalData+=block_all[-1]
        FinalData=[x+'\n' for x in FinalData if x!=None]
        WriteData(FinalData,output)        
            

            
            
#向上寻找各set中包含的单元
#暂用方法，暂时不做修改            
def FindDefUp(data,st,ref):
    facename=data[st].split('name=')[1]
    indexdict={}
    while ref!=[]:
        if facename in data[st-1]:
            _start=data[st-1].index(facename)+len(facename)
            _stype=data[st-1][_start+1:_start+3]
            print('Find Stype Definition Line: {} -> line {}'.format(_stype,st-1))
            ref.remove(_stype)
            indexdict[data[st-1][_start+1:_start+3]]=st-1
        st-=1  
    print('--------------Over--------------')
    print('\n'*2)
    return indexdict


#寻找面定义下，该面的组成set
#通用方法，无需修改
def FindDefBlow(data,st):
    facename=data[st].split('name=')[1]
    print ('----------Surface Info----------')
    print ('Surface Name -> {}'.format(facename))
    stype=[]
    print('Include Internal Sets: ')
    while facename in data[st+1]:
        print(data[st+1])
        stype.append(data[st+1][-2:])
        data[st+1]=None
        st+=1
    print ('Stype: {}'.format(stype))
    print ('----------Detail----------')
    return data, stype












def TitleMatch(data=[], symbol='', datatype = ''):

    idx_hpmsh=[]
    idx_abaqus=[]

    # query *Surface definition
    for i in range(len(data)):
        if symbol in data[i] and datatype == 'HPMSH':
            idx_hpmsh.append(i)
        elif symbol in data[i] and datatype == 'ABAQUS':
            idx_abaqus.append(i)
        elif symbol in data[i] and datatype == '':
            # we need judge the data type
            if i!=len(data)-1:
                if data[i].split('name=')[1] in data[i+1]:
                    idx_abaqus.append(i)
                else:
                    idx_hpmsh.append(i)
        else:
            continue
    print('Find All Surface Definition Lines')
    if datatype=='ABAQUS':
        print('Find {} surfaces named in ABAQUS format'.format(len(idx_abaqus)))
        print(idx_abaqus)
    else:
        print('Find {} surfaces named in HYPERMESH format'.format(len(idx_hpmsh)))
        print(idx_hpmsh)    
    return idx_abaqus, idx_hpmsh

def WriteData(data,file):
    f=open(file,'w')
    f.writelines(data)
    print('Modification Process Succeeds !')
    print('A New .inp file has been generated! -> {}'.format(file))
    f.close()
        
    
    
    
    
    
# read .inp file


def ReadData(file):
    with open(file) as f:
        data=f.readlines()
    f.close()    
    data=map(StripFuc,data)
    return data

#
def StripFuc(x):
    return x.strip('\n')
    
    
#main
file=filename 
write_to_file=outPutFileName  
thisDir=os.getcwd()
dataDir=os.path.join(thisDir,file)
FormatTrans(data=ReadData(dataDir),datatype='ABAQUS',to='HYPERMESH',output=write_to_file)