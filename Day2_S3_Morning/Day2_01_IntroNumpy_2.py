from numpy import random

# Generate a random integer from 0 to 100 
x = random.randint(100)
print(x)

# standard normal, 2 rows and 100 columns
x =random.randn(2,100)
print(x)
print(x.shape)

# random float 0 to 1
x = random.rand()
print(x)

x = random.rand(3, 5)
print(x)

# random int array with size 2 * 2
x=random.randint(100, size=(2,2))
print("random int", x)

# random based on an array
x = random.choice([3, 5, 7, 9])
print(x)

x = random.choice([3, 5, 7, 9], size=(3, 5))
print(x)

# data distribution
x = random.choice([3, 5, 7, 9], p=[0.1, 0.3, 0.6, 0.0], size=(100))
print(x)

# normal distribution
x = random.normal(loc=1, scale=2, size=(2, 3))
print(x)

# binomial distribution
x = random.binomial(n=10, p=0.5, size=10)
print(x)

x = random.poisson(lam=2, size=10)
print(x)

x = random.uniform(size=(2, 3))

x = random.logistic(loc=1, scale=2, size=(2, 3))

x = random.multinomial(n=6, pvals=[1/6, 1/6, 1/6, 1/6, 1/6, 1/6])
x = random.exponential(scale=2, size=(2, 3))
x = random.chisquare(df=2, size=(2, 3))






