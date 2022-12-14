import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

def get_data_loader(training = True):
    transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    if training:
        train_set = datasets.FashionMNIST('./data',train=True,download=True,transform=transform)
        loader = torch.utils.data.DataLoader(train_set, batch_size=64)
    else:
        test_set=datasets.FashionMNIST('./data', train=False,transform=transform)
        loader = torch.utils.data.DataLoader(test_set, batch_size=64, shuffle=False)
    return loader

def build_model():
    model = nn.Sequential(
        nn.Flatten(),
        nn.Linear(784,128),
        nn.ReLU(),
        nn.Linear(128,64),
        nn.ReLU(),
        nn.Linear(64,10),
    )
    return model

def train_model(model, train_loader, criterion, T):
    opt = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    model.train()
    for epoch in range(T):
        running_loss = 0.0
        for images, labels in train_loader:
            opt.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            opt.step()
            running_loss += loss.item()
        print(f"Train Epoch: {str(epoch)} Accuracy: {str(int(len(train_loader.dataset) - running_loss))}/{str(len(train_loader.dataset))}({str(round((len(train_loader.dataset) - running_loss)/len(train_loader.dataset) * 100,2))}%) Loss: {str(round(running_loss/len(train_loader),3))}")

def evaluate_model(model, test_loader, criterion, show_loss = True):
    model.eval()
    with torch.no_grad():
        correct = 0
        total = 0
        for images, labels in test_loader:
            outputs = model(images)
            loss = criterion(outputs, labels)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            loss += (loss.item()*images.size(0))
        if show_loss:
            print(f"Average loss: {str(round(loss.item()/len(test_loader),4))}")
        print(f"Accuracy: {str(round(correct / total * 100, 2))}%")
    
def predict_label(model, test_images, index):
    outputs = model(test_images[index])
    prob = F.softmax(outputs,1)
    predicted = torch.topk(prob.flatten(),3)
    class_names = ['T-shirt/top','Trouser','Pullover','Dress','Coat','Sandal','Shirt','Sneake','Bag','Ankle Boot']
    for i in range(len(predicted.indices)):
        print(f"{class_names[i]}: {round(float(predicted[0][i]) * 100,2)}%")