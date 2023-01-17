import numpy as np
import os
import matplotlib.pyplot as plt
from PIL import Image

############### get all the name#######################
def get_filename(path):
    name=[]
    for root,dirs,files in os.walk(path):
        for i in files:
            name.append(i) 
    return name

##################the fonction to rescale the image####
def scale(im, nR, nC):
    number_rows = len(im)     # source number of rows 
    number_columns = len(im[0])  # source number of columns 
    return [[ im[int(number_rows * r / nR)][int(number_columns * c / nC)]  
                 for c in range(nC)] for r in range(nR)]

#######################################################


for name in get_filename(os.path.abspath('E:\\nturgbd_skeletons_s001_to_s017\\nturgb+d_skeletons')):# read all the files skeleton
    print(name)

    with open(r".\nturgb+d_skeletons\%s" % (name),"r") as f:#open file skeleton
        data_raw = f.readlines()

    name = name.strip('.skeleton')# delete the filename suffix

    ######create a list of number like : 00 01 02 03 04 ...... 40  ################
    number = []
    for i in range(1,41):
        if i in range(1,10):
            number.append('0'+'{}'.format(i))
        else:
            number.append('{}'.format(i))
    ####################################################################################
    
    if name[-2:] in number:#only read the first 40 actions

        ########################convert the data into list of numbers list(list(line) for line in data)###############
        data = []
        data_1 = [line.strip('\n').split(' ') for line in data_raw]  # delete the '\n' in each line and split each number in a line by space
        for line in range(len(data_1)):
            data.append(np.array(data_1[line]).astype(np.float64).tolist())  # convert string to float line by line for the skeleton file
        ################################################################################################################
        
        
        #################################### calculate the matrix of image#################################################    
        
        frame_r = []# a list of 2 dimension to store the red color values in the frames line by line
        frame_g = []# a list of 2 dimension to store the green color values in the frames line by line
        frame_b = []# a list of 2 dimension to store the blue color values in the frames line by line
        nb_frames = 0#this variable is to count the frame number in a file
        for l in range(len(data)):
            if data[l][0] == 25:  #every fram begins by a line of single number '25', so we set it up as a signal to read a new frame, in this way, we can skip those unwanted lines in the files
                nb_frames+=1 #counter of number of frames in a skeleton file
                frame = []         
                for f in range(l+1,l+26):# read the following 25 lines after the line of single value '25'
                    frame.append(data[f])
                x = [row[0] for row in frame]# read the first colon of a frame and store it in x as a line
                y = [row[1] for row in frame]
                z = [row[2] for row in frame]

                diff_x = max(x)-min(x)
                diff_y = max(y)-min(y)
                diff_z = max(z)-min(z)
                min_x = min(x)
                min_y = min(y)
                min_z = min(z)

                r,g,b=[],[],[]
                for i in range(len(x)):
                    r.append(255*(x[i]-min_x)/diff_x)
                    g.append(255*(y[i]-min_y)/diff_y)
                    b.append(255*(z[i]-min_z)/diff_z)
                frame_r.append(r)# add the red color values of the frames line by line 
                frame_g.append(g)
                frame_b.append(b)
            else: pass#skip the unwanted lines in the files
        image = np.ones((25,nb_frames,3),dtype=np.uint8)          # initialize the image of BGR
        image[:,:,0] = np.array(frame_r).T #store the red color informations as the first layer of the image matrix 
        image[:,:,1] = np.array(frame_g).T
        image[:,:,2] = np.array(frame_b).T
        #################################################################################################

        try: 
            res = np.array(scale(image, 55, 55))#call scale fonction to reshape the image
            im = Image.fromarray(res)#call the PIL.Image module
            if name[10:12] in ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20']: #seperate the first 20 subjects as the training dataset
                image_path = './images/'+'train/'+'Action_'+'%s' %(name[-2:])+'/%s' %(name)+'.jpeg'
                im.save(f"{image_path}")#store the images in 40 classes (action) in the document of 'train'
            else: # seperate the other 20 subjects as the test dataset
                image_path = './images/'+'test/'+'Action_'+'%s' %(name[-2:])+'/%s' %(name)+'.jpeg'
                im.save(f"{image_path}")#store the images in 40 classes (action) in the document of 'test'
        
        except IndexError:# when we met the empty file, previous reading frame algrithme would not word and the the program would report an 'IndexError'. If this occures, skip it!
         continue