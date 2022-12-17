import math


def continued_fraction(n, d):
    if d == 0:
        return []
    q = n // d
    r = n - q * d
    return [q] + continued_fraction(d, r)


def convergents(n, d):
    k2, k1 = 0, 1
    d2, d1 = 1, 0
    res = []
    print(f"Непрерывная дробь {n}/{d}: {continued_fraction(n, d)}")
    for x in continued_fraction(n, d):
        k2, k1 = k1, k1 * x + k2
        d2, d1 = d1, d1 * x + d2
        res.append([k1, d1])
    return res


def wiener_attack(e, n):
    cnv = convergents(e, n)

    print(f"Подходящие дроби kn/dn: {cnv}")

    for i in cnv[2:]:
        k = i[0]
        d = i[1]

        if (e * d - 1) % k == 0:
            f = (e * d - 1) // k
            b = n - f + 1

            if b ** 2 - 4 * n > 0:
                p = (-b + math.isqrt(b ** 2 - 4 * n)) / 2
                q = (-b - math.isqrt(b ** 2 - 4 * n)) / 2
                print(f"Дискриминант больше нуля, рассмотрим корни уравнения:\n"
                      f"p = {p}\n"
                      f"q = {q}")

                if p*q == n:
                    return f"Значение d: {d}"
                else:
                    print(f"Произведение корней не равно n, переходим к следующим значениям\n")
    return 'Атака не удалась'


print("Введите параметры (e, n) открытого ключа")
inp_e, inp_n = list(map(int, input().split()))

print(wiener_attack(inp_e, inp_n))
