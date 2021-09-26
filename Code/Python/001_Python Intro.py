x = 10
if x > 5:
    print(x)

listx = [1,2,3,4,5,6,7]
print(listx)

listy = list(range(1,20,2))
print(listy)

# error
#listz = listx +1

# list comprehension
listz = [i +1 for i in listx]
print(listz)

# numpy
import numpy as np
arr_a = np.array(np.arange(1,8))
print(arr_a)

print(arr_a+1)
print(np.add(arr_a,1))

# it is inconvenient to index and subsetting
import pandas as pd
sr_a = pd.Series(arr_a,index=list('abcdefg'))
print(sr_a)

# dictionary
dict_a = {'a':1,'b':2,'c':3,'d':4}
print(dict_a['a'])

list_ab = list('abcdefg')
dict_b = dict(zip(list_ab,arr_a))
dict_c = {list_ab[i]:arr_a[i] for i in range(len(arr_a))}
print(dict_b)
print(dict_c)

# multiple columns
sr_b = pd.Series(arr_a*10,index=list('abcdefg'))
print(sr_b)

df_a = pd.DataFrame({'Column1':sr_b, 'Column2':sr_b})
print(df_a)

################################ Practice ###################




