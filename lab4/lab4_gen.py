import include
import cmath

#Task 1

def square_generator(n):
    for i in range(n + 1):
        yield i ** 2
print("1.", end=" ")
N = 5
for square in square_generator(N):
    print(square, end=" ")

#Task 2

def even_numbers(n):
    for i in range(n+1):
        if i % 2 == 0:
            yield i
print("\n\n2.", end=" ")
N = int(input("Напиши n: "))
N = N
print(", ".join(map(str, even_numbers(N))))

#Task 3

def taf(n):              #three and four
    for i in range(n+1):
        if i % 3 == 0 and i % 4 == 0 and i != 0:
            yield i
        
    if n < 12:
        return False
print("\n3.", end=" ")
print(", ".join(map(str, taf(N))))
if taf(N) == False:
    print("Zero")

#Task 4

def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2  

a, b = map(int, input("\n4. Введите a и b через пробел: ").split())
for square in squares(a, b):
    print(square, end=" ")

#Task 5

def countdown(n):
    for i in range(n, -1, -1):
        yield i
print("\n\n5. ")
for num in countdown(N):
    print(num, end=" ")