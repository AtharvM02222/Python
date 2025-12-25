def main():
    print("Welcome! Let's find and separate the numbers between two numbers into odd and even.")
    

    number1 = int(input("Enter the first number: "))
    number2 = int(input("Enter the second number: "))
    
    # Ensure number1 is less than number2
    if number1 > number2:
        number1, number2 = number2, number1 


    even_numbers = []
    odd_numbers = []
    

    for num in range(number1, number2 + 1):
        if num % 2 == 0:
            even_numbers.append(num)
        else:
            odd_numbers.append(num)


    print(f"The even numbers between {number1} and {number2} are: {even_numbers}")
    print(f"The odd numbers between {number1} and {number2} are: {odd_numbers}")

#RuN
main()
