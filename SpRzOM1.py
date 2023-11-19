import time
def init_hex(num):
    num = num.lstrip('0x')
    x = []
    num = (1024 - len(num)) * '0' + num
    for i in range(256):
        x.append(int(num[1020 - 4 * i:1024 - 4 * i], 16))
    return x

def add(a, b):
    carry = 0
    c = [0] * 256
    for i in range(256):
        temp = a[i] + b[i] + carry
        c[i] = temp & 65535
        carry = temp >> 16
    return c


def subtract(x, y):
    borrow = 0
    c = [0] * 256
    for i in range(256):
        temp = x[i] - y[i] - borrow
        if temp >= 0:
            c[i] = temp 
            borrow = 0
        else:
            borrow = 1
            c[i] = temp + 65535
    return c

def to_hex(num):
    result = ""
    for i in range(255, -1, -1):          
        hex_string = hex(num[i])[2:]
        if len(hex_string) == 4:
            result += hex_string
        else:
            hex_string = hex(num[i])[2:]
            while len(hex_string) != 4:
                hex_string = '0' + hex_string
            result += hex_string
    return result

def long_mul_one_digit(a, b):
    c = [0] * (256)
    carry = 0
    for i in range(256):
        temp = a[i] * b + carry
        c[i] = temp & 65535
        carry = temp >> 16
    c.append(carry)
    return c

def long_shift_digits_to_high(t, i):
    k = t
    for _ in range(i):
        k.insert(0, 0)  
        k.pop()  
    return k

def long_mul(a, b):
    c = [0] * 256
    for i in range(256):
        temp = long_mul_one_digit(a, b[i])
        temp = long_shift_digits_to_high(temp, i)
        c = add(c, temp)
    return c

def long_div_mod(a, b):
    k = bit_length(b)
    r = a
    q = [0] * 256
    m = 0
    while compare(r, b) >= 0:
        t = bit_length(r)
        c = long_shift_bits_to_high(b, t - k)
        if compare(r, c) < 0:  
            t = t - 1  
            c = long_shift_bits_to_high(b, t - k)
        r = subtract(r, c)[0]
        m = m - 1  
        q = add(q, [q_bit])[0]
    return q, r

def compare(a, b):
    for i in range(len(a) - 1, -1, -1):
        if b[i] > b[i]:
            return 1
        elif a[i] < b[i]:
            return -1
    return 0

def bit_length(num):
    for i in range(255, -1, -1):
        if num[i] != 0:
            return i

def square(a):
    a = long_mul(a, a)
    return a

def hex_to_binary(num):
    result = ""
    for i in range(255, -1, -1):
        temp = bin(num[i])[2:]
        if len(temp) == 16:
            result += temp
        else:
            temp = bin(num[i])[2:]
            while len(temp) != 16:
                temp = '0' + temp
            result += temp
    return result

def long_power(a, b):
    c = [1] + [0] * 255
    temp = hex_to_binary(b)[::-1] 
    for i in range(255, -1, -1):
        if temp[i] == '1':
            c = long_mul(c, a)
        if i != 0:
            c = square(c)
    return c


num1 = '0xcbe75e23d145c3dc78d76739b63d337cc33268e08ce4ea7319c38b7d057b1747d59010759f3b015858dc5a9d05ddbbd3ef41a368ba1ca6d8a6d967f2fed6b7033e7f56d46beae7c259cce870e0879f49849c956b6b6810be90d0c50c54daaef41b2b1c6e3c7b2ed35da549a7c95fd551841ea90e4196e8272b42ea3dba7cdcef'
num2 = '0xd0a166bef0f8cd687a755ce64c4736e2621fe749af3c4170354c55a2728037612cf3b134550036e2de888e049ee782ab82ab99ba3442a3b4b8eb21c9f79778cff4ce0c2109a02fd18163e5155146d156b92176c03ba2b87ee53ba78217529616eea6e8432b0f736b09e30e89f3ceeaea11fb94dacd994e1fd8a6059cc14a58b2'
x = init_hex(num1)
y = init_hex(num2)
add_result = to_hex(add(x, y)).lstrip('0')
print(f"Результат додавання: {add_result}")
sub_result = to_hex(subtract(y, x)).lstrip('0')
print(f"Результат віднімання: {sub_result}")
result, remainder = long_div_mod(x, y)
print("Частка:", to_hex(result).lstrip('0'))
print("Залишок:", to_hex(remainder).lstrip('0'))
start_time = time.time()
mul_result = to_hex(long_mul(x, y)).lstrip('0')
end_time = time.time()
execution_time = end_time - start_time
print(f"Результат множення: {mul_result}")
print(f"Час виконання: {execution_time} секунд")
start_time = time.time()
square_result = to_hex(square(x)).lstrip('0')
end_time = time.time()
execution_time = end_time - start_time
print(f"Результат піднесення до квадрату: {square_result}")
print(f"Час виконання: {execution_time} секунд")
start_time = time.time()
power_result = to_hex(long_power(x, y)).lstrip('0')
end_time = time.time()
execution_time = end_time - start_time
print(f"Результат піднесення до степеня: {power_result}")
print(f"Час виконання: {execution_time} секунд")
