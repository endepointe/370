
import sys
import math

file = open(sys.argv[1])
values = file.readlines()

total = 0
print("For",sys.argv[1],":")
for value in values:
    print(value.strip())
    total += int(value.strip())
print("avg:", math.ceil(total/15), "tries.")

'''
file.write("total=")
file.write(str(total))
file.close()
'''
