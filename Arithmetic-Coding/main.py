from Arithmetic import ArithmeticCoding

symbols = []
probs = []

with open("test_data.txt") as dataFile:
    for line in dataFile:
        symbols.append(line.split(" ")[0])
        probs.append(float(line.split(" ")[1]))

ArthCode = ArithmeticCoding(symbols, probs, "$")
inp = "AAAAAEEEAEEAEAEAEEACCCC$"
code = ArthCode.Compress(inp)
word = ArthCode.Decompress(code)

print("Arithmetic Coding test:")
print("Compression:")
print(f"Input:{inp}")
print(f"Result:{code}")
print("_______________________")
print("Decompression")
print(f"Input:{code}")
print(f"Result: {word}\n")
print("=======================")
