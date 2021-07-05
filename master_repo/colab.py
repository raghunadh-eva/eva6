%cd /content

!git clone https://github.com/raghunadh-eva/eva6.git

%cd ./eva6

!git pull

%cd ../

#parser = argparse.ArgumentParser(description='Call the main the function with arguments to perform tranining/validation')
#parser.add_argument("-d", "--dataset", help='specify the dataset to be used, MNIST,CIFAR10')
#parser.add_argument("-b", "--batch_size", type=int, help="specify the batch_size to be used. default: 64",default=64)
#parser.add_argument("-e", "--epochs", type=int, help="specify the epochs to be used. default: 1",default=1)
#parser.add_argument("-drop","--dropout_perc", type=float, help="specify the dropout perc to be used. default: 0.05",default=0.05)
#parser.add_argument("-opt","--optimizer" , help="Specify the optimizer to use. Specify the short names. default=SGD",default="SGD")
#parser.add_argument("-sch","--scheduler" , help="Specify the scheduler to use. Specify the short names. default=StepLR",default="StepLR")
#args = parser.parse_args()
#return args.d,args.b

!pip install torchsummary
!pip install -U albumentations
%matplotlib inline

from torchsummary import summary
from __future__ import print_function
from torchvision import datasets, transforms, utils
from torch.optim.lr_scheduler import StepLR
from tqdm import tqdm
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision

import matplotlib.pyplot as plt
import numpy as np
import albumentations as A
import cv2

#from eva6.master_repo import models as m
#from eva6.master_repo import utils as utils
from eva6.master_repo import main


h = 32 ; #image height
w = 32 ; #image width


dropout_perc  = 0.05


EPOCHS = 20

test_losses = []
test_acc = []

for epoch in range(EPOCHS):
  main.train(main.model, device, train_loader, optimizer, epoch)
  scheduler.step()
  test_losses, test_acc, test_fail_data, test_fail_target, test_pred_target = test(model, device, test_loader)

show_test_validation_plots(test_losses,test_acc,EPOCHS)

show_images(test_fail_data,test_fail_target,test_pred_target,mean,std_dev,n)
