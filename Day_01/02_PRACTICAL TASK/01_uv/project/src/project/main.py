def calculator(first_value, second_value, operator):
    if operator == "+":
        return first_value + second_value
    elif operator == "-":
        return first_value - second_value
    elif operator == "*":
        return first_value * second_value
    elif operator == "/":
        if second_value == 0:
            return "Error: Division by zero"
        return first_value / second_value
    else:
        return "Invalid operator"
    
def user_input(calculator):
    try:
        first_value = float(input("Enter the first value: "))
        second_value = float(input("Enter the second value: "))
    except ValueError:
        print("Invalid input! Please enter numeric values.")
        return

    operator = input("Enter the operator (+, -, *, /): ")
    result = calculator(first_value, second_value, operator)
    print(f"{first_value} {operator} {second_value} = {result:.2f}")

# Call the function
user_input(calculator)
