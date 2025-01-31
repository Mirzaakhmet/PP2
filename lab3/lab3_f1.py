# Task 1


def ouncesf(grams):

    ounces = 28.3495231 * grams

    return ounces



grams = float(input("1. How many grams you need for the ingredient?\n"))

print(ouncesf(grams))


# Task 2


def converter(F):

    C = (5 / 9) * (F - 32)

    return C


F = float(input("\n2. Fahrenheit temperature.\n"))

print(converter(F))


# Task 3


def solve(numheads, numlegs):

    rabbits = int((numlegs - (2 * numheads)) / 2)

    text = f"Rabbits: {rabbits}\nChickens: {numheads-rabbits}"

    return text


numheads = int(input("\n3. How many rabbits and how many chickens do we have?\nNumheads: "))

numlegs = int(input("Numlegs: "))


print(solve(numheads, numlegs))


#Task 4


def prime(a):

    count = 0

    for i in range(2, a+1):

        if (a % i == 0):

            count = count + 1

    if (count == 1):

        print(a, end=' ')

    else:

        return 0
 

def filter_prime(arr):

    for i in arr:

        a = i

        prime(a)


arr = list(map(int, input("4. Prime numbers.\nEnter the numbers: ").split()))

print("Prime numbers:", end=' ')

filter_prime(arr)


#Task 5


