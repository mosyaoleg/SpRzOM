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

def add(num1, num2):
    a = Mapper.mapStringToBin(num1)
    b = Mapper.mapStringToBin(num2)
    if len(a) < len(b):
        a, b = b, a
    c = []
    a.reverse()
    b.reverse()
    for i in range(len(a)):
        temp = 0
        if len(b) > i:
            temp = b[i]
        c.append((a[i] + temp) % 2)
    c.reverse()
    result = Mapper.mapBinToString(c)
    return result

def add_pol(a, b):
    if len(a) < len(b):
        a, b = a, b
    c = []
    a.reverse()
    b.reverse()
    for i in range(len(a)):
        temp = 0
        if len(b) > i:
            temp = b[i]
        c.append((a[i] + temp) % 2)
    c.reverse()
    return c

def square(num1):
    a = Mapper.mapStringToBin(num1)
    a.insert(0, a[-1])
    del a[- 1]
    return Mapper.mapBinToString(a) 

def Matrix(a): 
    m = len(a)
    p = 2 * m + 1
    mat = []
    for i in range(m):
        mat.append([])
        for j in range(m):
            if ((2 ** i) + (2 ** j)) % p == 1 or ((2 ** i) - (2 ** j)) % p == 1 or (-(2 ** i) + (2 ** j)) % p == 1 or (-(2 ** i) - (2 ** j)) % p == 1:
                mat[i].append(1)
            else:
                mat[i].append(0)
    return mat

def mul_pol(a, b): 
    mat = Matrix(a)
    d = []
    for k in range(len(a)):
        c = []
        for i in range(len(a)):
            suma = 0
            for j in range(len(a)):
                suma += a[j] * mat[j][i]
            c.append(suma % 2)
        suma = 0
        for i in range(len(c)):
            suma += c[i] * b[i]
        d.append(suma % 2)
        x = a[0]
        del a[0]
        a.append(x)
        y = b[0]
        del b[0]
        b.append(y)
    return d

def power(a, n):
    c = []
    for i in range(len(a)):
        c.append(1)
    n.reverse()
    for i in range(len(n)):
        if n[i] == 1:
            c = mul_pol(c.copy(), a.copy())
        a = Mapper.mapStringToBin(square(Mapper.mapBinToString(a.copy())))
    return c

def inverse(num1):
    a = Mapper.mapStringToBin(num1)
    m = len(a)
    n = m - 1
    n_Bin = Mapper.mapDecToBin(n)
    k = 1
    b = a.copy()
    for i in range(len(n_Bin)):
        if i == 0:
            continue
        c = Mapper.mapStringToBin(square(Mapper.mapBinToString(b.copy())))
        c = power(b.copy(), Mapper.mapDecToBin(2 ** k))
        b = mul_pol(c.copy(), b.copy())
        k = 2*k
        if n_Bin[i] == 1:
            b = Mapper.mapStringToBin(square(Mapper.mapBinToString(b.copy())))
            b = mul_pol(b.copy(), a.copy())
            k = k + 1
    b = Mapper.mapStringToBin(square(Mapper.mapBinToString(b.copy())))
    return Mapper.mapBinToString(b)


def trace(num1):
    a = Mapper.mapStringToBin(num1)
    tr = [0]
    for i in range(len(a)):
        tr = add_pol(tr.copy(), a.copy())
        a = Mapper.mapStringToBin(square(Mapper.mapBinToString(a)))
    return Mapper.mapBinToString(tr)

m = 173
num1 = "00111000010110011010001111111111111100101001011110000010010001011011111001001011110001000101010011101100000011011111100001101110110001101000001010110100110001000010100010100"
num2 = "10111000000001010000101000010001010100001111101100001010001001101110011001111100101010101011111011011101110011001001000101111110001101110011111110001110001100111001111001011"
a = Mapper.mapStringToBin(num1)
b = Mapper.mapStringToBin(num2)
start_time = time.time()
add_result = add(num1, num2)
end_time = time.time()
execution_time = end_time - start_time
print("Сума:", add_result)
print(f"Час виконання: {execution_time} секунд")
start_time = time.time()
mul_result = mul_pol(a, b)
result = Mapper.mapBinToString(mul_result)
end_time = time.time()
execution_time = end_time - start_time
print("Добуток:", result)
print(f"Час виконання: {execution_time} секунд")
start_time = time.time()
square_result = square(num1)
end_time = time.time()
execution_time = end_time - start_time
print("Квадрат:", square_result)
print(f"Час виконання: {execution_time} секунд")
start_time = time.time()
trace_result = trace(num1)
end_time = time.time()
execution_time = end_time - start_time
print("Слід:", trace_result)
print(f"Час виконання: {execution_time} секунд")
start_time = time.time()
inverse_result = inverse(num1)
end_time = time.time()
execution_time = end_time - start_time
print("Обернений:", inverse_result)
print(f"Час виконання: {execution_time} секунд")
start_time = time.time()
num3 = "00010101111010100111101110111010001111100000001011111000001000100110101000111101110111001100111000001001111001100110101011011000110111111000011100011000111101010110100100100"
n = Mapper.mapStringToBin(num3)
power_result = power(a, n)
result = Mapper.mapBinToString(power_result)
end_time = time.time()
execution_time = end_time - start_time
print("Степінь:", result)
print(f"Час виконання: {execution_time} секунд")

