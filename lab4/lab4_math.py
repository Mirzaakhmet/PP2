import math
from math import*

# Task 1

def detor():
    degree = int(input("1. Input degree: "))
    radian = radians(degree)
    print(f"Output radian: {radian}")

detor()

# Task 2

def aretrap():
    height = int(input("\n2. Height: "))
    firts_value = int(input("Base, first value: "))
    second_value = int(input("Base, second value: "))
    area = ((firts_value + second_value) * height) * 0.5
    print(f"Expected Output: {area}")

aretrap()

# Task 3

def regpol():
    number = int(input("\n3. Input number of sides: "))
    lenght = int(input("Input the length of a side: "))
    area = (number * pow(lenght, 2)) / (4 * tan(math.pi / number))
    print(f"The area of the polygon is: {int(area)}")

regpol()

# Task 4

def lologram():
    lenght = int(input("\n4. Length of base: "))
    height = int(input("Height of parallelogram: "))
    area = lenght * height
    print(f"Expected Output: {float(area)}")

lologram()