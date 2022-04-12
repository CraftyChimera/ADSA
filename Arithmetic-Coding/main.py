from Arithmetic import ArithmeticCoding
from math import log2

symbols = []
probs = []

with open("test_data.txt") as dataFile:
    for line in dataFile:
        symbols.append(line.split(" ")[0])
        probs.append(float(line.split(" ")[1]))

entropy = sum(p*log2(1/p) for p in probs)

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
assert word == inp
print("=======================")
print(f"Entropy:{entropy} bits")
