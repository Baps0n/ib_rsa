import base64
import json
import math
import random


def gcd_euclidean(a, b):
    x2 = 1
    x1 = 0
    y2 = 0
    y1 = 1
    while b > 0:
        q = a // b
        r = a - q * b
        x = x2 - q * x1
        y = y2 - q * y1
        a = b
        b = r
        x2 = x1
        x1 = x
        y2 = y1
        y1 = y
        print(a, y2, y1)
    return {'gcd': a, 'x': x2, 'y': y2}


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def is_prime_ferma(n):
    for i in range(100):
        a = random.randint(2, n-1)
        if pow(a, n-1, n) != 1:
            return False
    return True


def pow_mod(a, k, n):
    b = 1
    if k == 0:
        return b
    k = bin(k)[2:]
    if k[0] == '1':
        b = a
    for i in k[1:]:
        a = (a**2) % n
        if i == '1':
            b = (a * b) % n
    return b


def gen_prime(p_len):
    for i in range(1000000):
        a = random.randrange(2 ** (p_len - 1) + 1, 2 ** p_len - 1)
        if a % 2 != 0:
            if is_prime_ferma(a):
                return a


def gen_prime_pair(p_len):
    p = 0
    for i in range(1000000):
        p = random.randrange(2 ** (p_len//2 + 1) + 1, 2 ** (p_len//2+2) - 1)
        if p % 2 != 0:
            if is_prime_ferma(p):
                break

    for i in range(1000000):
        q = random.randrange(2 ** (p_len//2 - 3) + 1, 2 ** (p_len//2-2) - 1)
        if q % 2 != 0:
            if is_prime_ferma(q):
                # print(p,q)
                if len(bin(p*q)[2:]) == p_len:
                    # print(p,q)
                    return [p, q]


def gen_d(pq, e):
    p = pq[0]
    q = pq[1]
    n = p * q
    f_euler = (p - 1) * (q - 1)
    print('FFFF', f_euler)
    d = gcd_euclidean(max(f_euler, e), min(f_euler, e))['y']
    if d < 0:
        d = max(f_euler, e) + d
    # print('gen_d', pq, e, f_euler, d)
    return d


def convert_data(inp, n):
    inp = ''.join([format(ord(i), "02x") for i in inp])

    block_size = len(hex(n)[2:])
    # inp_s = [inp[i:i+block_size] for i in range(0, len(inp), block_size)]
    cur = 0
    inp_s = []
    while cur < len(inp)-1:
        block = inp[cur:cur+block_size]
        if int(block, 16) > n-1:
            cur -= 1
            block = block[:-1]
        inp_s.append(block)
        cur += block_size
    # if len(inp_s[-1]) < block_size:
    #     inp_s[-1] += str('0' * (block_size - len(inp_s[-1])))
    # print('c', inp_s)
    return inp_s


def data_to_unicode(data, n):
    res = []
    # print('UN', data)
    if len(data) % 2 == 1:
        data += '0'

    for i in range(0, len(data), 2):
        res.append(chr(int(data[i] + data[i+1], 16)))
    # print(res)
    return ''.join(res)

# def rsa_encode(data, e, n):
#     return ''.join([chr(pow_mod(ord(i), e, n)) for i in data])


# def rsa_decode(enc_data, d, n):
#     return ''.join([chr(pow_mod(ord(i), d, n)) for i in enc_data])


def rsa_encode(data, e, n):
    data = convert_data(data, n)
    res = []
    for i in data:
        res_i = hex(pow(int(i, 16), e, n))[2:]
        res.append('0' * (len(hex(n)[2:]) - len(res_i)) + str(res_i))
    # print('e', res)
    return data_to_unicode(''.join(res), n)


def rsa_decode(enc_data, d, n):
    enc_data = convert_data(enc_data, n)
    res = []
    for i in enc_data:
        res_i = hex(pow(int(i, 16), d, n))[2:]
        res.append(str(res_i))
    # print('d', res)
    return data_to_unicode(''.join(res), n)


def main():
    print("Выберите тип операции, введя её номер:\n"
          "1. Шифрование\n"
          "2. Расшифрование\n"
          "3. Генерация ключевой пары")
    operation = input()
    while '1' not in operation and '2' not in operation and '3' not in operation:
        print("Ввод некорректен. Введите номер типа операции")
        operation = input()

    if '3' in operation:
        print("Введите желаемую битовую длину модуля")
        bit_len = int(input())
        pq = gen_prime_pair(bit_len)
        n = pq[0]*pq[1]
        f_euler = (pq[0]-1)*(pq[1]-1)
        n = base64.b64encode(str(n).encode("UTF-8")).decode("UTF-8")
        print(f"Сгенерированный модуль n: {n}")
        print("Введите значение e:")
        e = int(input())
        while gcd_euclidean(e, f_euler)["gcd"] != 1:
            print("Введенное значение e не является взаимно простым с модулем n. Введите другое число")
            e = int(input())

        d = gen_d(pq, e)

        print(f"Ключевая пара (e,n):\n"
              f"({base64.b64encode(str(e).encode('UTF-8')).decode('UTF-8')}, {n}")
        print(f"Ключевая пара (d,n):\n"
              f"({base64.b64encode(str(d).encode('UTF-8')).decode('UTF-8')}, {n}")

        # key_pairs = f"(e,n) = ({base64.b64encode(str(e).encode('UTF-8')).decode('UTF-8')}, {n})\n" \
        #             f"(d,n) = ({base64.b64encode(str(d).encode('UTF-8')).decode('UTF-8')}, {n})"

        keys = {'e': base64.b64encode(str(e).encode('UTF-8')).decode('UTF-8'),
                'd': base64.b64encode(str(d).encode('UTF-8')).decode('UTF-8'),
                'n': n}
        with open("keys.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(keys, indent=4))
            print("Ключи записаны в файл keys.json")

        print("Выполнить шифрование используя полученную ключевую пару?\n"
              "1. Да\n"
              "2. Нет, выйти из программы")
        quit_enc = input()
        while '1' not in quit_enc and '2' not in quit_enc:
            print("Ввод некорректен. Введите номер операции")
            quit_enc = input()

        if '1' in quit_enc:
            operation = '1'

        if '2' in quit_enc:
            return 'Завершение работы'

    print("Выберите режим считывания/записи данных, введя его номер:\n"
          "1. Консоль\n"
          "2. Файлы")
    read_mode = input()
    while '1' not in read_mode and '2' not in read_mode:
        print("Ввод некорректен. Введите номер режима")
        read_mode = input()

    e = 1
    d = 1
    n = 1
    if '1' in read_mode:
        if '1' in operation:
            print("Введите открытый ключ")
            key = list(input().split())
            e = int(base64.b64decode(str(key[0]).encode("UTF-8")).decode("UTF-8"))
            n = int(base64.b64decode(str(key[1]).encode("UTF-8")).decode("UTF-8"))
            print("Введите открытый текст")
        if '2' in operation:
            print("Введите закрытый ключ")
            key = list(input().split())
            d = int(base64.b64decode(str(key[0]).encode("UTF-8")).decode("UTF-8"))
            n = int(base64.b64decode(str(key[1]).encode("UTF-8")).decode("UTF-8"))
            print("Введите шифртекст")
        inp = input()

    if '2' in read_mode:
        inp_f = "in.txt"
        with open(inp_f, "r", encoding="utf-8") as f:
            inp = f.read()
        keys_f = "keys.json"
        with open(keys_f, "r", encoding="utf-8") as f:
            keys = json.loads(f.read())

        if '1' in operation:
            print(f"Открытый текст считан из файла {inp_f}: {inp}")
        if '2' in operation:
            print(f"Шифртекст считан из файла {inp_f}: {inp}")

        e = int(base64.b64decode(str(keys['e']).encode("UTF-8")).decode("UTF-8"))
        d = int(base64.b64decode(str(keys['d']).encode("UTF-8")).decode("UTF-8"))
        n = int(base64.b64decode(str(keys['n']).encode("UTF-8")).decode("UTF-8"))
        print(f"Ключи считаны из файла {keys_f}")

    res = ''
    if '1' in operation:
        print(e, n)
        res = rsa_encode(inp, e, n)
    if '2' in operation:
        print(d, n)
        res = rsa_decode(inp, d, n)

    if '1' in operation:
        print(f"Полученный шифртекст:\n"
              f"{res}")
    if '2' in operation:
        print(f"Полученный открытый текст:\n"
              f"{res}")

    if '2' in read_mode:
        out_f = "out.txt"
        with open("out.txt", "w", encoding="utf-8") as f:
            f.write(res)

        if '1' in operation:
            print(f"Полученный шифртекст записан в файл {out_f} : {res}")
        if '2' in operation:
            print(f"Полученный открытый текст записан в файл {out_f} : {res}")


if __name__ == '__main__':
    main()
