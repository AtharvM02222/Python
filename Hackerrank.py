print("Hello World")
#
import math
import os
import random
import re
import sys


n = int(input())

if n % 2:
    print("Weird")
elif 2 <= n <= 5:
    print("Not Weird")
elif 6 <= n <= 20:
    print("Weird")
else:
    print("Not Weird")
#
a = int(input())
b = int(input())

print(a + b)
print(a - b)
print(a * b)
#
a = int(input())
b = int(input())

Q = a//b
w = a/b

print(Q)
print(w)
#
n = int(input())

if 0 < n:
    for i in range(n):
        print(pow(i,2))
#
def is_leap(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False
#
if __name__ == '__main__':
    n = int(input())
    for i in range(n):
        print(i + 1, end = "")
#
