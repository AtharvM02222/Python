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
def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    n = int(data[0])  # Number of entries in the phone book
    
    phone_book = {}
    
    # Read phone book entries
    for i in range(1, n + 1):
        entry = data[i].split()
        name = entry[0]
        phone_number = entry[1]
        phone_book[name] = phone_number
    
    # Read queries and process them
    queries = data[n + 1:]
    for query in queries:
        if query in phone_book:
            print(f"{query}={phone_book[query]}")
        else:
            print("Not found")

# Calling main function to execute the program
if __name__ == "__main__":
    main()
#
#!/bin/python3

import math
import os
import random
import re
import sys



def main():
    # Reading input
    n = int(input())
    array = list(map(int, input().split()))  # Space-separated integers to list of integers
    
    # Reverse the array
    reversed_array = array[::-1]
    
    # Print reversed array elements as space-separated numbers
    print(' '.join(map(str, reversed_array)))

# Calling main function to execute the program
if __name__ == "__main__":
    main()
#
t = int(input())
for _ in range(t):
    line = input()
    first = ""
    second = ""

    for i, c in enumerate(line):
        if (i & 1) == 0:
            first += c
        else:
            second += c
    print(first, second)
#
class Person:
    def __init__(self, initialAge):
        if (initialAge < 0):
            print("Age is not valid, setting age to 0.")
            self.age = 0
        else:
            self.age = initialAge


    def amIOld(self):
        if self.age >= 18:
            print("You are old.")
        elif self.age >= 13:
            print("You are a teenager.")
        elif age < 13:
            print("You are young.")

    def yearPasses(self):
        self.age += 1
#
#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'solve' function below.
#
# The function accepts following parameters:
#  1. DOUBLE meal_cost
#  2. INTEGER tip_percent
#  3. INTEGER tax_percent
#
meal_cost = float(input())

tip_percent = int(input())

tax_percent = int(input())


tip = (meal_cost / 100) * tip_percent
tax = (meal_cost / 100) * tax_percent

total_cost = meal_cost + tip + tax

print(round(total_cost))
#
'use strict';

process.stdin.resume();
process.stdin.setEncoding('utf-8');

let inputString = '';
let currentLine = 0;

process.stdin.on('data', inputStdin => {
    inputString += inputStdin;
});

process.stdin.on('end', _ => {
    inputString = inputString.trim().split('\n').map(string => {
        return string.trim();
    });
    
    main();    
});

function readLine() {
    return inputString[currentLine++];
}

/*
 * Complete the vowelsAndConsonants function.
 * Print your output using 'console.log()'.
 */
function vowelsAndConsonants(s) {
    for (let i = 0; i < s.length; i++) {
        if ("aeiou".includes(s[i])) console.log(s[i]);
    }

    for (let i = 0; i < s.length; i++) {
        if (!"aeiou".includes(s[i])) console.log(s[i]);
    }
}
                                        

function main() {
    const s = readLine();
    
    vowelsAndConsonants(s);
}
#
'use strict';

process.stdin.resume();
process.stdin.setEncoding('utf-8');

let inputString = '';
let currentLine = 0;

process.stdin.on('data', inputStdin => {
    inputString += inputStdin;
});

process.stdin.on('end', _ => {
    inputString = inputString.trim().split('\n').map(string => {
        return string.trim();
    });
    
    main();    
});

function readLine() {
    return inputString[currentLine++];
}

/**
*   Calculate the area of a rectangle.
*
*   length: The length of the rectangle.
*   width: The width of the rectangle.
*   
*	Return a number denoting the rectangle's area.
**/
function getArea(length, width) {
    let area = Number(length) * Number(width)
    return area;
}

/**
*   Calculate the perimeter of a rectangle.
*	
*	length: The length of the rectangle.
*   width: The width of the rectangle.
*   
*	Return a number denoting the perimeter of a rectangle.
**/
function getPerimeter(length, width) {
    let perimeter = 2 * (Number(length) + Number(width))
    return perimeter;
}


function main() {
    const length = +(readLine());
    const width = +(readLine());
    
    console.log(getArea(length, width));
    console.log(getPerimeter(length, width));
}
#
'use strict';

process.stdin.resume();
process.stdin.setEncoding('utf-8');

let inputString = '';
let currentLine = 0;

process.stdin.on('data', inputStdin => {
    inputString += inputStdin;
});

process.stdin.on('end', _ => {
    inputString = inputString.trim().split('\n').map(string => {
        return string.trim();
    });
    
    main();    
});

function readLine() {
    return inputString[currentLine++];
}

/**
*   The variables 'firstInteger', 'firstDecimal', and 'firstString' are declared for you -- do not modify them.
*   Print three lines:
*   1. The sum of 'firstInteger' and the Number representation of 'secondInteger'.
*   2. The sum of 'firstDecimal' and the Number representation of 'secondDecimal'.
*   3. The concatenation of 'firstString' and 'secondString' ('firstString' must be first).
*
*	Parameter(s):
*   secondInteger - The string representation of an integer.
*   secondDecimal - The string representation of a floating-point number.
*   secondString - A string consisting of one or more space-separated words.
**/
function performOperation(secondInteger, secondDecimal, secondString) {
    // Declare a variable named 'firstInteger' and initialize with integer value 4.
    const firstInteger = 4;
    
    // Declare a variable named 'firstDecimal' and initialize with floating-point value 4.0.
    const firstDecimal = 4.0;
    
    // Declare a variable named 'firstString' and initialize with the string "HackerRank".
    const firstString = 'HackerRank ';
    
    // Write code that uses console.log to print the sum of the 'firstInteger' and 'secondInteger' (converted to a Number        type) on a new line.
    
    
    // Write code that uses console.log to print the sum of 'firstDecimal' and 'secondDecimal' (converted to a Number            type) on a new line.
    
    
    // Write code that uses console.log to print the concatenation of 'firstString' and 'secondString' on a new line. The        variable 'firstString' must be printed first.
    console.log(Number(secondInteger) + firstInteger)
    console.log(firstDecimal + Number(secondDecimal))
    console.log(firstString + secondString)
}


function main() {
    const secondInteger = readLine();
    const secondDecimal = readLine();
    const secondString = readLine();
    
    performOperation(secondInteger, secondDecimal, secondString);
}
#
'use strict';

process.stdin.resume();
process.stdin.setEncoding('utf-8');

let inputString = '';
let currentLine = 0;

process.stdin.on('data', inputStdin => {
    inputString += inputStdin;
});

process.stdin.on('end', _ => {
    inputString = inputString.trim().split('\n').map(string => {
        return string.trim();
    });
    
    main();    
});

function readLine() {
    return inputString[currentLine++];
}
/*
 * Create the function factorial here
 */
function factorial(n) {
    // Base case: factorial of 0 is 1
    if (n === 0) {
        return 1;
    }
    
    // Recursive case: factorial of n is n * factorial(n-1)
    return n * factorial(n - 1);
}



function main() {
    const n = +(readLine());
    
    console.log(factorial(n));
}
#
