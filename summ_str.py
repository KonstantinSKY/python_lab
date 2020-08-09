import sys

digit_string = sys.argv[1]

numbers = list(digit_string)
summ = 0
for number in numbers:
    summ += int(number)
print(summ)

# short solution
print(sum([int(x) for x in sys.argv[1]]))
