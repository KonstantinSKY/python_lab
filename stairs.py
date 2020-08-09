import sys


# digit = int(sys.argv[1])
digit = 5

for i in range(digit):
    print(" "*(digit-(i+1))+"#"*(i+1))

[print(" "*(digit-(i+1))+"#"*(i+1)) for i in range(digit)]
print("enf")