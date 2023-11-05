import time
class BigInt:
    def __init__(self, value=0):
        self.value = value
        self.digits = list(str(value))

    def __str__(self):
        return str(self.value)

    @classmethod
    def from_string(cls, string_value):
        value = int(string_value)
        return cls(value)

    @classmethod
    def from_small(cls, small_value):
        return cls(small_value)

    def add(self, other):
        num1 = self.digits[::-1]
        num2 = list(str(other.value))[::-1]
        max_len = max(len(num1), len(num2))
        result = []
        carry = 0
        for i in range(max_len):
            digit1 = int(num1[i]) if i < len(num1) else 0
            digit2 = int(num2[i]) if i < len(num2) else 0
            total = digit1 + digit2 + carry
            carry = total // 10
            result.append(total % 10)

        if carry:
            result.append(carry)

        result = int(''.join(map(str, result[::-1])))
        return BigInt(result)

    def subtract(self, other):
        num1 = self.digits[::-1]
        num2 = list(str(other.value))[::-1]
        max_len = max(len(num1), len(num2))
        result = []
        borrow = 0
        for i in range(max_len):
            digit1 = int(num1[i]) if i < len(num1) else 0
            digit2 = int(num2[i]) if i < len(num2) else 0
            diff = digit1 - digit2 - borrow
            if diff < 0:
                diff += 10
                borrow = 1
            else:
                borrow = 0

            result.append(diff)

        result = int(''.join(map(str, result[::-1])))
        return BigInt(result)

    def multiply(self, other):
        result = BigInt(0)
        current = BigInt(self.value)
        while other.value > 0:
            result = result.add(current)
            other = other.subtract(BigInt(1))
        return result

    def karatsuba_multiply(self, other):
        if self.value < 10 or other.value < 10:
            return BigInt(self.value * other.value)

        n = max(len(self.digits), len(other.digits))
        half = n // 2
        a = BigInt(int(''.join(map(str, self.digits[:-half]))))
        b = BigInt(int(''.join(map(str, self.digits[-half:]))))
        c = BigInt(int(''.join(map(str, other.digits[:-half]))))
        d = BigInt(int(''.join(map(str, other.digits[-half:]))))
        ac = a.karatsuba_multiply(c)
        bd = b.karatsuba_multiply(d)
        ad_bc = (a.add(b)).karatsuba_multiply(c.add(d)).subtract(ac).subtract(bd)
        result = ac.multiply(BigInt(10**(2*half))).add(ad_bc.multiply(BigInt(10**half))).add(bd)
        return result

    def square(self):
        return self.karatsuba_multiply(self)
      
    def long_division(self, other):
        num1_str = "".join(map(str, self.digits))
        num2_str = "".join(map(str, other.digits))
        quotient = 0
        remainder = 0
        for i in range(len(num1_str)):
            current_digit = int(num1_str[i])
            current_value = remainder * 10 + current_digit
            current_quotient = current_value // int(num2_str)
            quotient = quotient * 10 + current_quotient
            remainder = current_value % int(num2_str)

        return BigInt(quotient), BigInt(remainder)

    def power(self, exp):
        if exp == 0:
            return BigInt(1)
        if exp == 1:
            return self

        result = BigInt(1)
        base = self

        while exp > 0:
            if exp % 2 == 1:
                result = result.karatsuba_multiply(base)
            base = base.karatsuba_multiply(base)
            exp = exp // 2

        return result

    def to_hex(self):
        return hex(self.value)

    def to_binary(self):
        return bin(self.value)

    @classmethod
    def from_hex(cls, hex_string):
        value = int(hex_string, 16)
        return cls(value)

    @classmethod
    def from_binary(cls, binary_string):
        value = int(binary_string, 2)
        return cls(value)

num1 = BigInt(12347)
num2 = BigInt(56789)
base = BigInt(123)
exp = 3
print("Введені числа", num1, num2)
small_number = 0
big_number = BigInt.from_small(small_number)
print(f"Велике число: {big_number}")
add_result = num1.add(num2)
print(f"Результат додавання: {add_result}")
sub_result = num1.subtract(num2)
print(f"Результат віднімання: {sub_result}")
result, remainder = num2.long_division(num1)
print(f"Частка: {result}")
print(f"Залишок: {remainder}")
start_time = time.time()
mul_result = num1.karatsuba_multiply(num2)
end_time = time.time()
execution_time = end_time - start_time
print(f"Результат множення: {mul_result}")
print(f"Час виконання: {execution_time} секунд")
start_time = time.time()
square_result = BigInt.square(num1)
end_time = time.time()
execution_time = end_time - start_time
print(f"Результат піднесення до квадрату: {square_result}")
print(f"Час виконання: {execution_time} секунд")
hex_add = BigInt.to_hex(add_result)
binary_sub = BigInt.to_binary(sub_result)
from_hex_add = BigInt.from_hex(hex_add)
from_binary_sub = BigInt.from_binary(binary_sub)
print(f"Результат додавання в шістнадцятковому вигляді: {hex_add}")
print(f"Результат віднімання в бінарному вигляді: {binary_sub}")
print(f"Результат додавання в десятковому вигляді: {from_hex_add}")
print(f"Результат віднімання в десятковому вигляді: {from_binary_sub}")
print("Основа і степінь до якого підносимо", base, exp)
start_time = time.time()
power_result = BigInt.power(base, exp)
end_time = time.time()
execution_time = end_time - start_time
print(f"Результат піднесення до степеня: {power_result}")
print(f"Час виконання: {execution_time} секунд")
# Тест 1: Перевірка додавання та множення
a = BigInt(153)
b = BigInt(513)
c = BigInt(315)
result1 = (a.add(b)).karatsuba_multiply(c)
result2 = a.karatsuba_multiply(c).add(b.karatsuba_multiply(c))
print("Test 1")
print(f"Результат виконання операції: {result1}")
print(f"Очікуваний результат: {result2}")
# Тест 2: Перевірка ділення та множення
a = BigInt(72)
n = BigInt(20)
result1 = n.karatsuba_multiply(a)
result2 = a
for i in range(1, 20):
    result2 = result2.add(a)

print("Test 2")
print(f"Результат виконання операції: {result1}")
print(f"Очікуваний результат: {result2}")
