import math
import time
class Number:
    def __init__(self, base, num, Type="hex"):
        self.base = base
        if Type == "hex":
            self.hex = num
            self.getDec()
            self.getBig()
        elif Type == "dec":
            self.numDec = num
            self.getBig()
            self.getHex()
        elif Type == "big":
            self.numBig = num
            self.getDecFromBig()
            self.getHex()
        else:
            print("Помилка: проблема з поданням числа(оберіть іншу систему числення)")

    def getDec(self):
        num = self.hex[::-1]
        numDec = 0
        i = 0
        for char in num:
            numDec += Mapper.mapHexToDec(char) * int(pow(16, i))
            i += 1
        self.numDec = numDec

    def getHex(self):
        num = self.numDec
        numHex = ""
        while num > 0:
            numHex += Mapper.mapDecToHex(num % 16)
            num = num // 16
        self.hex = numHex[::-1]

    def getDecFromBig(self):
        num = self.numBig
        num.reverse()
        numDec = 0
        i = 0
        for n in num:
            numDec += n * int(self.base ** i)
            i += 1
        self.numDec = int(numDec)
        self.numBig.reverse()

    def getBig(self):
        num = self.numDec
        numBig = []
        while num > 0:
            numBig.append(num % self.base)
            num = num // self.base
        numBig.reverse()
        self.numBig = numBig

class Mapper:

    @staticmethod
    def mapHexToDec(char):
        if char == 'a':
            return 10
        elif char == 'b':
            return 11
        elif char == 'c':
            return 12
        elif char == 'd':
            return 13
        elif char == 'e':
            return 14
        elif char == 'f':
            return 15
        else:
            return int(char)

    @staticmethod
    def mapDecToHex(dec):
        if dec == 10:
            return 'a'
        elif dec == 11:
            return 'b'
        elif dec == 12:
            return 'c'
        elif dec == 13:
            return 'd'
        elif dec == 14:
            return 'e'
        elif dec == 15:
            return 'f'
        else:
            return str(dec)

    @staticmethod
    def mapDecToBin(dec):
        binary = ""
        while dec > 0:
            binary = str(dec % 2) + binary
            dec = dec // 2
        num_Bin = []
        for b in binary:
            num_Bin.append(int(b))
        return num_Bin

    @staticmethod
    def mapBinToDec(num_Bin):
        num_Bin.reverse()
        num_Dec = 0
        i = 0
        for char in num_Bin:
            num_Dec += char * int(2 ** i)
            i += 1
        return num_Dec

    @staticmethod
    def mapHexToBin(num_Hex):
        num_Bin = []
        for char in num_Hex:
            num_Bin.append(int(char))
        return num_Bin
    
    @staticmethod
    def mapBinToHex(num):
        num_Hex = ""
        for bit in num:
            num_Hex += str(bit)
        return num_Hex

    @staticmethod
    def mapStringToBin(num_str):
        num_Bin = []
        for char in num_str:
            num_Bin.append(int(char))
        return num_Bin
    
    @staticmethod
    def mapBinToString(num):
        num_str = ""
        for bit in num:
            num_str += str(bit)
        return num_str

def insert(num, p):
    if len(num) <= p:
        num.append(1)
        num  = shiftDigitsToHigh(num, p)
    else:
        num.reverse()
        num[p] = 1
        num.reverse()
    return num


def compare(num1, num2):
    if len(num1) > len(num2):
        return True
    elif len(num1) < len(num2):
        return False
    else:
        for i in range(len(num2)):
            if num1[i] > num2[i]:
                return True
            if num1[i] < num2[i]:
                return False
        return True

def reverse(nums):
    for num in nums:
        num.reverse()


def shiftDigitsToHigh(num, c):
    new_Num = num.copy()
    for i in range(c):
        new_Num.append(0)
    return new_Num

def mulOneDigit(num1, a, base):
    num1.reverse()
    carry = 0
    result = []
    for i in range(len(num1)):
        temp = num1[i] * a + carry
        result.append(temp % base)
        carry = temp // base
    if carry != 0:
        result.append(carry)
    reverse([result, num1])
    return result

def poly_to_GF2_vector(poly_coefficients):
    vector_size = max(poly_coefficients) + 1
    vector = 0

    for coef in poly_coefficients:
        vector |= 1 << coef

    return bin(vector)[2:].zfill(vector_size)

def GF2_vector_to_poly(vector):
    vector = int(vector, 2)
    coefficients = []

    while vector:
        degree = vector.bit_length() - 1
        coefficients.append(degree)
        vector ^= 1 << degree

    return coefficients

def add_pol(a, b):
    if len(a) < len(b):
        a, b = b, a
    result = []
    a.reverse()
    b.reverse()
    for i in range(len(a)):
        temp = 0
        if len(b) > i:
            temp = b[i]
        result.append((a[i] + temp) % 2)
    result.reverse()
    return result

def mul_pol(a, b, base):
    if len(a) > len(b):
        a, b = b, a
    result = []
    b.reverse()
    for i in range(len(b)):
        temp = mulOneDigit(a, b[i], base)
        temp = shiftDigitsToHigh(temp, i)
        result = add_pol(temp, result)
    return result

def div_pol(a, b):
    k = len(b)
    r = a
    q = []
    while compare(r, b):
        t = len(r)
        c = shiftDigitsToHigh(b, t-k)
        r = add_pol(r, c)
        q = insert(q, t-k)
        while(len(r) != 0):
            if r[0] == 0:
                del r[0]
            else:
                break
    return q, r

def square_pol(a, gen):
    for i in range(len(a) - 1):
        a.insert(i*2 + 1, 0)
    result = div_pol(a.copy(), gen)[1]
    return result

def add(num1, num2):
    a = Mapper.mapStringToBin(num1)
    b = Mapper.mapStringToBin(num2)
    if len(a) < len(b):
        a, b = b, a
    result = []
    a.reverse()
    b.reverse()
    for i in range(len(a)):
        temp = 0
        if len(b) > i:
            temp = b[i]
        result.append((a[i] + temp) % 2)
    result.reverse()
    vector = Mapper.mapBinToString(result)
    return vector

def mul(num1, num2, gen, m):
    a = Mapper.mapStringToBin(num1)
    b = Mapper.mapStringToBin(num2)
    p = Mapper.mapStringToBin(gen)
    d = mul_pol(a, b, 2)
    e = div_pol(d, p)[1]
    while(len(e) > m):
        del e[0]
    result = Mapper.mapBinToString(e)
    return result

def trace(num1, gen, m):
    a = Mapper.mapStringToBin(num1)
    p = Mapper.mapStringToBin(gen)
    result = [0]
    for i in range(0, m):
        result = add_pol(result.copy(), a.copy())
        a = square_pol(a.copy(), p.copy())
    vector = Mapper.mapBinToString(result)
    return vector

def power(num1, power, gen):
    a = Mapper.mapStringToBin(num1)
    n = Mapper.mapStringToBin(power)
    p = Mapper.mapStringToBin(gen)
    b = [1]
    n.reverse()
    for i in range(len(n)):
        if n[i] == 1:
            b = mul_pol(b.copy(), a.copy(), 2)
            b = div_pol(b.copy(), p)[1]
        a = square_pol(a.copy(), p)
        a = div_pol(a.copy(), p)[1]
    result = Mapper.mapBinToString(b)
    return result

def inverse(num1, gen, m):
    n = (2 ** m) - 2
    n_Bin = Mapper.mapDecToBin(n)
    result = Mapper.mapBinToString(n_Bin)
    return power(num1, result, gen)


m = 173
poly_coefficients = [173, 10, 2, 1, 0]
gen = poly_to_GF2_vector(poly_coefficients)
num1 = "00110100010011010100111110100011110100001001010000001101010101000010001000100011010001111110110010110000010101010100011110111100001110010010111100111110110001101111111001110"
num2 = "01010110011010101001111011111101011110110010101000100110000111110011100101101001111110111010000010001001111000000011111110110110101000011101100000001011110111011000000101001"
start_time = time.time()
add_result = add(num1, num2)
end_time = time.time()
execution_time = end_time - start_time
print("Сума:", add_result)
print(f"Час виконання: {execution_time} секунд")
start_time = time.time()
mul_result = mul(num1, num2, gen, m)
end_time = time.time()
execution_time = end_time - start_time
print("Добуток:", mul_result)
print(f"Час виконання: {execution_time} секунд")
start_time = time.time()
a = Mapper.mapStringToBin(num1)
p = Mapper.mapStringToBin(gen)
square = square_pol(a, p)
square_result = Mapper.mapBinToString(square)
end_time = time.time()
execution_time = end_time - start_time
print("Квадрат:", square_result)
print(f"Час виконання: {execution_time} секунд")
start_time = time.time()
trace_ = trace(num1, gen, m)
trace_result = GF2_vector_to_poly(trace_)
end_time = time.time()
execution_time = end_time - start_time
print("Слід:", trace_result)
print(f"Час виконання: {execution_time} секунд")
start_time = time.time()
inverse_result = inverse(num1, gen, m)
end_time = time.time()
execution_time = end_time - start_time
print("Обернений:", inverse_result)
print(f"Час виконання: {execution_time} секунд")
start_time = time.time()
n = "00110111110100001101010111000110110000111111010100011000010111010101010011111000101111101010110000001110011011001011010110001110100101011100000001001011001011100000101011010"
power_result = power(num1, n, gen)
end_time = time.time()
execution_time = end_time - start_time
print("Степінь:", power_result)
print(f"Час виконання: {execution_time} секунд")

#test
num1 = "01110110000100100110000110110100100010001111110001100011010101001010010011111101000000011010110011110011010110011001101101101010010101100011001100000011011000110010100011010"
num2 = "11000111010000011110110011111010011011101110100000011000110111011001011001111110000110000111010110100110011010100001011110010110011111101100100001001001000010001010000100000"
num3 = "10100000011000100110011110011110010001110010101011000001011010000111111011000101010110001101010110000001101011010010110101010001001110011001110110011101111000101001000001111"
a = Mapper.mapStringToBin(num1)
b = Mapper.mapStringToBin(num2)
c = Mapper.mapStringToBin(num3)   
a_b = add_pol(a.copy(), b.copy())
a_bc = mul(Mapper.mapBinToString(a_b), num3, gen, m)
ac = mul(num1, num3, gen, m)
bc = mul(num2, num3, gen, m)
ac_bc = add(ac, bc)
if a_bc == ac_bc:
    print("Test completed")
else:
    print("Test not completed")


