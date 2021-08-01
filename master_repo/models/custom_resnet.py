import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import matplotlib.pyplot as plt
import numpy as np
import albumentations as A
import cv2
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.utils as utils
import albumentations.pytorch as ToTensorV2
import tqdm as tqdm

class BasicBlock_c(nn.Module):
    expansion = 1

    def __init__(self, in_planes, planes, stride=1):
        super(BasicBlock_c, self).__init__()
        self.conv1 = nn.Conv2d(
            in_planes, planes, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3,padding=1,
                               stride=stride, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        #self.conv3 = nn.Conv2d(planes, planes, kernel_size=3,padding=1,
        #                       stride=2, bias=False)
        #self.bn3 = nn.BatchNorm2d(planes)


    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = F.relu(self.bn2(self.conv2(out)))
        #out = F.relu(self.bn3(self.conv3(out)))
        return out

class ResNetCustom(nn.Module):
    def __init__(self, block, num_blocks, num_classes=10):
        super(ResNetCustom, self).__init__()

        self.in_planes = 64

        self.conv0  =    nn.Sequential(
                            nn.Conv2d(3, 64, kernel_size=3,stride=1, padding=1, bias=False),
                            nn.BatchNorm2d(64),
                            nn.ReLU(),
                            nn.DropOut(0.05)
                         )

        ##Layer1
        self.conv1 =     nn.Sequential(
                            nn.Conv2d(64,128,kernel_size=3,stride=1,padding=1,bias=False),
                            nn.MaxPool2d(2,2),
                            nn.BatchNorm2d(128),
                            nn.ReLU(),
                            nn.DropOut(0.05)
                         )
        self.layer1 =    self._make_layer(block,64,128, num_blocks[0], stride=2)

        #Layer2
        self.conv2 =     nn.Sequential(
                            nn.Conv2d(128,256,kernel_size=3,stride=1,padding=1,bias=False),
                            nn.MaxPool2d(2,2),
                            nn.BatchNorm2d(256),
                            nn.ReLU(),
                            nn.DropOut(0.05)
                         )

        ##layer3
        self.conv3 =     nn.Sequential(
                            nn.Conv2d(256,512,kernel_size=3,stride=1,padding=1,bias=False),
                            nn.MaxPool2d(2,2),
                            nn.BatchNorm2d(512),
                            nn.ReLU(),
                            nn.DropOut(0.05)
                         )
        self.layer3 =    self._make_layer(block, 256, 512, num_blocks[2], stride=2)

        self.pool1 = nn.MaxPool2d(4,4)

        self.linear = nn.Linear(512*block.expansion, num_classes,bias=False)

        self.softmax = nn.Softmax(dim=-1)

    def _make_layer(self, block, in_planes, planes, num_blocks, stride):
        #strides = [stride] + [1]*(num_blocks-1)
        layers = []
        #for stride in strides:
        self.in_planes = in_planes
        layers.append(block(self.in_planes, planes, stride))
        #self.in_planes = planes * block.expansion
        return nn.Sequential(*layers)

    def forward(self, x):
        out = self.conv0(x)
        out_l1 = self.layer1(out)
        out = self.conv1(out) + out_l1
        out = self.conv2(out)
        out_l3 = self.layer3(out)
        out = self.conv3(out) + out_l3

        out = self.pool1(out)
        out = out.view(out.size(0), -1)

        out = self.linear(out)

        return self.softmax(out)

def ResNetCustomS9():
    return ResNetCustom(BasicBlock_c, [1, 1, 1, 1])
