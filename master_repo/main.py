#!/usr/bin/env python

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import matplotlib.pyplot as plt
import numpy as np
import albumentations as A
import cv2
from torchsummary import summary
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.utils as utils
import albumentations.pytorch as Apy
import tqdm as tqdm
import torch.optim.lr_scheduler as StepLR

from models import *
from utils import *

import argparse

parser = argparse.ArgumentParser(description='Call the main the function with arguments to perform tranining/validation')
parser.add_argument("-d", "--dataset", help='specify the dataset to be used, MNIST,CIFAR10.',required=True)
parser.add_argument("-b", "--batch_size", type=int, help="specify the batch_size to be used. default: 64",default=64)
parser.add_argument("-e", "--epochs", type=int, help="specify the epochs to be used. default: 1",default=1)
parser.add_argument("-m","--model" , help="Specify the model to use. default=resnet18",default="resnet18")
parser.add_argument("-opt","--optimizer" , help="Specify the optimizer to use. Specify the short names. default=SGD",default="SGD")
parser.add_argument("-sch","--scheduler" , help="Specify the scheduler to use. Specify the short names. default=StepLR",default="StepLR")
parser.add_argument("-num_images","--num_images_gradcam" ,type =int, help="Specify the num of images to apply gradcam in. default=10",default=10)

args = parser.parse_args()

if args.dataset == "CIFAR10":
    mean = [0.4914 , 0.4822 , 0.4465]

    std = [0.247 , 0.2435 , 0.2616]

    classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

    h = 32
    w = 32

elif args.dataset == "MNIST":
    print("MNIST data")
else:
    raise Exception("The dataset provided is not supported")

test_transforms  = transforms.Compose([
                                        transforms.ToTensor(),
                                        transforms.Normalize((mean[0],mean[1],mean[2]), (std[0],std[1],std[2]))
                                     ])

train_transforms  = transforms.Compose([
                                        transforms.ToTensor(),
                                        transforms.Normalize((mean[0],mean[1],mean[2]), (std[0],std[1],std[2]))
                                      ])
train_transforms_a = A.Compose([
                                A.Normalize(mean=(mean[0], mean[1], mean[2]), std=(std[0], std[1], std[2])),
                                A.Sequential([
                                    A.PadIfNeeded(
                                        min_height=h+4,
                                        min_width=w+4,
                                        border_mode=cv2.BORDER_CONSTANT,
                                        value=(mean[0],mean[1],mean[2])
                                        ),
                                        A.RandomCrop(
                                        height=h,
                                        width=w
                                        )
                                ], p = 0.5),
                     #A.Cutout(num_holes=1,max_h_size=16,max_w_size=16,fill_value=(0.4914,0.4822,0.4465))
                     A.CoarseDropout(max_holes=1,max_height=16,max_width=16,min_holes=1,min_height=16,min_width=16,fill_value=(mean[0], mean[1], mean[2]),mask_fill_value=None),
                     Apy.ToTensorV2()
                     ])

if args.dataset == 'CIFAR10':
    train = data_albumentations_cifar10(root='./data',train=True,download=True, transform=train_transforms_a)
    test =  datasets.CIFAR10('./data', train=False, download=True, transform=test_transforms)

elif args.dataset == 'MNIST':
    print("place holder for mnist data")
else:
    raise Exception("The dataset provided is not supported")

SEED = 1

#what happens when SEED = 2 ?
torch.manual_seed(SEED)

cuda = torch.cuda.is_available()
print('CUDA Available?',cuda)

if cuda:
    torch.cuda.manual_seed(SEED)

device = torch.device("cuda" if cuda else "cpu")
print(device)

if args.model == "resnet18":
    model = ResNet18().to(device)

if args.dataset == "CIFAR10":
    summary(model, input_size=(3, 32, 32))

if args.optimizer == 'SGD':
    optimizer = optim.SGD(model.parameters(), lr=0.02, momentum=0.9)
else:
    raise Exception("The specified optimizer doesnt exist")

if args.scheduler == 'StepLR':
    scheduler = optim.lr_scheduler.StepLR(optimizer,step_size=20, gamma=0.7)
elif args.scheduler == 'ROP':
    scheduler = optim.lr_scheduler.StepLR(optimizer,step_size=20, gamma=0.7)
else :
    raise Exception("The specified scheduler doesnt exist")

dataloader_args = dict(shuffle=True, batch_size=args.batch_size, num_workers=2, pin_memory=True) if cuda else dict(shuffle=True, batch_size=64)
#Why change batch_size for CPU - since it should not matter

train_loader = torch.utils.data.DataLoader(train, **dataloader_args)

test_loader  = torch.utils.data.DataLoader(test, **dataloader_args)

loss_function = nn.CrossEntropyLoss()

print("No of EPOCHS:",args.epochs)

for epoch in range(args.epochs):
    print('Epoch {}, lr {}'.format(epoch, optimizer.param_groups[0]['lr']))

    train(model, device, train_loader, optimizer, epoch)
    scheduler.step()
    test_losses, test_acc, test_fail_data, test_fail_target, test_pred_target = test(model, device, test_loader)

show_test_validation_plots(test_losses,test_acc,args.epochs)

show_images(test_fail_data,test_fail_target,test_pred_target,args.num_images)

gradCAM(model,device,test_loader,args.num_images)
