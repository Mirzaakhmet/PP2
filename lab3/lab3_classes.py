# Classes
 
#Task 1
class toUpper:
    def __init__(self):
        self.text = ''
 
    def getString(self):
        self.text = str(input('Enter a string: '))
   
    def printString(self):
        print(self.text.upper())
 
obj = toUpper()
obj.getString()
obj.printString()
 
#Task 2    
class Shape:
    def area(self):
        return 0
 
class Square(Shape):
    def __init__(self, length):
        self.length = length
 
    def area(self):
        return self.length ** 2
   
shape = Shape()
print("Default Shape Area:", shape.area())
 
square = Square(5)
print("Square Area:", square.area())

#Task 3
class Rectangle(Shape):
    def __init__(self,  lenght, widht):
        self.length = lenght
        self.widht = widht
    
    def area(self):
        return self.length * self.widht

abcd = Rectangle(5,4)
print(abcd.area())

#Task 4
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def show(self):
        text = 'Coordinates of the specified point: ('+str(self.x)+';'+str(self.y)+')'
        return text
    
    def move(self, plus_x, plus_y):
        self.x += plus_x
        self.y += plus_y
        
        text = 'Now the coordinates of the specified point: ('+str(self.x)+';'+str(self.y)+')'
        return text
    
    def dist(self):
        text = 'Distance between x and y: ' + str((self.x**2 + self.y**2)**0.5)
        return text

to4ka = Point(5,10)
print(to4ka.show())
print(to4ka.move(5,15))
print(to4ka.show())
print(to4ka.dist())

#Task 5
class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
    
    def  deposit(self, plus):
        self.balance += plus
        text = 'Bank account: '+str(self.owner)+'\nReplenishment: '+str(plus)+'\nAvailable: '+str(self.balance)+'\n'
        return text

    def withdraw(self, minus):
        if minus > self.balance:
            text = 'It is impossible to perform this operation,'+'\nyou do not have such amount in your account'+'\nBalance: '+str(self.balance)
            return text
        else:
            self.balance -= minus
            text = 'Bank account: '+str(self.owner)+'\nWithdrawal: '+str(minus)+'\nAvailable: '+str(self.balance)+'\n'
            return text
        
person1 = Account('Muslim', 150000)
print(person1.deposit(15000))
print(person1.withdraw(35000))

person2 = Account('Perizat', 8455)
print(person2.deposit(1488))
print(person2.withdraw(3000))

#task 6
def check_prime(i):
    check, a = False, 2
    if i == 2:
        return True
    while i>a:
        if i%a == 0:
            check = False
            break
        else:
               check = True
        a += 1
    return check

arr = list(map(int, input('Enter the numbers: ').split()))

prime_nums = list(filter(lambda x: check_prime(x), arr))

print(prime_nums)