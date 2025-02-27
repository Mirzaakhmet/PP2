from functools import reduce
import time
import math

# Task 1

def multiply_list(numbers):
    return reduce(lambda x, y: x * y, numbers)

# Task 2

def count_case(s):
    upper = sum(1 for c in s if c.isupper())
    lower = sum(1 for c in s if c.islower())
    return upper, lower

# Task 3

def is_palindrome(s):
    return s == s[::-1]

# Task 4

def delayed_sqrt(number, delay):
    time.sleep(delay / 1000)
    return math.sqrt(number)

# Task 5

def all_true(t):
    return all(t)

if __name__ == "__main__":
    print(multiply_list([1, 2, 3, 4]))
    
    upper, lower = count_case("Hello World")
    print(f"Uppercase: {upper}, Lowercase: {lower}")
    
    print(is_palindrome("racecar"))
    
    number, delay = 25100, 2123
    print(f"Square root of {number} after {delay} milliseconds is {delayed_sqrt(number, delay)}")
    
    print(all_true((True, True, False)))
