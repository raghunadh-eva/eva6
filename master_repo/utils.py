# -*- coding: utf-8 -*-
"""utils.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gOTzuQWFeMG5YVojJmHeHeClan5HzyyR
"""
from torchsummary import summary
from __future__ import print_function
from torchvision import datasets, transforms, utils
from torch.optim.lr_scheduler import StepLR
from tqdm import tqdm
from albumentations.pytorch import ToTensorV2
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import albumentations as A
import cv2

train_nonorm = datasets.CIFAR10('./data_nonorm', train=True,  download=True, transform=train_nonorm_transforms)
test_nonorm =  datasets.CIFAR10('./data_nonorm', train=False, download=True, transform=test_nonorm_transforms)
train_loader_nonorm = torch.utils.data.DataLoader(train_nonorm, **dataloader_args)
test_loader_nonorm  = torch.utils.data.DataLoader(test_nonorm, **dataloader_args)

def get_data_mean_std(train_nonorm,train_loader_nonorm,test_nonorm,test_loader_nonorm,h,w):
  chsum = 0

  for index, (data,target) in enumerate(train_loader_nonorm):
    chsum += data.sum(dim=(0,2,3),keepdim=True)

  mean = chsum / (len(train_nonorm) * h * w)

  chsum = None
  for index, (data,target) in enumerate(train_loader_nonorm):
    if index == 0:
      print(data.min(),data.max())
      chsum = (data - mean).pow(2).sum(dim=(0,2,3),keepdim=True)
    else:
      chsum += (data - mean).pow(2).sum(dim=(0,2,3),keepdim=True)

  std = torch.sqrt(chsum/(len(train_nonorm) * h * w))
  #print("Traindata Mean",mean)
  #print("Traindata std dev",std)

  chsum = 0

  for index, (data,target) in enumerate(test_loader_nonorm):
    chsum += data.sum(dim=(0,2,3),keepdim=True)

  mean = chsum / (len(test_nonorm) * h * w)

  chsum = None
  for index, (data,target) in enumerate(test_loader_nonorm):
    if index == 0:
      chsum = (data - mean).pow(2).sum(dim=(0,2,3),keepdim=True)
    else:
      chsum += (data - mean).pow(2).sum(dim=(0,2,3),keepdim=True)

  std = torch.sqrt(chsum/(len(test_nonorm) * h * w))

  return train_mean,train_std_dev,test_mean,test_std_dev;

##copied from albumentations.io
cv2.setNumThreads(0)
cv2.ocl.setUseOpenCL(False)

class data_albumentations(datasets.CIFAR10):
    def __init__(self, root="~/data/cifar10", train=True, download=True, transform=None):
        super().__init__(root=root, train=train, download=download, transform=transform)

    def __getitem__(self, index):
        image, label = self.data[index], self.targets[index]

        if self.transform is not None:
            transformed = self.transform(image=image)
            image = transformed["image"]

        return image, label

def show_test_validation_plots(test_losses,test_acc,EPOCHS):

  fig, axs = plt.subplots(1, 2)

  axs[0].set_title('Test/Validation Loss Graph')
  axs[0].set_xticks(np.arange(1,EPOCHS+1))

  axs[1].set_title('Test/Validation Accuracy Graph')
  axs[1].set_xticks(np.arange(1,EPOCHS+1))

  axs[0].plot(test_losses)
  axs[1].plot(test_acc)

  plt.imshow()

def show_images(test_fail_data,test_fail_target,test_pred_target,n):

  test_10_images = []
  for i in range(0,n):
    test_10_images.append(test_fail_data[i])

  test_10_images_target = []
  for i in range(0,n):
    test_10_images_target.append(test_fail_target[i])

  test_10_pred_target = []
  for i in range(0,n):
    test_10_pred_target.append(test_pred_target[i])
  #print(test_10_images_target)

  print('Actual Labels')
  print(' '.join('%5s' % classes[test_10_images_target[j]] for j in range(0,n)))
  print('Predicted Labels')
  print(' '.join('%5s' % classes[test_10_pred_target[j]] for j in range(0,n)))

  test_10_images_unnorm = []

  img = unnorm_img(img)

  test_10_images_unnorm.append(img)

  grid = torchvision.utils.make_grid(torch.stack(test_10_images_unnorm).cpu(), nrow=5)
  plt.figure(figsize=(5,5))
  plt.imshow(np.transpose(grid, (1,2,0)))

def unnorm_img(img):
  img = img.cpu()
  img = img.numpy()
  img[0] = img[0] * 0.247 + 0.4914
  img[1] = img[1] * 0.2435 + 0.4822
  img[2] = img[2] * 0.2616 + 0.4465

  img = torch.from_numpy(img)
  return img

classes = ('plane', 'car', 'bird', 'cat','deer', 'dog', 'frog', 'horse', 'ship', 'truck')

def gradCAM(model,device,test_loader,num_images):

    model.eval()

    test_failed_data = []

    counter = 0

    for data, target in test_loader:
      data, target = data.to(device), target.to(device)
      output = model(data)
      pred = output.argmax(dim=1, keepdim=True)


      for k,x in enumerate(pred.eq(target.view_as(pred))):

        if not x:
          if num_images <= 0:
            break
          counter = counter+1
          prediction = output[k][pred[k].unsqueeze(dim=1)]
          prediction = prediction.backward(retain_graph=True)
          gradients = model.get_gradient()
          pooled_gradients = torch.mean(gradients, dim=[0, 2, 3])
          activations = model.get_activations(data[k].unsqueeze(dim=0)).detach()
          for i in range(512):
            activations[:, i, :, :] *= pooled_gradients[i]
          heatmap = torch.mean(activations.cpu(), dim=1).squeeze()
          heatmap = np.maximum(heatmap, 0)
          heatmap /= torch.max(heatmap)
          heatmap = heatmap.numpy()

          img = unnorm_img(data[k])

          save_image(img,'img.jpg')
          img = cv2.imread('./img.jpg')
          heatmap = cv2.resize(heatmap,(img.shape[1],img.shape[0]))
          heatmap = np.uint8(255 * heatmap)
          heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
          superimposed_img = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)
          gradcam = cv2.cvtColor(superimposed_img, cv2.COLOR_BGR2RGB)
          tran = transforms.ToTensor()
          plt.subplot(2, 5, counter)
          plt.imshow(gradcam)
          plt.axis('off')
          plt.title("actual: %s\npredicted: %s" % (classes[target[k]], classes [pred[k]]), fontsize=8)
          plt.subplots_adjust(top=3, bottom=2, left=3, right=5)
          num_images = num_images - 1;
      break
