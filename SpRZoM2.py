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
        if char == 'A':
            return 10
        elif char == 'B':
            return 11
        elif char == 'C':
            return 12
        elif char == 'D':
            return 13
        elif char == 'E':
            return 14
        elif char == 'F':
            return 15
        else:
            return int(char)

    @staticmethod
    def mapDecToHex(dec):
        if dec == 10:
            return 'A'
        elif dec == 11:
            return 'B'
        elif dec == 12:
            return 'C'
        elif dec == 13:
            return 'D'
        elif dec == 14:
            return 'E'
        elif dec == 15:
            return 'F'
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


def add(num1, num2, base):
    if len(num2) > len(num1):
        num1, num2 = num2, num1
    num3 = []
    reverse([num1, num2])
    carry = 0
    for i in range(len(num1)):
        s = 0
        if len(num2) > i:
            s = num2[i]
        temp = num1[i] + s + carry
        num3.append(temp % base)
        carry = temp // base
    if carry != 0:
        num3.append(carry)
    num3.reverse()
    number3 = Number(base = base, num = num3, Type="big")
    reverse([num1, num2])
    return number3

def sub(num1, num2, base):
    num3 = []
    reverse([num1, num2])
    borrow = 0
    for i in range(len(num1)):
        s = 0
        if len(num2) > i:
            s = num2[i]
        temp = num1[i] - s - borrow
        if temp >= 0:
            num3.append(temp)
            borrow = 0
        else:
            num3.append(temp + base)
            borrow = 1
    num3.reverse()
    while(len(num3) != 0):
        if num3[0] == 0:
            del num3[0]
        else:
            break
    reverse([num1, num2])
    number3 = Number(base = base, num = num3, Type="big")
    return number3

def mul(num1, num2, base):
    if len(num2) > len(num1):
        num2, num1 = num1, num2
    num3 = []
    num2.reverse()
    for i in range(len(num2)):
        temp = mulOneDigit(num1, num2[i], base)
        temp = shiftDigitsToHigh(temp, i)
        num3 = add(temp, num3, base).numBig
    num2.reverse()
    number3 = Number(base = base, num = num3, Type="big")
    return number3

def div(num1, num2):
    k = len(num2)
    r = num1
    q = []
    while compare(r, num2):
        t = len(r)
        c = shiftDigitsToHigh(num2, t-k)
        if not compare(r,c):
            t -= 1
            c = shiftDigitsToHigh(num2, t-k)
        r = Mapper.mapDecToBin(sub(r, c, 2).numDec)
        q = insert(q, t-k)
    return q, r  

def power(num1, num2):
    num3 = [1]
    num2.reverse()
    for char in num2:
        if char == 1:
            num3 = Mapper.mapDecToBin(mul(num3, num1, 2).numDec)
        num1 = Mapper.mapDecToBin(mul(num1.copy(), num1, 2).numDec)
    return num3

def reverse(nums):
    for num in nums:
        num.reverse()

def binary_alg(num1, num2): 
    if not compare(num1, num2):
        num1, num2 = num2.copy(), num1.copy()
        a = num1.copy()
        num1 = num2.copy()
        num2 = a

    d = [1]
    while num1[-1] == 0 and num2[-1] == 0:
        
        num1 = div(num1, [1,0])[0]
        num2 = div(num2, [1,0])[0]
        print(num1, num2)
        d = Mapper.mapDecToBin(mul(d, [1,0], 2).numDec)
    while num1[-1] == 0:
        num1 = div(num1, [1,0])[0]
        if num1[0] == None:
            num1.append(0)
    while num2 != [0]:
        while num2[-1] == 0:
            num2 = div(num2, [1,0])[0]
            if num2[0] == None:
                num2.append(0)
        if compare(num1, num2):
            a = num1.copy()
            num1 = num2.copy()
            num2 =  Mapper.mapDecToBin(sub(a, num2, 2).numDec)
        else:
            num2 = Mapper.mapDecToBin(sub(num2, num1, 2).numDec)
        if len(num2) == 0:
            num2.append(0)
    d = mul(d, num1, 2)
    return d 

def lcm(num1, num2):
    if not compare(num1, num2):
        x = num1.copy()
        num1 = num2.copy()
        num2 = x
    gcd = binary_alg(num1.copy(), num2.copy())
    num1 = div(num1, Mapper.mapDecToBin(gcd.numDec))[0]
    num3 = mul(num2, num1, 2)
    return num3 

def BarrettReduction(x, n, m):
    if len(x) != 2 * len(n):
        return div(x,n)[1]
    q = KillLastDigits(x, len(n) - 1)
    q = mul(q, m, 2).numBig
    q = KillLastDigits(x, len(n) + 1)
    r = sub(x.copy(), mul(q.copy(), n.copy(), 2).numBig, 2).numBig
    print("r mod ", n, ":", r)
    while compare(r, n):
        r = sub(r, n, 2).numBig
    return r


def KillLastDigits(x, k):
    if x == None:
        return x
    for i in range(0, k):
        del x[-i+1]
    return x

def add_mod(num1, num2, mod_Bin, base):
    num4 = add(num1, num2, 2)
    num4_Bin = Mapper.mapDecToBin(num4.numDec)
    m = 2 ** len(num4_Bin)
    m_Bin = Mapper.mapDecToBin(m)
    m = div(m_Bin, mod_Bin)[0]
    num5 = BarrettReduction(num4_Bin, mod_Bin, m)
    return num5

def sub_mod(num1, num2, mod_Bin, base):
    if not compare(num1, num2):
        num1, num2 = num2, num1
    num4 = sub(num1, num2, 2)
    num4_Bin = Mapper.mapDecToBin(num4.numDec)
    m = 2 ** len(num4_Bin)
    m_Bin = Mapper.mapDecToBin(m)
    m = div(m_Bin, mod_Bin)[0]
    num5 = BarrettReduction(num4_Bin, mod_Bin, m)
    return num5  



def mul_mod(num1, num2, mod_Bin, base):
    num4 = mul(num1, num2, base)
    num4_Bin = Mapper.mapDecToBin(num4.numDec)
    m = 2 ** len(num4_Bin)
    m_Bin = Mapper.mapDecToBin(m)
    m = div(m_Bin, mod_Bin)[0]
    num5 = BarrettReduction(num4_Bin, mod_Bin, m)
    return num5 

def LongModPowerBarrett(a, b, n):
    c = [1]
    m = 2 ** (len(n))
    mBin = Mapper.mapDecToBin(m)
    m = div(mBin, n)[0]
    b.reverse()
    for i in range(0, len(b)):
        if b[i] == 1:
            c = BarrettReduction(mul(c.copy(), a.copy(), 2).numBig, n, m)
        a = BarrettReduction(mul(a.copy(), a.copy(), 2).numBig, n, m)
    return c


base = 1024
num1 = Number(base, "CBE75E23D145C3DC78D76739B63D337CC33268E08CE4EA7319C38B7D057B1747D59010759F3B015858DC5A9D05DDBBD3EF41A368BA1CA6D8A6D967F2FED6B7033E7F56D46BEAE7C259CCE870E0879F49849C956B6B6810BE90D0C50C54DAAEF41B2B1C6E3C7B2ED35DA549A7C95FD551841EA90E4196E8272B42EA3DBA7CDCEF")
num2 = Number(base, "D0A166BEF0F8CD687A755CE64C4736E2621FE749AF3C4170354C55A2728037612CF3B134550036E2DE888E049EE782AB82AB99BA3442A3B4B8EB21C9F79778CFF4CE0C2109A02FD18163E5155146D156B92176C03BA2B87EE53BA78217529616EEA6E8432B0F736B09E30E89F3CEEAEA11FB94DACD994E1FD8A6059CC14A58B2")
mod = Number(base, "247A")
num1_Bin = Mapper.mapDecToBin(num2.numDec)
num2_Bin = Mapper.mapDecToBin(num1.numDec)
modBin = Mapper.mapDecToBin(mod.numDec)
start_time = time.time()
res = add_mod(num1_Bin, num2_Bin, modBin, 2)
resDec = Mapper.mapBinToDec(res)
resNum = Number(base, resDec, "dec")
end_time = time.time()
execution_time = end_time - start_time
print("Сума двох чисел:", resNum.hex)
print(f"Час виконання: {execution_time} секунд")
start_time = time.time()
res = sub_mod(num2_Bin, num1_Bin, modBin, 2)
resDec = Mapper.mapBinToDec(res)
resNum = Number(base, resDec, "dec")
end_time = time.time()
execution_time = end_time - start_time
print("Різниця двох чисел:", resNum.hex)
print(f"Час виконання: {execution_time} секунд")
start_time = time.time()
res = mul_mod(num2_Bin, num1_Bin, modBin, 2)
resDec = Mapper.mapBinToDec(res)
resNum = Number(base, resDec, "dec")
end_time = time.time()
execution_time = end_time - start_time
print("Добуток двох чисел:", resNum.hex)
print(f"Час виконання: {execution_time} секунд")
start_time = time.time()
res = LongModPowerBarrett(num2_Bin, num1_Bin, modBin)
resDec = Mapper.mapBinToDec(res)
resNum = Number(base, resDec, "dec")
end_time = time.time()
execution_time = end_time - start_time
print("Степінь двох чисел:", resNum.hex)
print(f"Час виконання: {execution_time} секунд")
#test
a = Number(base, "1EAEDD395588036066915AF60F3F84502967BD8617DC")
b = Number(base, "1253FBED85830A10694A33E1C0DF38E62C8F6B2575B1")
c = Number(base, "1253FBEF85830A10694A33E1C0DF38E62C8F6B2575B1")
mod = Number(base, "247A")
a_Bin = Mapper.mapDecToBin(a.numDec)
b_Bin = Mapper.mapDecToBin(b.numDec)
c_Bin = Mapper.mapDecToBin(c.numDec)
mod_Bin = Mapper.mapDecToBin(mod.numDec)
a_b = add_mod(a_Bin, b_Bin, mod_Bin, 2)
a_bc = mul_mod(a_b, c_Bin, mod_Bin, 2)
ca_b = mul_mod(c_Bin, a_b, mod_Bin, 2)
ac = mul_mod(a_Bin, c_Bin, mod_Bin, 2)
bc = mul_mod(b_Bin, c_Bin, mod_Bin, 2)
ac_bc = add_mod(ac, bc, mod_Bin, 2)
if a_bc == ca_b and ca_b == ac_bc:
    print("Test completed")
else:
    print("Test not completed")


