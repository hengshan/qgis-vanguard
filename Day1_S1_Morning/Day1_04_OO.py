class Person():
    def __init__(self):
        print("Initiating a person object")
    
HS = Person()
HS.hobby="TT"
KH = Person()
KH.hobby="SW"
TG = Person()
TG.hobby="CC"

print(HS.hobby)
print(KH.hobby)
print(TG.hobby)

class Employee(Person):
   def __init__(self, department):
       super().__init__()
       self.department = department

e1 = Employee("DSGA")
e2 = Employee("Others")
print(e1.department)
print(e2.department)

