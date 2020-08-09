import sys

digit = int(sys.argv[1])

[print(" "*(digit-(i+1))+"#"*(i+1)) for i in range(digit)]
