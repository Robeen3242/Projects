import torch
from torchvision.models import resnet18, ResNet18_Weights
from torch import nn, optim

model = resnet18(weights = ResNet18_Weights.DEFAULT)

#Generally we want to freeze (don't compute gradients) for most of the model
for param in model.parameters():
    param.requires_grad = False

#The last linear layer is model.fc which is unfrozen by default, we replace it with a new layer
#that acts as our classifier.
model.fc = nn.Linear(512,10) #Finetune the model on a dataset with 10 labelnano

#optimize the classifier, although we register parameters they never compute gradients
optimizer = optim.SGD(model.parameters(), lr=1e-2, momentum = 0.9)

