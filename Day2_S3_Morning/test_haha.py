def test():
	return [1]

def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == 5

for i in range(10):
	print(i)

# Initialize `fahrenheit` dictionary 
fahrenheit = {'t1':90, 't2':-20, 't3':-10, 't4':0}

#Get the corresponding `celsius` values
celsius = list(map(lambda x: (float(5)/9)*(x-32), fahrenheit.values()))

#Create the `celsius` dictionary
celsius_dict = dict(zip(fahrenheit.keys(), celsius))

print(celsius_dict)