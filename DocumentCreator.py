import os 

number = []
for i in range(1,41):
    if i in range(1,10):
        number.append('0'+'{}'.format(i))
    else:
        number.append('{}'.format(i))

for i in number:
    os.makedirs('./images/test'+'/'+ 'Action_'+i)#create 40 class (action) document in the test document
    os.makedirs('./images/train'+'/'+ 'Action_'+i)#create 40 class (action) document in the train document
