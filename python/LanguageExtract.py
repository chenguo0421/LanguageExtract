# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import sys
import os
import xml.dom.minidom as Dom
import xml.etree.ElementTree as ET
import shutil


# 创建文件夹
def mkdir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')




# 创建指定的临时文件，若存在，则先删除再创建
def create_text(file_path,msg):
     if os.path.exists(file_path):
        os.remove(file_path)

     file = open(file_path, 'w', encoding="utf-8")
     file.write(msg)
     file.close()


# 检查一个文件是否有内容
def checkFileEmpty(file_path):
    size = os.path.getsize(file_path)
    if size == 0:
        print('文件是空的')
        return True
    else:
        print('文件不是空的')
        return False




# 根据xmlPath生成strings.xml文件
def write(xmlPath,list):
    print("strings.xml文件路径为：[{0}]".format(xmlPath))
    # 若strings.xml文件存在，先移除
    if os.path.exists(xmlPath) and os.path.isfile(xmlPath):
        os.remove(xmlPath)
    # 在内存中创建一个空的文档
    doc = Dom.Document()
    # 创建一个根节点Managers对象
    root = doc.createElement('resources')
    # 将根节点添加到文档对象中
    doc.appendChild(root)
    for item in list:
        strlist = item.split(_item_split_str) # 用分隔符分割str字符串，並保存到列表
        print("正在构建item节点：",strlist)
        # 仅当列表长度可以被分割成键，值时，认为时有效的item，否则直接不处理
        if len(strlist) == 2:
            # 创建string标签对
            tempAttrib = strlist[0].replace(" ","")
            nodeString = doc.createElement('string')
            nodeString.setAttribute('name',tempAttrib)
            nodeString.appendChild(doc.createTextNode(strlist[1]))
            root.appendChild(nodeString)
    # 开始写xml文档
    fp = open(xmlPath, 'w', encoding="utf-8")
    doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
    fp.close()

# 读取txt文件文本内容
def readTxtFile(file_path):
     # 若txt文件存在,才读取，否则返回null
     if os.path.exists(file_path) and os.path.isfile(file_path):
        f = open(file_path, mode="r", encoding="utf-8")
        texts = []
        for line in f:
            texts.append(line.strip())
        print(texts)
        return ''.join(texts)


# 修改字符串指定位置的值，返回新的字符串
def replace_char(str,ch,index):
    strs = list(str)
    strs[index] = ch
    return ''.join(strs)

# 采用双指针，从后往前，选择性移除空格
# 移除空格条件：
# 1. firstIndex指针往前移动，直到firstIndex指针指向'@'符号
# 2. secondIndex从firstIndex指针下一位置处继续往前移动，直到下一个'@'符号出现，移动期间，将这之间的空格字符串的下标记录在一个下标数组内
# 3. 下一个'@'符号出现时，判断如果这之间出现的字符串只有空格，#，*三种符号，则循环下标数组，移除字符串对应下标的元素
# 4. 如果这之间出现了其他字符串，则清空下标数组内，secondIndex = secondIndex - 1；firstIndex = secondIndex；进入步骤一
def replaceStr(str):
    strs = list(str)
    print(strs)
    size = len(strs)
    print("replaceStr size : ", size)
    indexs = []
    for firstIndex in range(size-1,-1,-1):
        # 当出现第一个@符号后
        if strs[firstIndex] == '@':
            secondIndex = firstIndex - 1
            tempIndexs = []
            isOnlySplitCh = True
            for secondIndex in range(secondIndex,-1,-1):
                # 当出现第二个@符号后
                if strs[secondIndex] == '@':
                    secondIndex = secondIndex - 1
                    firstIndex = secondIndex
                    break
                # 第一个@到第二个@之间出现空格及分隔符之外的其他字符
                if strs[secondIndex] != ' ' and strs[secondIndex] != '#' and strs[secondIndex] != '*':
                    isOnlySplitCh = False
                    secondIndex = secondIndex - 1
                    firstIndex = secondIndex
                    break

                # 第一个@到第二个@之间出现了空格，将空格下标保存到临时数组
                if strs[secondIndex] == ' ':
                    tempIndexs.append(secondIndex)

            if isOnlySplitCh:
                indexs = indexs + tempIndexs

    print(indexs)

    for index in range(len(indexs)):
        strs.pop(indexs[index])

    return ''.join(strs)


# 生成繁体翻译文件
def createFTXml():
    # 1. 生成翻译翻译文件夹
    HKDir = os.path.join(_resPath,_rHKName)
    TWDir = os.path.join(_resPath,_rTWName)
    print("准备创建HK繁体文件夹 ： ",HKDir)
    mkdir(HKDir)
    print("创建HK繁体文件夹完成")
    print("准备创建TW繁体文件夹 ： ",TWDir)
    mkdir(TWDir)
    print("创建TW繁体文件夹完成")

    #读取翻译后的txt文件
    print("正在读取翻译后文件。。。")
    _ftText = readTxtFile(_rTempFTFile)
    print("翻译后的文件：",_ftText)
    print("翻译后的文件读取完成")

    # 翻译后的文件，可能出现分隔符被破坏的情况，例如分隔符中间出现了空格，这时候需要将这类空格移除
    _ftText = replaceStr(_ftText)

    # 按格式拆分翻译后的文件成多个Item
    itemList = _ftText.split(_item_end_str)

    # 构建繁体中文HK翻译文件
    HKPath = os.path.join(HKDir,_fileName)
    write(HKPath,itemList)

    # 构建繁体中文TW翻译文件
    TWPath = os.path.join(TWDir,_fileName)
    write(TWPath,itemList)


# 当前脚本执行流程简介：
# 开发人员运行脚本 python python/LanguageExtract.py 指定的res文件夹路径(例如：D:\project\workspace\tvtWorkSpace\NVMS2.1.x\NVMS_3.0.1\f-tvt-base\src\main\res)
# 通过脚本方式，自动提取指定Module中的res下的value-zh-rCN下的strings.xml文件的所有值，输出到一个res/tempFile/jt.txt文件中，Terminal等待用户确认
# 开发人员将res/tempFile/jt.txt的内容丢到网页翻译，简体->繁体
# 开发人员将翻译后的结果，复制回res/tempFile/ft.txt文件中
# 开发人员在Terminal中输入yes，确定已将翻译后的内容复制到ft.txt中
# 脚本自动根据res/tempFile/ft.txt的内容，创建values-zh-rTW和values-zh-rHK文件夹，并创建文件夹下的strings.xml文件
# 脚本根据res/tempFile/ft.txt的内容，自动在strings.xml创建string标签对，生成繁体语种标签


# 翻译文件的名称
_fileName = 'strings.xml'
# 中文翻译
_rCNName = 'values-zh-rCN'
# 中文繁体(台湾)翻译
_rTWName = 'values-zh-rTW'
# 中文繁体(香港)翻译
_rHKName = 'values-zh-rHK'
# 临时创建的文件夹，主要用于临时存放操作文件
_rTempDir = 'tempFile'
# 翻译前的带有格式的中文简体文本
_rTempJTFile = 'jt.txt'
# 翻译后的带有格式的中文繁体文本
_rTempFTFile = 'ft.txt'
# 分隔符
_item_split_str = '@**@'
# 结束符
_item_end_str = '@##@'

# 获取命令行入参
# 指定Module中的res的全路径
_resPath = sys.argv[1]
print (_resPath)

# 中文翻译文件夹全路径(xxx/res/value-zh-rCN)
_rCNABSPath = os.path.join(_resPath,_rCNName)
print (_rCNABSPath)

# 中文翻译文件全路径（xxx/value-zh-rCN/strings.xml）
_rCNStringsABSPath = os.path.join(_rCNABSPath,_fileName)
print (_rCNStringsABSPath)

#创建临时文件夹
path = os.path.join(_resPath,_rTempDir)
mkdir(path)
print (path)

# 构建临时文件路径
# 有格式的简体中文文件路径
_rTempJTFile = os.path.join(path,_rTempJTFile)
# 有格式的繁体中文文件路径
_rTempFTFile = os.path.join(path,_rTempFTFile)

# 获取strings.xml根节点
print (_rCNStringsABSPath)
tree = ET.ElementTree(file = _rCNStringsABSPath)
root = tree.getroot()

attribAndTextStrList = []

for child in root:
    print (child.attrib)
    print (child.text)
    # 拼接属性字段
    attribAndTextStrList.append(child.attrib['name'])
    # 拼接属性和值的连接符
    attribAndTextStrList.append(_item_split_str)
    # 拼接属性值
    attribAndTextStrList.append(child.text)
    # 拼接属性结束符
    attribAndTextStrList.append(_item_end_str)


# 得到有格式的xml属性和属性值的字符串
attribAndTextStr = ''.join(attribAndTextStrList)
print(attribAndTextStr)

# 创建简体中临时文件，将有格式的xml属性和属性值的字符串写入到临时文件中
create_text(_rTempJTFile,attribAndTextStr)

# 创建繁体中临时文件
create_text(_rTempFTFile,'')



# 循环等待用户输入手动翻译结果
ret = True
while ret:
    # 等待用户确认已完成手动翻译，并且已经将翻译结果填充到了ft.txt内
    inputStr = input("Please confirm whether manual translation has been completed (yes/quit?)")
    if inputStr == 'yes':
        # 结束循环标志
        ret = False
        if checkFileEmpty(_rTempFTFile):
            print('翻译后的临时文件是空的')
            # 手动翻译操作未完成，继续循环等待
            ret = True
        else:
            print('翻译后的临时文件不是空的')
            print('正在为您生成繁体翻译文件，请稍后。。。')
            # 准备将翻译后的文件生成繁体xml文件
            createFTXml()
            print('繁体翻译文件已生成完成!')

            # 构建翻译文件完成后，删除临时文件夹
            shutil.rmtree(path)

    elif inputStr == 'quit':
        ret = False
        print('输入quit,结束执行')





