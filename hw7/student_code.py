# python imports
import os
from tqdm import tqdm

# torch imports
import torch
import torch.nn as nn
import torch.optim as optim

# helper functions for computer vision
import torchvision
import torchvision.transforms as transforms


class LeNet(nn.Module):
    def __init__(self, input_shape=(32, 32), num_classes=100):
        super(LeNet, self).__init__()
        self.a = nn.Conv2d(in_channels=3, out_channels=6, kernel_size=5, stride=1, padding=0, bias=True)
        self.b = nn.ReLU()
        self.c = nn.MaxPool2d(kernel_size=2, stride=2)
        self.d = nn.Conv2d(in_channels=6, out_channels=16, kernel_size=5, stride=1, padding=0, bias=True)
        self.e = nn.ReLU()
        self.f = nn.MaxPool2d(kernel_size=2, stride=2)
        self.g = nn.Flatten()
        self.h = nn.Linear(16*5*5,256, bias=True)
        self.i = nn.ReLU()
        self.j = nn.Linear(256,128, bias=True)
        self.k = nn.ReLU()
        self.l = nn.Linear(128, num_classes, bias=True)

    def forward(self, x):
        shape_dict = {}
        x = self.a(x)
        x = self.b(x)
        x = self.c(x)
        shape_dict[1] = list(x)
        x = self.d(x)
        x = self.e(x)
        x = self.f(x)
        shape_dict[2] = list(x)
        x = self.g(x)
        shape_dict[3] = list(x)
        x = self.h(x)
        x = self.i(x)
        shape_dict[4] = list(x)
        x = self.j(x)
        x = self.k(x)
        shape_dict[5] = list(x)
        x = self.i(x)
        shape_dict[6] = list(x)
        out = x
        return out, shape_dict


def count_model_params():
    '''
    return the number of trainable parameters of LeNet.
    '''
    model = LeNet()
    name, params = model.named_parameters()
    for param in params:
        model_params += torch.numel(param)

    return model_params


def train_model(model, train_loader, optimizer, criterion, epoch):
    """
    model (torch.nn.module): The model created to train
    train_loader (pytorch data loader): Training data loader
    optimizer (optimizer.*): A instance of some sort of optimizer, usually SGD
    criterion (nn.CrossEntropyLoss) : Loss function used to train the network
    epoch (int): Current epoch number
    """
    model.train()
    train_loss = 0.0
    for input, target in tqdm(train_loader, total=len(train_loader)):
        ###################################
        # fill in the standard training loop of forward pass,
        # backward pass, loss computation and optimizer step
        ###################################

        # 1) zero the parameter gradients
        optimizer.zero_grad()
        # 2) forward + backward + optimize
        output, _ = model(input)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        # Update the train_loss variable
        # .item() detaches the node from the computational graph
        # Uncomment the below line after you fill block 1 and 2
        train_loss += loss.item()

    train_loss /= len(train_loader)
    print('[Training set] Epoch: {:d}, Average loss: {:.4f}'.format(epoch+1, train_loss))

    return train_loss


def test_model(model, test_loader, epoch):
    model.eval()
    correct = 0
    with torch.no_grad():
        for input, target in test_loader:
            output, _ = model(input)
            pred = output.max(1, keepdim=True)[1]
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_acc = correct / len(test_loader.dataset)
    print('[Test set] Epoch: {:d}, Accuracy: {:.2f}%\n'.format(
        epoch+1, 100. * test_acc))

    return test_acc