from Arithmetic import ArithmeticCoding

symbols = []
probs = []

with open("test_data.txt") as dataFile:
    for line in dataFile:
        symbols.append(line.split(" ")[0])
        probs.append(float(line.split(" ")[1]))

ArthCode = ArithmeticCoding(symbols, probs, "$")

code = ArthCode.Compress("AAAAAEEEAEEAEAEAEEACCCC$")
word = ArthCode.Decompress(code)
# Output results
print("Arithmetic Coding test:")
print("~~~~~~~~~~~~~~~~~~~~~~~")
print('Compress ')
print(f"Result:{code}")
print("_______________________\n")
print(f"Decompress:{code}")
print(f"Result: {word}\n")
print("=======================")
