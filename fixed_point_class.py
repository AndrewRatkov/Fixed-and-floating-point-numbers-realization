from basic_functions import *
import sys

class FixedPointNum:
    def __init__(self, a: int, b: int, code: list[int], rounding: int):
        if LOCAL_DEBUG:
#            assert len(code) <= a + b
            for i in range(len(code)):
                assert code[i] == 0 or code[i] == 1
            assert rounding in range(4)
        self.a = a
        self.b = b
        if len(code) <= a + b:
            self.code = [0 for _ in range(a + b - len(code))] # подразумевается, что len(code) <= a + b
            self.code.extend(code)
        else:
            self.code = code[-(a+b):] # берём последние a+b бит
        self.rounding = rounding
        self.integer = 0
        p = 1
        for el in self.code[:0:-1]:
            self.integer += p * el
            p <<= 1
        self.integer -= p * self.code[0]

    def __add__(self, other):
        if LOCAL_DEBUG:
            assert isinstance(other, FixedPointNum), "Types should be equal"
            assert other.a == self.a and other.b == self.b and self.rounding == other.rounding, "Types should be equal"
        new_int = self.integer + other.integer
        return FixedPointNum(self.a, self.b, int2code2(new_int, self.a + self.b), self.rounding)

    def __sub__(self, other):
        if LOCAL_DEBUG:
            assert isinstance(other, FixedPointNum), "Types should be equal"
            assert other.a == self.a and other.b == self.b and self.rounding == other.rounding, "Types should be equal"
        new_int = self.integer - other.integer
        return FixedPointNum(self.a, self.b, int2code2(new_int, self.a + self.b), self.rounding)

    def __mul__(self, other):
        if LOCAL_DEBUG:
            assert isinstance(other, FixedPointNum), "Types should be equal"
            assert other.a == self.a and other.b == self.b and self.rounding == other.rounding, "Types should be equal"
        new_int = self.integer * other.integer

        if self.rounding == Rounding_TOWARD_ZERO: # changed after deadline
            if new_int >= 0:
                new_int >>= self.b
            else:
                new_int = -((abs(new_int)) >> self.b)
        elif self.rounding == Rounding_TOWARD_INFINITY:
            new_int = -((-new_int) // (1 << self.b))
        elif self.rounding == Rounding_TOWARD_NEG_INFINITY:
            new_int //= (1 << self.b)
        else:
            inv = False
            if new_int < 0:
                inv = True
                new_int *= -1
            if (new_int % (1 << self.b)) * 2 > (1 << self.b):
                new_int >>= self.b
                new_int += 1
            elif (new_int % (1 << self.b)) * 2 == (1 << self.b):
                new_int >>= self.b
                new_int += (new_int % 2)
            else:
                new_int >>= self.b
            if inv:
                new_int *= -1
        new_int %= (1 << (self.a + self.b))
        return FixedPointNum(self.a, self.b, int2code2(new_int, self.a + self.b), self.rounding)

    def __truediv__(self, other):
        if LOCAL_DEBUG:
            assert isinstance(other, FixedPointNum), "Types should be equal"
            assert other.a == self.a and other.b == self.b and self.rounding == other.rounding, "Types should be equal"

        if other.integer == 0: # new case
            print("Division by zero", file=sys.stderr)
            return
        if self.integer == 0:
            return FixedPointNum(self.a, self.b, int2code2(0, self.a + self.b), self.rounding)



        if self.rounding == Rounding_TOWARD_ZERO:
            if self.is_neg() == other.is_neg():
                new_int = (abs(self.integer) << self.b) // abs(other.integer)
            else:
                new_int = -((abs(self.integer) << self.b) // abs(other.integer))
        elif self.rounding == Rounding_NEAREST_EVEN:
            new_int = (abs(self.integer) << self.b) // abs(other.integer)
            if 2 * ((abs(self.integer) << self.b) % abs(other.integer)) > abs(other.integer):
                new_int += 1
            elif 2 * ((abs(self.integer) << self.b) % abs(other.integer)) == abs(other.integer) and new_int % 2 == 1:
                new_int += 1
            if self.is_neg() != other.is_neg():
                new_int *= -1
        elif self.rounding == Rounding_TOWARD_INFINITY:
            if self.is_neg() != other.is_neg():
                new_int = -((abs(self.integer) << self.b) // abs(other.integer))
            else:
                new_int = (abs(self.integer) << self.b) // abs(other.integer)
                if abs(self.integer) % abs(other.integer) > 0:
                    new_int += 1
        else:
            if self.is_neg() == other.is_neg():
                new_int = (abs(self.integer) << self.b) // abs(other.integer)
            else:
                new_int = -((abs(self.integer) << self.b) // abs(other.integer))
                if abs(self.integer) % abs(other.integer) > 0:
                    new_int -= 1

        return FixedPointNum(self.a, self.b, int2code2(new_int, self.a + self.b), self.rounding)

    def is_neg(self):
        return self.code[0] == 1

    def __str__(self):
        first_part = 0  # округлённое вверх число (если оно отрицательное), иначе просто целая часть числа
        for i in range(self.a - 1, 0, -1):
            first_part += self.code[i] * (1 << (self.a - 1 - i))
        first_part -= self.code[0] * (1 << (self.a - 1))
        second_part = 0
        for i in range(self.a, self.a + self.b):
            second_part += self.code[i] * (1 << self.a + self.b - i - 1)
        second_part *= (5 ** self.b)
        if self.is_neg():
            if second_part > 0:
                second_part = (10 ** self.b) - second_part
                first_part += 1
        first_nulls = self.b - len(str(second_part))
        if first_nulls >= 3:
            rounded_second_part = "000"
        else:
            rounded_second_part = "0" * first_nulls + str(second_part)[:3 - first_nulls]

        def increase(after_dot, before_dot):
            if after_dot != "999":
                after_dot = str(int(after_dot) + 1)
                after_dot = "0" * (3 - len(after_dot)) + after_dot
            else:
                after_dot = "000"
                before_dot += 1
            return after_dot, before_dot

        def decrease(after_dot, before_dot):
            if after_dot != "999":
                after_dot = str(int(after_dot) + 1)
                after_dot = "0" * (3 - len(after_dot)) + after_dot
            else:
                after_dot = "000"
                before_dot -= 1
            return after_dot, before_dot

        def has_not_0(s: str):
            for c in s:
                if c != '0':
                    return True
            return False

        if self.rounding == Rounding_TOWARD_ZERO:
            if self.is_neg() and first_part == 0 and rounded_second_part != "000": # у отрицательных чисел больше: -1 first_part = 0, поэтому для них надо отдельно писать минус в начале
                return '-' + str(first_part) + '.' + rounded_second_part + '0' * (3 - len(rounded_second_part))
            return str(first_part) + '.' + rounded_second_part + '0' * (3 - len(rounded_second_part))

        elif self.rounding == Rounding_TOWARD_INFINITY:
            if self.is_neg(): # округлять отрицательные числа к плюс бесконечности - то же самое, что к 0
                if first_part == 0 and rounded_second_part != "000": # у отрицательных чисел больше: -1 first_part = 0, поэтому для них надо отдельно писать минус в начале
                    return '-' + str(first_part) + '.' + rounded_second_part + '0' * (3 - len(rounded_second_part))
                return str(first_part) + '.' + rounded_second_part + '0' * (3 - len(rounded_second_part))
            else:
                if len(str(second_part)) > 3 - first_nulls and has_not_0(str(second_part)[3 - first_nulls:]): # если есть что-то после трёх цифр после запятой, то надо увеличивать
                    rounded_second_part, first_part = increase(rounded_second_part, first_part)
                return str(first_part) + '.' + rounded_second_part + '0' * (3 - len(rounded_second_part))

        elif self.rounding == Rounding_TOWARD_NEG_INFINITY:
            if self.is_neg():
                if len(str(second_part)) > 3 - first_nulls and has_not_0(str(second_part)[3 - first_nulls:]): # если есть что-то после трёх цифр после запятой, то надо уменьшать
                    rounded_second_part, first_part = decrease(rounded_second_part, first_part)
                if first_part == 0:  # все отрицательные числа при округлении к - бесконечности остаются отрицательными
                    return '-' + str(first_part) + '.' + rounded_second_part + '0' * (3 - len(rounded_second_part))
                return str(first_part) + '.' + rounded_second_part + '0' * (3 - len(rounded_second_part))
            else: # округлять положительные числа к минус бесконечности - то же самое, что к нулю
                return str(first_part) + '.' + rounded_second_part + '0' * (3 - len(rounded_second_part))

        else: # округление к ближайшему чётному
            str_second_part = str(second_part)
            if self.is_neg():
                if first_nulls <= 3 and len(str_second_part) > 3 - first_nulls:
                    if str_second_part[3 - first_nulls] == '5':
                        if has_not_0(str_second_part[4 - first_nulls:]): # проверка на наличие ненулевых символов дальше
                            rounded_second_part, first_part = decrease(rounded_second_part, first_part)
                        else:
                            if int(rounded_second_part) % 2 == 1:
                                rounded_second_part, first_part = decrease(rounded_second_part, first_part)
                    elif str_second_part[3 - first_nulls] > '5':
                        rounded_second_part, first_part = decrease(rounded_second_part, first_part)
                if first_part == 0 and rounded_second_part != "000": # у отрицательных чисел больше: -1 first_part = 0, поэтому для них надо отдельно писать минус в начале
                    return '-' + str(first_part) + '.' + rounded_second_part + '0' * (3 - len(rounded_second_part))
                return str(first_part) + '.' + rounded_second_part + '0' * (3 - len(rounded_second_part))
            else:
                if first_nulls <= 3 and len(str_second_part) > 3 - first_nulls:
                    if str_second_part[3 - first_nulls] == '5':
                        if has_not_0(str_second_part[4 - first_nulls:]): # проверка на наличие ненулевых символов дальше
                            rounded_second_part, first_part = increase(rounded_second_part, first_part)
                        else:
                            if int(rounded_second_part) % 2 == 1:
                                rounded_second_part, first_part = increase(rounded_second_part, first_part)
                    elif str_second_part[3 - first_nulls] > '5':
                        rounded_second_part, first_part = increase(rounded_second_part, first_part)
                return str(first_part) + '.' + rounded_second_part + '0' * (3 - len(rounded_second_part))
