def cal_power(n):
    return x ** n


x = int(input("Enter the value of x:"))
numbers = [2, 3, 4]

result = map(cal_power, numbers)
print(list(result))