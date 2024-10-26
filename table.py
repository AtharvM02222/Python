def print_table(number, up_to=10):
    for i in range(1, up_to + 1):
        result = number * i
        print(f"{number} x {i} = {result}")


number = int(input("Enter the number for which you want the table: "))
up_to = int(input("Enter the range for the table (default is 10): "))

# Print
print_table(number, up_to)
