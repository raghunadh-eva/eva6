Session4 : PART2:

I tried applying the concepts explained in the class. I have three blocks in my network. Since the #params were constrained I restricted the max number of channels used in convolution is 32.

Block3:



​    self.conv3 = nn.Sequential(

​      nn.Conv2d(32, 20, 1),

​      **nn.ReLU(),** - **<u>This is the stupid blunder I did again, to use ReLU() at the output of last layer</u>**

​      nn.AvgPool2d(7)

​    )

​    self.fc = nn.Sequential(

​      nn.Linear(20, 10)

​    )



**<u>Re-written blocks:</u>**



Block1: Use 16 channels instead of 32 and extract more features in block1 instead of single 32channel convolution

 self.conv1 = nn.Sequential(

​      nn.Conv2d(1, 16, 3, padding =1),

​      nn.ReLU(),

​      nn.BatchNorm2d(16),

​      nn.Dropout2d(0.05),

​      nn.Conv2d(16, 16, 3, padding =1),

​      nn.ReLU(),

​      nn.BatchNorm2d(16),

​      nn.Dropout2d(0.05),

​      nn.Conv2d(16, 16, 3, padding =1),

​      nn.ReLU(),

​      nn.BatchNorm2d(16),

​      nn.Dropout2d(0.05),

​      nn.MaxPool2d(2, 2)

​      \##Dont use dropoout in first pass

​    )

​    BLOCK2: Extend the same logic and to block2 as well block3 as well

​    self.conv2 = nn.Sequential(

​      nn.Conv2d(16, 16, 3, padding =1),

​      nn.ReLU(),

​      nn.Dropout2d(0.05),

​      nn.BatchNorm2d(16),

​      nn.Conv2d(16, 16, 3, padding =1),

​      nn.ReLU(),

​      nn.BatchNorm2d(16),

​      nn.Dropout2d(0.05),

​      nn.Conv2d(16, 16, 3, padding =1),

​      nn.ReLU(),

​      nn.BatchNorm2d(16),

​      nn.MaxPool2d(2, 2)

​    )

​    \#7x7x32 --> #7x7x32

​    \#Global average pooling

​    self.conv3 = nn.Sequential(

​      nn.Conv2d(16, 16, 3, padding =1),

​      nn.ReLU(),

​      nn.BatchNorm2d(16),

​      nn.Conv2d(16, 16, 3, padding =1),

​      nn.ReLU(),

​      nn.BatchNorm2d(16),

​      nn.Conv2d(16, 16, 3, padding =1),

​      nn.AvgPool2d(7)

​    )

​    \#7x7x10

​    self.fc = nn.Sequential(

​      nn.Linear(16, 10)

​    )

Changes observed with and without dropout - 

If I don't use dropout, the model learns fast  for the train data in the first 5 epochs and the the gap between the train accuracy and test accuracy keeps widening. With dropout, I have lower train accuracy vs test in the same first few epochs and as training accuracy improves over epochs test does converge and follow it and in the end resulting in similar accuracy

Accuracy : Epoch19

Train set: Average loss: 832.7743, Accuracy: 59731/60000 (99.6%)  

Test set: Average loss: 0.0162, Accuracy: 9945/10000 (99.5%)

##No of parameters



