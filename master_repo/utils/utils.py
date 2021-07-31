# -*- coding: utf-8 -*-
"""utils.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gOTzuQWFeMG5YVojJmHeHeClan5HzyyR
"""
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
import torch.optim.lr_scheduler as StepLR
from tqdm import tqdm

from torchvision.utils import save_image


def get_data_mean_std():

  if args.dataset == "CIFAR10":
      train_nonorm_transforms = transforms.Compose([transforms.ToTensor()])
      test_nonorm_transforms  = transforms.Compose([transforms.ToTensor()])
      dataloader_args = dict(shuffle=True, batch_size=args.batch_size, num_workers=2, pin_memory=True) if cuda else dict(shuffle=True, batch_size=64)
      train_nonorm = datasets.CIFAR10('./data_nonorm', train=True,  download=True, transform=train_nonorm_transforms)
      test_nonorm =  datasets.CIFAR10('./data_nonorm', train=False, download=True, transform=test_nonorm_transforms)
      train_loader_nonorm = torch.utils.data.DataLoader(train_nonorm, **dataloader_args)
      test_loader_nonorm  = torch.utils.data.DataLoader(test_nonorm, **dataloader_args)
      h = 32
      w = 32

  for index, (data,target) in enumerate(train_loader_nonorm):
    chsum += data.sum(dim=(0,2,3),keepdim=True)

  chsum = 0

  mean = chsum / (len(train_nonorm) * h * w)
  train_mean = mean
  chsum = None
  for index, (data,target) in enumerate(train_loader_nonorm):
    if index == 0:
      print(data.min(),data.max())
      chsum = (data - mean).pow(2).sum(dim=(0,2,3),keepdim=True)
    else:
      chsum += (data - mean).pow(2).sum(dim=(0,2,3),keepdim=True)

  train_std = torch.sqrt(chsum/(len(train_nonorm) * h * w))
  #print("Traindata Mean",mean)
  #print("Traindata std dev",std)

  chsum = 0

  for index, (data,target) in enumerate(test_loader_nonorm):
    chsum += data.sum(dim=(0,2,3),keepdim=True)

  mean = chsum / (len(test_nonorm) * h * w)
  test_mean = mean

  chsum = None
  for index, (data,target) in enumerate(test_loader_nonorm):
    if index == 0:
      chsum = (data - mean).pow(2).sum(dim=(0,2,3),keepdim=True)
    else:
      chsum += (data - mean).pow(2).sum(dim=(0,2,3),keepdim=True)

  test_std = torch.sqrt(chsum/(len(test_nonorm) * h * w))

  return train_mean,train_std,test_mean,test_std;

##copied from albumentations.io
cv2.setNumThreads(0)
cv2.ocl.setUseOpenCL(False)

def show_test_validation_plots(test_losses,test_acc,EPOCHS):

  fig, axs = plt.subplots(1, 2)

  axs[0].set_title('Test/Validation Loss Graph')
  axs[0].set_xticks(np.arange(1,EPOCHS+1))

  axs[1].set_title('Test/Validation Accuracy Graph')
  axs[1].set_xticks(np.arange(1,EPOCHS+1))

  axs[0].plot(test_losses)
  axs[1].plot(test_acc)

  plt.show()

def show_images(test_fail_data,test_fail_target,test_pred_target,n):

  test_10_images = []
  for i in range(0,n):
    img_un = unnorm_img(test_fail_data[i])
    test_10_images.append(img_un)

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

  grid = torchvision.utils.make_grid(torch.stack(test_10_images).cpu(), nrow=5)
  plt.imshow(np.transpose(grid, (1,2,0)))
  plt.show()

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
    n = num_images

    for data, target in test_loader:
      data, target = data.to(device), target.to(device)
      output = model(data)
      pred = output.argmax(dim=1, keepdim=True)


      for k,x in enumerate(pred.eq(target.view_as(pred))):

        if not x:
          if num_images <= 0:
            plt.show()
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
          img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
          #tran = transforms.ToTensor()
          plt.subplot(4, n*2/4, counter)
          plt.imshow(img)
          plt.axis('off')
          plt.title("actual: %s\npredicted: %s" % (classes[target[k]], classes [pred[k]]), fontsize=8)
          counter = counter + 1
          plt.subplot(4, n*2/4, counter)
          plt.imshow(gradcam)
          plt.axis('off')
          plt.title("actual: %s\npredicted: %s" % (classes[target[k]], classes [pred[k]]), fontsize=8)
          plt.subplots_adjust(top=6, bottom=4, left=3, right=5)
          num_images = num_images - 1;
      break

class data_albumentations_cifar10(datasets.CIFAR10):
    def __init__(self, root="~/data/", train=True, download=True, transform=None):
        super().__init__(root=root, train=train, download=download, transform=transform)
    def __getitem__(self, index):
        image, label = self.data[index], self.targets[index]
        if self.transform is not None:
            transformed = self.transform(image=image)
            image = transformed["image"]
            return image, label


def train(model, device, train_loader, optimizer,loss_function,scheduler,is_onelr):

  model.train()
  pbar = tqdm(train_loader)

  l1_lamda = 0.0001

  correct = 0
  processed = 0
  for batch_idx, (data, target) in enumerate(pbar):
    # get samples
    data, target = data.to(device), target.to(device)

    # Init
    optimizer.zero_grad()
    # In PyTorch, we need to set the gradients to zero before starting to do backpropragation because PyTorch accumulates the gradients on subsequent backward passes.
    # Because of this, when you start your training loop, ideally you should zero out the gradients so that you do the parameter update correctly.

    # Predict
    y_pred = model(data)

    # Calculate loss
    #Cross entropy loss
    #loss = F.nll_loss(y_pred, target)
    loss = loss_function(y_pred,target,target)
    #

    ##Add L1 Loss
    l1 = 0
    for p in model.parameters():
      p_tensor = torch.sum(torch.abs(p))
      l1 += p_tensor

    loss = loss + l1_lamda * l1

    #train_losses.append(loss)

    # Backpropagation
    loss.backward()
    optimizer.step()
    if is_onelr == "OneLR":
        scheduler.step()
    # Update pbar-tqdm

    pred = y_pred.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
    correct += pred.eq(target.view_as(pred)).sum().item()
    processed += len(data)

    pbar.set_description(desc= f'Loss={loss.item()} Batch_id={batch_idx} Accuracy={100*correct/processed:0.2f}')
    #train_acc.append(100*correct/processed)
  return loss;

def test(model, device, test_loader,test_losses,test_acc):

    test_fail_data = []
    test_fail_target = []
    test_pred_target = []

    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            #print(pred,target.view_as(pred))
            correct += pred.eq(target.view_as(pred)).sum().item()
            for i,x in enumerate(pred.eq(target.view_as(pred))):
              if not x:
                test_fail_data.append(data[i])
                test_fail_target.append(target[i])
                test_pred_target.append(pred[i])
                #print(target[i])

    test_losses.append(test_loss)

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.2f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))

    test_acc.append(100. * correct / len(test_loader.dataset))

    return test_losses, test_acc, test_fail_data, test_fail_target, test_pred_target;
