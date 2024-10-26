
print("Hello")
print("World")      
print("!")

name = "Mike"    # Strings
age = 30         # Integer
gpa = 3.5         # Decimal
is_tall = True    # Boolean -> True/False

name = "John"

print("Your name is " + name)
print("Your name is", name)


print( int(3.14) )
print( float(3) )
print( str(True) )
print( int("50") + int("70") )


greeting = "Hello"
#indexes:   01234

print( len(greeting) )
print( greeting[0] )
print( greeting[-1] )
print( greeting.find("llo") )
print( greeting.find("z") )
print( greeting[2:] )
print( greeting[2:3] )


print( 2 * 3 )       # Basic Arithmetic: +, -, /, *
print( 2**3 )       # Basic Arithmetic: +, -, /, *
print( 10 % 3 )      # Modulus Op. : returns remainder of 10/3
print( 1 + 2 * 3 )   # order of operations
print(10 / 3.0)      # int's and doubles


num = 10
num += 100 # +=, -=, /=, *=
print(num)

++num
print(num)

# Math module has useful math methods
import math
print( pow(2, 3) )
print( math.sqrt(144) )
print( round(2.7) )


name = input("Enter your name: ")
print("Hello", name + "!")

num1 = int(input("Enter First Num: "))
num2 = int(input("Enter Second Num: "))
print(num1 + num2)


lucky_numbers = [4, 8, "fifteen", 16, 23, 42.0]
#       indexes  0  1       2      3   4   5

lucky_numbers[0] = 90
print(lucky_numbers[0])
print(lucky_numbers[1])
print(lucky_numbers[-1])
print(lucky_numbers[2:])
print(lucky_numbers[2:4])
print(len(lucky_numbers))


numberGrid = [ [1, 2], [3, 4] ]
numberGrid[0][1] = 99

print(numberGrid[0][0])
print(numberGrid[0][1])


friends = []
friends.append("Oscar")
friends.append("Angela")
friends.insert(1, "Kevin")

# friends.remove("Kevin")
print( friends )
print( friends.index("Oscar") )
print( friends.count("Angela") )
friends.sort()
print( friends )
friends.clear()
print( friends )


lucky_numbers = (4, 8, "fifteen", 16, 23, 42.0)
#       indexes  0  1       2      3   4   5

lucky_numbers[0] = 90
print(lucky_numbers[0])
print(lucky_numbers[1])
print(lucky_numbers[-1])
print(lucky_numbers[2:])
print(lucky_numbers[2:4])
print(len(lucky_numbers))


def add_numbers(num1, num2=99):
     return num1 + num2

sum = add_numbers(4, 3)
print(sum)


is_student = False
is_smart = False

if is_student and is_smart:
	print("You are a student")
elif is_student and not(is_smart):
	print("You are not a smart student")
else:
	print("You are not a student and not smart")


# >, <, >=, <=, !=, ==
if 1 > 3:
	print("number omparison was true")


if "dog" == "cat":
   print("string omparison was true")


test_grades = {
    "Andy" : "B+",
    "Stanley" : "C",
    "Ryan" : "A",
    3 : 95.2
}
print( test_grades["Andy"] )
print( test_grades.get("Ryan", "No Student Found") )
print( test_grades[3] )


index = 1
while index <= 5:
	print(index)
	index += 1


for index in range(5):
    print(index)

lucky_nums = [4, 8, 15, 16, 23, 42]
for lucky_num in lucky_nums:
    print(lucky_num)

for letter in "Giraffe":
    print(letter)


try:
    answer = 10 / int(input("Enter Number: "))
except ZeroDivisionError as e:
    print(e)
except:
    print("Caught any exception")       



class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def read_book(self):
         print("Reading", self.title, "by", self.author)

book1 = Book("Harry Potter", "JK Rowling");
# book1.title = "Half-Blood Prince"

print(book1.title)
book1.read_book()



class Book:
    def __init__(self, title, author):
        self.title = title;
        self.author = author

    @property
    def title(self):
        print("getting title")
        return self._title

    @title.setter
    def title(self, value):
        print("setting title")
        self._title = value

    @title.deleter
    def title(self):
        del self._title


    def read_book(self):
         print("Reading", self.title, "by", self.author)

book1 = Book("Harry Potter", "JK Rowling");
# book1.title = "Half-Blood Prince"

print(book1.title)
book1.read_book()



class Chef:

   def __init__(self, name, age):
       self.name = name
       self.age = age


   def make_chicken(self):
       print("The chef makes chicken")

   def make_salad(self):
       print("The chef makes salad")

   def make_special_dish(self):
       print("The chef makes bbq ribs")

class ItalianChef(Chef):

   def __init__(self, name, age, countryOfOrigin):
       self.countryOfOrigin = countryOfOrigin
       super().__init__(name, age)

   def make_pasta(self):
       print("The chef makes pasta")

   def make_special_dish(self):
       print("The chef makes chicken parm")


myChef = Chef("Gordon Ramsay", 50)
myChef.make_chicken()

myItalianChef = ItalianChef("Massimo Bottura", 55, "Italy")
myItalianChef.make_chicken()
print(myItalianChef.age);
