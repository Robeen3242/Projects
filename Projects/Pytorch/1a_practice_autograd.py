#Neural networks (NNs) are collectinos of nested functions that are executed on some input
#utilizing weights and biases which are stored in tensors

#Forward Propagation: NN makes the best guess about a correct output, running input data through each function.

#Backward Propagation: NN adjusts parameters proportionate to error in the guess by traversing backwards
#from the output, collecting derivatives of hte error with respect to the functions(gradients) and optimizing
#parameters using gradient descent.

#Gradient: A set of derivatives that represent direction

#Optimizer: The optimizer minimizes the error (loss function)

import torch
from torchvision.models import resnet18, ResNet18_Weights
model = resnet18(weights = ResNet18_Weights.DEFAULT)
data = torch.rand(1,3,64,64)
labels = torch.rand(1,1000)

prediction = model(data) # forward pass
loss = (prediction - labels).sum()
loss.backward() #backwward pass
#Autograd calcs and stores gradient for each parameter in the .grad attribute

optim = torch.optim.SGD(model.parameters(), lr=1e-2, momentum=0.9)
optim.step() #gradient descent

# ----- Differentiatiion ----- #
# a and b are parameters of NN and Q is the error
a = torch.tensor([2.,3.], requires_grad=True)
b = torch.tensor([6.,4.], requires_grad=True)
q = 3*a**3 - b**2 #q = 3a^3 - b^2

#Differentiating backwards
external_grad = torch.tensor([1.,1.]) 
q.backward(gradient=external_grad)
#Gradients are now deposited in a.grad and b.grad
# print(9*a**2 == a.grad)
# print(-2*b == b.grad)

# In general, torch.autograd is an engine for computing vector Jacobian product.
# If v is a gradient of a scalar function l, then by chain rule, the vector-Jacobian product would be the 
# gradient of l with respect to x.

# You can set a tensors requires_grad flag to T/F depending on whether a tensor doesn't require a gradient
# It is assumed false unless it is opperated on by a tensor that has it true
x = torch.rand(5,5)
y = torch.rand(5,5)
z = torch.rand((5,5), requires_grad=True)

a = x + y
b = x + z
# print(a.requires_grad)
# print(b.requires_grad)
