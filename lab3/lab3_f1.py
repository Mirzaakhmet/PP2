#function 1

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


def get_permutations(line, prefix=""):
    if len(line) == 0:
        print(prefix)
    else:
        for i in range(len(line)):
            remaining = line[:i] + line[i+1:]
            get_permutations(remaining, prefix + line[i])

line = input("Enter the word: ").strip()
print("All permutations of the line: ")
get_permutations(line)


from itertools import permutations

def get_permutations():
    line = input("Enter the word: ").strip()
    
    all_permutations = permutations(line)   # перестановка
    
    print("All permutations of the line: ")
    for perm in all_permutations:
        print("".join(perm))    # объединение

get_permutations()

#Task 6

from itertools import permutations

def get_permutations():
    words = list(map(str, input("Enter the word: ").split()))
    
    all_permutations = permutations(words)
    
    print("All permutations of the line: ")
    for perm in all_permutations:
        print(" ".join(perm))

get_permutations()

#Task 7

def has_33(nums):
    ans = False
    for i in range(1, len(nums)):
        if nums[i] == 3 and nums[i-1] == 3:
            ans = True
            break
    return ans

arr = list(map(int, input("Enter the numbers: ").split()))

print(has_33(arr))

#Task 8

def spy_game(nums):
    ans = False
    for i in range(0, len(nums)):
        if nums[i] == 0:
            for j in range(i+1, len(nums)):
                if nums[j] == 0:
                    for k in range(j+1, len(nums)):
                        if nums[k] == 7:
                            ans = True
                            break
    return ans

arr = list(map(int, input("Enter the numbers: ").split()))

print(spy_game(arr))

#Task 9

def volume_of_sphere(r):
    V = (4 * 3.14 * r**3)/3 
    return V

a = int(input("Enter the radius of a sphere: "))
print(f'Volume of a sphere = {volume_of_sphere(a)}')

#Task 10

def unique_list(arr):
    unique_arr = []
    for i in arr:
        a = 0
        for j in arr:
            if i == j:
                a += 1
        if a == 1:
            unique_arr.append(i)
    return unique_arr

var = list(map(int, input("Enter the numbers: ").split()))

print(unique_list(var))

#Task 11

def is_palindrome(a):
    if a == a[::-1]:
        print(f'The {a} is a palindrome')
    else:
        print(f'The {a} is not a palindrome')

var = input("Enter a word, phrase or sequence: ")

is_palindrome(var)

#Task 12

def histogram():
    nums  = list(map(int, input("Enter the numbers: ").split()))
    for i in nums:
        pic = '*'*i
        print("".join(pic))
    
histogram()

#Task 13

def guess_the_num():
    from random import randint

    print('Hello! What is your name?')
    user_name = str(input("My name is "))

    a, b = map(int,input("Between which numbers should the number be guessed: ").split())
    hidden_num = randint(a, b)

    print(f"Well, {user_name}, I am thinking of a number between {a} and {b}.")

    count = 1
    while True:
        num = int(input('Take a guess.\n'))

        if num != hidden_num:
            if num < hidden_num:
                print('Your guess is too low.')
            else:
                print('Your guess is too high.')
            count += 1
        else:
            print(f'Good job, {user_name}! You guessed my number in {count} guesses!')

        

guess_the_num()