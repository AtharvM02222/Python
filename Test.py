def main():
    print("Welcome! Let's find the numbers between two numbers.")
    

    number1 = int(input("Enter the first number: "))
    number2 = int(input("Enter the second number: "))
    
    # Ensure number1 is less than number2
    if number1 > number2:
        number1, number2 = number2, number1  


    print(f"The numbers between {number1} and {number2} are:")
    for num in range(number1, number2 + 1):
        print(num)

# Run 
main()
