import torch
import numpy as np
# ------- Attributes and Operations ------- #
data = [[1,2],[3,4]]
x_data = torch.tensor(data) #Type is inferred
# np_array = np.array(data) #to numpy
# x_np = torch.from_numpy(np_array) #to Tensor

x_ones = torch.ones_like(x_data) #'ones' all the values
x_rand = torch.rand_like(x_data, dtype=torch.float) #overrides datatype of x_data with random variables between 0 and 1


shape = (2,3)
rand_tensor = torch.rand(shape)
ones_tensor = torch.ones(shape)
zeros_tensor = torch.zeros(shape)

tensor = torch.rand(3,4)
# print(tensor.shape)
# print(tensor.dtype)
# print(tensor.device)


if torch.cuda.is_available():
    #Checks if we can move our tensor to the GPU
    tensor = tensor.to('cuda')
    print(tensor.device)


tensor = torch.ones(4,4)
tensor[:, 1] = 0 #Change all of collumn 1 to 0
# tensor[2] = 0 #Change all of row 2 to 0

t1 = torch.cat([tensor,tensor,tensor], dim=1) #concatenates tensors

#Both return the product
# print(f"tensor.mul(tensor) \n {tensor.mul(tensor)}")
# print(f"tensor * tensor \n {tensor*tensor}")

#Both return the matrix multiplication 
# print(f"tensor.matmul(tensor.T) \n {tensor.matmul(tensor.T)} \n")
# print(f"tensor @ tensor.T \n {tensor @ tensor.T}")

#adds to all places
# print(tensor, "\n")
# tensor.add_(5)
# print(tensor)

# ----- Bridge with Numpy ----- #
# Tensors in CPU and Numpy arrays share memory locations
t = torch.ones(5)
n = t.numpy()
# print(f"t: {t}")
# print(f"n: {t}")

#Changing one changes th other
t.add_(1)
# print(f"t: {t}")
# print(f"n: {t}")

n = np.ones(5)
t = torch.from_numpy(n)
np.add(n,1, out=n)
print(f"t: {t}")
print(f"n: {t}")

