# xml Parsing package 
import xml.etree.ElementTree as ET
import pickle
import os
# os.listdir()  Method to return a list of the names of the files or folders contained in the specified folder 
from os import listdir, getcwd
from os.path import join
import cv2
from glob import glob
import shutil


sets = ['train','test']
classes = ["registration_plate"]  ## Change to your own category  #  Category of self training 

images = r"./images"
#  Perform the normalization operation 
def convert(size, box): # size:( Original picture w, Original picture h) , box:(xmin,xmax,ymin,ymax)
    dw = 1./size[0]     # 1/w
    dh = 1./size[1]     # 1/h
    x = (box[0] + box[1])/2.0   #  The center point of the object in the figure x coordinate 
    y = (box[2] + box[3])/2.0   #  The center point of the object in the figure y coordinate 
    w = box[1] - box[0]         #  The actual pixel width of the object 
    h = box[3] - box[2]         #  The actual pixel height of the object 
    x = x*dw    #  The center point of the object x Coordinate ratio of ( amount to  x/ Original picture w)
    w = w*dw    #  The width ratio of the object width ( amount to  w/ Original picture w)
    y = y*dh    #  The center point of the object y Coordinate ratio of ( amount to  y/ Original picture h)
    h = h*dh    #  The width ratio of the object width ( amount to  h/ Original picture h)
    return (x, y, w, h)    #  return   Relative to the center point of the object in the original drawing x Coordinate ratio ,y Coordinate ratio , Width ratio , Height ratio , Value range [0-1]


# year ='2012',  Corresponding to the id（ file name ）
def convert_annotation(image_id):
    #  The corresponding passage year  Find the appropriate folder , And open the corresponding image_id Of xml file , Its corresponding bund file 
    in_file = open('./Image sets/%s.xml' % (image_id), encoding='utf-8')
    # print(in_file.name)
    #  Prepare in the corresponding image_id  Write the corresponding label, Respectively 
    # <object-class> <x> <y> <width> <height>
    out_file = open('./labels/%s.txt' % (image_id), 'w', encoding='utf-8')
    # print(out_file.name)
    #  analysis xml file 
    tree = ET.parse(in_file)
    #  Get the corresponding key value pair 
    root = tree.getroot()
    #  Get the size of the picture 
    # size = root.find('size')
    # #  Gain width 
    # w = int(size.find('width').text)
    # #  Get high 
    # h = int(size.find('height').text)
    # print("Image sets" + "/" + image_id + '.jpg')

    img = cv2.imread("Image sets" + "/" + image_id + '.jpg')
    w = int(img.shape[1])
    h = int(img.shape[0])

    # #  Traverse the target obj
    for obj in root.iter('object'):
        cls = obj.find('name').text
        # if cls = waterweeds
        if cls not in classes == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(
            str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


#  Return to the current working directory 
wd = getcwd()
print(wd)


for image_set in sets:
    #  Look for the labels If the folder does not exist, create 
    if not os.path.exists('./labels/'):
        os.makedirs('./labels/')
        
    try:
        os.makedirs('./labels/test')
    except:pass
    
    try:
        os.makedirs('./labels/train')
    except:pass

    # For test set
    image_ids = list()
    for img in glob('Image sets/%s/*.jpg'%image_set):
        img = '%s/'%image_set + img.split('/')[-1].split('.')[0]
        image_ids.append(img)
        
    list_file = open('./%s.txt' % (image_set), 'w')
    #  The corresponding file _id And write in the full path and wrap 
    for image_id in image_ids:
        list_file.write('datasets/images/%s.jpg\n' % (image_id.split('/')[1]))
        #  call   year =  year   image_id =  Corresponding file name _id
        convert_annotation(image_id)
    #  Close file 
    list_file.close()
    
    
# for img in glob('Image sets/train/*.jpg'):
#     shutil.copy(img,'labels/train/')
    
# for img in glob('Image sets/test/*.jpg'):
#     shutil.copy(img,'labels/test/')