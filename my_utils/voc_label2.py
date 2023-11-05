import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets = ['train', 'val', 'test']

classes = ["person"]  # 你自己数据集的类别


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_id):
    in_file = open('E:/xgh/yolov7-main/data/mydata/xml/%s.xml' % (image_id))  # 读取xml的路径
    out_file = open('E:/xgh/yolov7-main/data/mydata/labels/%s.txt' % (image_id), 'w')  # 存放label的路径
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        # difficult = obj.find('difficult').text
        cls = obj.find('name').text
        # if cls not in classes or int(difficult) == 1:
        #     continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text),
             float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


wd = getcwd()

for image_set in sets:
    if not os.path.exists('E:/xgh/yolov7-main/data/mydata/labels/'):
        os.makedirs('E:/xgh/yolov7-main/data/mydata/labels/')
    image_ids = open('E:/xgh/yolov7-main/data/mydata/dataSet/%s.txt'
                     % (image_set)).read().strip().split()  # 这里读取的是makeTXT.py划分数据集后的txt

    list_file = open('E:/xgh/yolov7-main/data/mydata/%s.txt' % (image_set), 'w')  # 这里生成了划分后数据集的具体路径，也是后边yaml需要用到的

    for image_id in image_ids:
        list_file.write('E:/xgh/yolov7-main/data/mydata/images/%s.png\n'
                        % (image_id))  # 把你自己数据集的图片的路径写入上一步的txt文件
        convert_annotation(image_id)
    list_file.close()
