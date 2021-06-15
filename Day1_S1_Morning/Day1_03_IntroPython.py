########### Basic Data Type ##########
# define a integer
my_int = 100
print(my_int)

# defind a floating-point number
my_float = 3.14
print(my_float) 

# define a string
my_string = "Lets Learn Python!"
print(my_string)

# string Concatenation
string_one = "I’m reading "
string_two = "a new great book!"
print(string_one + string_two)

# string replicate
print("Hello World "*3)

# math operator
print(2 ** 3)	# Exponent
print(22 % 8)	# Modulus
print(22 //8)	# Integer Division
print(22/8)		#Division
print(3* 4) 	# Mutliplication

########## List ############
my_list = [100, 2, 3]
my_list2 = ["a", "b", "c"] 
print(my_list + my_list2)
print([my_list , my_list2])

my_list3 = ["4", "ss", "book", 5]
print(my_list3)
my_list3.append("hello")
print(my_list3)
my_list3.remove("book")
print(my_list3)
my_list3.pop()
print(my_list3)
print(sorted(my_list))
print(my_list3[1:2])
print(my_list3[:2])

# Loop a list
for x in range(4): 
	my_list3 +=['fruit']
	print(my_list3)

# List comprehension
my_list4= [x * 2 for x in my_list3]
print(my_list4)

my_list4[2]="5"
my_list5= [x + "hi" for x in my_list4]
print(my_list5)

# For loop
for x in my_list5:
	print(x)

# if else
a = 45
b = 49 
if b > a:
	print("b is greater than a")
elif a == b:
	print(" a and b are equal")


# define a function
def name(x,y):
	print(x+y)

name(1,1)

# dictionary
car = {
"brand": "Ford",
"model": "Mustang",
"year": 1964
}

x = car.keys()
print(x) #before the change
car["color"] = "white"
print(x) #after the change

x = car.values()
print(x) #before the change
car["color"] = "red"
print(x) #after the change

x = car.items()
print(x) #before the change
car["year"] = 2020
print(x) #after the change

# python function args
def myFunction(*args, **kwargs):
    print(args)
    print(kwargs)

# if the module that is being run is the main program, the __name__ variable will be set as  __main__ 
if __name__ == "__main__":
    myFunction("hello", "mars", a = 24, b = 87, c = 3, d = 46)
