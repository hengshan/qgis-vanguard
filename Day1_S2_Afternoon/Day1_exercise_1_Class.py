# create a string list 
list1 = ["a", "b", "c"]
print(list1)

# create a integer list
list2 = [1, 2, 3]
for l in list2:
    print(l)


class MyClass():
    def __init__(self, input_list):
        self.input_list = input_list
        print("MyClass Initialized")

    def __str__(self):
    	return f'unpack a list: {" ".join(map(str, self.input_list))}'
    	#f'unpack a list: {" ".join(str(x) for x in a)}'


class MySubClass(MyClass):
    def __init__(self, input_list):
        self.input_list = input_list
        print("MySubClass Initialized")

    def sum_square(self):
        if all(isinstance(l, int) for l in self.input_list):
            return sum(l**2 for l in self.input_list)
        elif all(isinstance(l, str) for l in self.input_list):
            return "".join(l * 2 for l in self.input_list)
        else:
            print("The input list should only contain numbers or strings, not both")

list3 = [1, 2, "ab"]
m = MyClass(list3)
print(m)

ms=MySubClass(list1)
print(ms.sum_square())

ms2=MySubClass(list2)
print(ms2.sum_square())
