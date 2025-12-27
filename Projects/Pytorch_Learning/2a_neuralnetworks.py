#NN's are constructed using torch.nn package. NN's depend on autograds.

# Typical training procedure for a NN
# 1. Define NN that has learnable parameters and weights
# 2. Iterate over dataset of inputs
# 3. Process through network
# 4. Compute loss
# 5. Propagate gradients back into networks parameters
# 6. Update the weights using weight = weight - learning_rate*gradient

import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        #WE ONLY DEFINE PARAMETERS FOR NOW
        #EACH PARAMETER HAS ITS BIAS
        # The 'image channels' refer to feature maps
        # conv1 compares individual feature maps
        # conv2 compares 6 feature maps locally


        # 1 input image channel, 6 output channels, 5x5 square convolution kernel
        self.conv1 = nn.Conv2d(1, 6, 5)
        # 6 input image channel, 16 output channels, 5x5 square convolution kernel
        self.conv2 = nn.Conv2d(6, 16, 5)
        # an affine operation: y = Wx + b

        #output 120 features
        self.fc1 = nn.Linear(16 * 5 * 5, 120)  # 5*5 from image dimension
        #output 84 features
        self.fc2 = nn.Linear(120, 84)
        # output 10 features
        self.fc3 = nn.Linear(84, 10)

    def forward(self, input):
        #Forward never iterates over a dataset, it processes one batch at a time
        #We are batch processing here

        #Conceptually if we are processing a 32x32 image it is inefficient to give every neuron
        #1024 weights and instead we do it 5x5 for small regions and we use one filter (conv1,conv2, etc)
        #to weigh these regions evenly. The set of 5x5 are called kernels, and applying a kernel(filter)
        #to one image produces a feature map.

        #Our input is a 32x32 image with a 5x5 kernel with one stride. Therefore we produce a 28x28
        #32-5+1= 28
        #Each image becomes a grid of kernels, this grid is a feature map

        #Feature maps still grow fast and are affected by slight pixel shifts. We pool by reducing dimensions
        #for faster and more efficient computation. Think of it like creating a frequency map where we only care
        #about the general location rather than exact location.

        #We do conv -> pool because we are essentially detecting patterns first and then summarizing them.

        # ---- Conv 1 ---- #
        # Convolution layer C1: 1 input image channel, 6 output channels, 5x5 square convolution.
        # Outputs a Tensor with size (N, 6, 28, 28), where N is the size of the batch
        c1 = F.relu(self.conv1(input))

        # Subsampling layer S2: 2x2 grid
        # This layer does not have any parameter, and outputs a (N, 6, 14, 14) Tensor
        s2 = F.max_pool2d(c1, (2, 2))

        # ---- Conv 2 ---- #
        # Convolution layer C3: 6 input channels, 16 output channels, 5x5 square convolution
        # Outputs a (N, 16, 10, 10) Tensor
        c3 = F.relu(self.conv2(s2))

        # Subsampling layer S4: 2x2 grid
        # this layer does not have any parameter, and outputs a (N, 16, 5, 5) Tensor
        s4 = F.max_pool2d(c3, 2)

        # Flatten operation: purely functional, outputs a (N, 400) Tensor
        s4 = torch.flatten(s4, 1)

        # ---- Connecting layers ---- #
        #'Connecting' means we feed the output of one layer to another
        # Each layer is a function and you chain them together


        # Fully connected layer F5: (N, 400) Tensor input,
        # and outputs a (N, 120) Tensor
        f5 = F.relu(self.fc1(s4))

        # Fully connected layer F6: (N, 120) Tensor input,
        # and outputs a (N, 84) Tensor
        f6 = F.relu(self.fc2(f5))

        # Fully connected layer OUTPUT: (N, 84) Tensor input, and
        # outputs a (N, 10) Tensor
        output = self.fc3(f6)
        return output

net = Net()
#Returns initialized attributes
#print(net)
params = list(net.parameters())
#print(len(params)) #prints weight, bias, weight, bias ....

input = torch.randn(1,1,32,32)
out = net(input)
#print(out) #prints these params

net.zero_grad() #Zero gradient buffers
out.backward(torch.randn(1,10)) #fill with random gradients

# ----- Loss Function ----- #
output = net(input)
target = torch.randn(10) #create a random target (since we don't have one)
target = target.view(1,-1) #make it the same shape as our output
criterion = nn.MSELoss()

loss = criterion(output, target)
#print(loss)

# input -> conv2d -> relu -> maxpool2d -> conv2d -> relu -> maxpool2d
#       -> flatten -> linear -> relu -> linear -> relu -> linear
#       -> MSELoss
#       -> loss

# ----- Backprop ----- #
net.zero_grad()     # zeroes the gradient buffers of all parameters

print('conv1.bias.grad before backward')
print(net.conv1.bias.grad)

loss.backward()

print('conv1.bias.grad after backward')
print(net.conv1.bias.grad)

# ----- Updating ----- #
# Use weight = weight -learning_rate*gradient

learning_rate = 0.01
for f in net.parameters():
    f.data.sub_(f.grad.data*learning_rate)

    import torch.optim as optim

#Sometimes we want to use different update rules. The package torch.optim implements a lot of methods.
# create your optimizer
optimizer = optim.SGD(net.parameters(), lr=0.01)

# in your training loop:
optimizer.zero_grad()   # zero the gradient buffers as they are accumulated
output = net(input)
loss = criterion(output, target)
loss.backward()
optimizer.step()    # Does the update