import numpy as np

# create an 2D array
a = np.array([[1,2],[3,4],[5,6]])
print(np.shape(a))
print(a.shape)
print(a.ndim)

# create an array of zerors, ones, a constant, identify, empty
a = np.zeros((2,3,4))
print(a)

a = np.ones((3,4,5))
print(a)

a =np.full((3,2),7)
print(a)

a =np.eye(3)
print(a)

a =np.empty((2,2))
print(a)

# matrix multiplication
# print(a@b)

# arrange & linespace
print(np.arange(1,16,3))
print(np.linspace(0,100,5))

# arithmetric
a =np.full((3,3),[1,2,3])
b=np.eye(3)
print(a@b)#matrix mulitplication
print(a+b)
print(a-b)
print(a*b)
print(np.average(a))
print(np.exp(a))
print(np.sqrt(a))
print(np.sin(a))
print(np.cos(a))
print(np.log(a))

# reshape
print(a.reshape(9,1))

# subsetting, slicing, indexing
c=a+b
print(c)
print(c[1])#get the second row
print(c[1,1])# the second row and second column

print(c[0:2])#slice the first and second rows
print(c[0:2,1])#slice the first and second rows, and only the second column

print(c[:1])#slice the first row
print(c[1,...])#slice the first row
print(c[[1,2],[1,2]]) # select (1,1),(2,2)

d=np.arange(1,11)
print(d[2::2]) # select from the third item and select every two items

# enumerate
for x, val in np.ndenumerate(a):
	print(x,val)
	
for x in np.nditer(a):
  print(x)


# combining array
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
arr = np.concatenate((arr1, arr2))
print(arr)

arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])
arr = np.concatenate((arr1, arr2), axis=0)
print(arr)
arr_axis1 = np.concatenate((arr1, arr2), axis=1)
print(arr_axis1)

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
arr_h = np.hstack((arr1, arr2))
arr_v = np.vstack((arr1, arr2))
arr_d = np.dstack((arr1, arr2))
print(arr_h,arr_v,arr_d)

# split array
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15], [16, 17, 18]])
newarr = np.array_split(arr, 3, axis=1)
print(newarr)

# search
arr = np.array([1, 2, 3, 4, 5, 4, 4])
x = np.where(arr == 4)
print(x)

