#!/usr/bin/env python3

import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import matplotlib.pyplot as plt
import numpy as np
import albumentations as A
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.utils as utils
import albumentations.pytorch as Apy
import torch.optim.lr_scheduler as StepLR
from torchvision.utils import save_image

from torchsummary import summary
from torch_lr_finder import LRFinder
from tqdm import tqdm
from models import *
from utils import *

import argparse

parser = argparse.ArgumentParser(description='Call the main the function with arguments to perform tranining/validation')
parser.add_argument("-d", "--dataset", help='specify the dataset to be used, MNIST,CIFAR10.',required=True)
parser.add_argument("-b", "--batch_size", type=int, help="specify the batch_size to be used. default: 128",default=128)
parser.add_argument("-e", "--epochs", type=int, help="specify the epochs to be used. default: 1",default=1)
parser.add_argument("-m","--model" , help="Specify the model to use. default=resnet18",default="resnet18")
parser.add_argument("-opt","--optimizer" , help="Specify the optimizer to use. Specify the short names. default=SGD",default="SGD")
parser.add_argument("-sch","--scheduler" , help="Specify the scheduler to use. Specify the short names. default=StepLR",default="StepLR")
parser.add_argument("-num_images","--num_images_gradcam" ,type =int, help="Specify the num of images to apply gradcam in. default=10",default=10)
parser.add_argument("-gcam","--grad_cam" ,help="Specify when you need to generate gcam output", action="store_true")
parser.add_argument("-s","--eva_session" ,type=int ,help="Specify the assignment key", required=True)
parser.add_argument("-lr","--lr_value" ,type=float, help="The Learning rate to start with",default=0.02)
parser.add_argument("-find_lr","--lr_finder" , help="Find the LR", action="store_true")
parser.add_argument("-lr_type","--lr_finder_type" , help="Specify the lr increase type. exp/linear", default="")

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
if args.eva_session == 9:
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
                                A.HorizontalFlip(),
                                A.CoarseDropout(max_holes=1,max_height=8,max_width=8,min_holes=1,min_height=8,min_width=8,fill_value=(mean[0], mean[1], mean[2]),mask_fill_value=None),
                                Apy.ToTensorV2()
                        ])
else:
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
                                A.Rotate(limit=5,border_mode=cv2.BORDER_CONSTANT, value=(mean[0],mean[1],mean[2]),p=0.5),
                     #A.Cutout(num_holes=1,max_h_size=16,max_w_size=16,fill_value=(0.4914,0.4822,0.4465))
                     A.CoarseDropout(max_holes=1,max_height=16,max_width=16,min_holes=1,min_height=16,min_width=16,fill_value=(mean[0], mean[1], mean[2]),mask_fill_value=None),
                     Apy.ToTensorV2()
                     ])

if args.dataset == 'CIFAR10':
    train_data = data_albumentations_cifar10(root='./data',train=True,download=True, transform=train_transforms_a)
    test_data =  datasets.CIFAR10('./data', train=False, download=True, transform=test_transforms)

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
elif args.model == "resnet18_ln":
    model = ResNet18_ln().to(device)
elif args.model == "custom_resnet":
    model = ResNetCustomS9().to(device)
else:
    raise Exception("The input model type is not supported")

if args.dataset == "CIFAR10":
    summary(model, input_size=(3, 32, 32))
elif args.dataset == "MNIST":
    print('MNIST DATA')
else:
    raise Exception("The input dataset is not supported")

if args.optimizer == 'SGD':
    optimizer = optim.SGD(model.parameters(), lr=args.lr_value, momentum=0.9)
else:
    raise Exception("The specified optimizer doesnt exist")

dataloader_args = dict(shuffle=True, batch_size=args.batch_size, num_workers=2, pin_memory=True) if cuda else dict(shuffle=True, batch_size=64)
#Why change batch_size for CPU - since it should not matter

train_loader = torch.utils.data.DataLoader(train_data, **dataloader_args)

test_loader  = torch.utils.data.DataLoader(test_data, **dataloader_args)

loss_function = nn.CrossEntropyLoss()

print("No of EPOCHS:",args.epochs)

test_losses = []
test_acc = []
total_train_loss = 0

if args.lr_finder:
    if args.lr_finder_type == "exp" or args.lr_finder_type == "linear":
        lr_finder = LRFinder(model, optimizer, loss_function, device=device)
        #lr_finder.range_test(train_loader, end_lr=100, num_iter=100)
        lr_finder.range_test(train_loader, val_loader=test_loader, end_lr=100, num_iter=12288, step_mode=args.lr_finder_type)
        lr_finder.plot(log_lr=False)
        lr_finder.plot() # to inspect the loss-learning rate graph
        lr_finder.reset()
    else:
        raise Exception("Unknown lr step_mode type")

else:
    if args.scheduler == 'StepLR':
        scheduler = optim.lr_scheduler.StepLR(optimizer,step_size=20, gamma=0.7)
    elif args.scheduler == 'ROP':
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5, factor=0.7, verbose=True)
    else :
        raise Exception("The specified scheduler doesnt exist")

    for epoch in range(args.epochs):
        print('Epoch {}, lr {}'.format(epoch, optimizer.param_groups[0]['lr']))

        loss = train(model, device, train_loader, optimizer,loss_function)
        if args.scheduler == 'ROP':
            total_train_loss += loss
            scheduler.step(total_train_loss)
        else:
            scheduler.step()
            test_losses, test_acc, test_fail_data, test_fail_target, test_pred_target = test(model, device, test_loader,test_losses,test_acc)

    show_test_validation_plots(test_losses,test_acc,args.epochs)

    show_images(test_fail_data,test_fail_target,test_pred_target,args.num_images_gradcam)

if args.grad_cam:
    gradCAM(model,device,test_loader,args.num_images_gradcam)
