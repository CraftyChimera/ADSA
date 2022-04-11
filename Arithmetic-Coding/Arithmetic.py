class ArithmeticCoding:

    def __init__(self, symbols, probs, terminator):
        self.symbols = symbols
        self.probs = probs
        self.__InitRangeTable()
        self.terminator = terminator

    def __InitRangeTable(self):
        self.rangeLow = {}
        self.rangeHigh = {}
        rangeStart = 0

        for i in range(len(self.symbols)):
            s = self.symbols[i]
            self.rangeLow[s] = rangeStart
            rangeStart += self.probs[i]
            self.rangeHigh[s] = rangeStart

    def Compress(self, word):
        low_final = 0.0
        range = 1.0
        high_final = 1.0

        for c in word:
            low = low_final + range * self.rangeLow[c]
            high = low_final + range * self.rangeHigh[c]
            range = high - low
            low_final = low
            high_final = high

        value = 0
        x = 0.5
        while(value < low_final):
            value += x
            if (value > high_final):
                value -= x
            x /= 2
        return value

    def Decompress(self, code):
        s = ""
        result = ""
        while (s != self.terminator):
            for key in self.rangeLow:
                if code >= self.rangeLow[key] and code < self.rangeHigh[key]:
                    result += key
                    low = self.rangeLow[key]
                    high = self.rangeHigh[key]
                    _range = high - low
                    code = (code - low)/_range
                    if (key == self.terminator):
                        s = key
                        break

        return result
