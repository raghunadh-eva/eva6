Session4 : PART2:

I tried applying the concepts explained in the class. I have three blocks in my network. Since the #params were constrained I restricted the max number of channels used in convolution is 32.

Block3:

Use transition layer to conver 7x7x32 into 7x7x20 (tried 7x7x10) with 1x1x20 convolution

Use the gap layer to to convert into 1d and pass to Fully connected layer

​    self.conv3 = nn.Sequential(

​      nn.Conv2d(32, 20, 1),

​      **nn.ReLU(),** - **<u>This is the stupid blunder I did again, to use ReLU() at the output of last layer</u>**

​      nn.AvgPool2d(7)

​    )

​    \#7x7x10

​    self.fc = nn.Sequential(

​      nn.Linear(20, 10)

​    )



Re-written blocks:

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

​    

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

Accuracy : Epoch19

Train set: Average loss: 832.7743, Accuracy: 59731/60000 (99.6%)  

Test set: Average loss: 0.0162, Accuracy: 9945/10000 (99.5%)

##No of parameters



