from functools import reduce
from math import log2


initial_state = 0
precision = 8

alphabet = [0, 1, 2]
pmf = [1/2, 1/4, 1/4]
entropy = sum(p*log2(1/p) for p in pmf)

cdf = reduce(lambda acc, el: acc + [acc[-1] + round(el*precision)], pmf, [0])


def cdf_func(symbol):
    return cdf[symbol], cdf[symbol+1]


def icdf_func(cdf_value):
    for symbol in alphabet:
        cdf_low, cdf_high = cdf_func(symbol)
        if cdf_low <= cdf_value < cdf_high:
            return symbol, cdf_low, cdf_high


def push(state, symbol, cdf_func, prec):
    cdf_low, cdf_high = cdf_func(symbol)
    freq = cdf_high - cdf_low
    return prec*(state // freq) + (state % freq) + cdf_low


def pop(state, icdf_func, prec):
    cdf_value = state % prec
    symbol, cdf_low, cdf_high = icdf_func(cdf_value)
    freq = cdf_high - cdf_low
    return symbol, freq*(state // prec) + cdf_value - cdf_low


sequence = 100*[2, 0, 0, 1]

state = initial_state
for symbol in reversed(sequence):
    state = push(state, symbol, cdf_func, precision)

print("Asymmetric Number System Encoding:")
print("Compression:")
print(f"Result:{state}")
print("_______________________")

decoded_sequence = len(sequence)*[None]
for i in range(len(sequence)):
    decoded_sequence[i], state = pop(state, icdf_func, precision)

assert decoded_sequence == sequence

print(f'''
- Encoded {len(sequence)} symbols
- Entropy: {entropy} bits
''')
