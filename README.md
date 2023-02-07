# Recognation-of-Humain-Movements by Deep learning
I have used the dataset NTU RGB +D to recognize the humain movements.

The goal of this project is to recognize human actions by computer vision. For this we will use the NTU RGB+D dataset and we will perform learning and predictions using pre-trained convolutional neural networks on the ImageNet dataset.

## Transform the time series movement data into RGB images
The data we used was uploaded to the NTU RGB+D GitHub which contains 56,880 actions in the form of RGB videos, 3D skeleton files and infrared videos. Here we have focused on processing .SKELETON files which contain the position in space of 25 joints of the skeleton for each frame. Each filename in the dataset is in the format SsssCcccPpppRrrrAaaa (for example, S001C002P003R002A013), where 'sss' is the configuration number, 'ccc' is the camera ID, 'ppp' is the ID interpreter (subject), 'rrr' is the replication number (1 or 2), and 'aaa' is the action class label.
![image](https://user-images.githubusercontent.com/105889748/216825905-6edce1fe-8bed-4cd2-b1ad-26c12fabbd9e.png)
The figure shows the position of the 25 joints along the X, Y and Z axes for a frame. Each axis is associated with a red color for X, green for Y and blue for Z according to the figure below:
![image](https://user-images.githubusercontent.com/105889748/216825978-9ba1d3d3-77da-49e8-a02d-f3a51237e039.png)
the x coordinate of joint i at frame f, max(X) the maximum value of X at this frame and min(X) the minimum value of X at this frame.

Using this algorithm, one can transform the coordinates of the joints into an RGB image that the rows correspond to the joints and the columns correspond to the frames. For example, the file S001C001P001R001A001.skeleton contains 103 frames, we can output an image with dimension 25*103*3:

![image](https://user-images.githubusercontent.com/105889748/216826824-c0e8a279-3dd6-4416-be6a-86df133cafb2.png)

Once we get the RGB image, we need to resize it into a square in order to feed into the neural network model in the later step. We have chosen the 55*55*3 dimension for all the images so we have to stretch the rows and crush the original image columns. To do this, we gave back the indexes for the rows and the columns.

We obtain the resized image with the size of 55*55*3.

![image](https://user-images.githubusercontent.com/105889748/216826911-7ec61f41-7add-4426-b0e7-4fb9510705c0.png)

## Recognition of the movements by convelitional neural networks
