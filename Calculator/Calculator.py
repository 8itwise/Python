
def add():
    print(num1 + num2)

def subtract():
    print(num1 - num2)

def multiply():
    print(num1 * num2)

def divide():
    print(num1 / num2)

num1 = float(input("Please input your first number: "))

symbol = input("Please choose an arithmetic operator. \n"
               "1 = Addition \n"
               "2 = subtraction \n"
               "3 = Multiplication \n"
               "4 = Division \n")

num2 = float(input("Please input your second number: "))


if symbol == str("1"):
    add()
    if symbol == str("2"):
        subtract()
        if symbol == str("3"):
            multiply()
            if symbol == str("4"):
                divide()
else:
    print("You are doing it wrong")

#calculates the square root
num = float(input('Enter a number: '))
num_sqrt = num ** 0.5
print('The square root of', num,'is', num_sqrt)

#calculates the cube root
num = float(input('Enter a number: '))
num_sqrt = num ** 0.25
print('The square root of', num,'is', num_sqrt)

#calculates the square
num = float(input('Enter a number: '))
num_square = num ** 2
print('The square root of', num,'is', num_square)

#calculates the cube
num = float(input('Enter a number: '))
num_cube = num ** 3
print('The square root of', num,'is', num_cube)




