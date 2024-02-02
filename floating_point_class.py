from basic_functions import *

class FloatNum:
    def __init__(self, code: list[int], rounding: int, half_or_float: bool): # half_or_float: False -> half, True -> float
        if not half_or_float:
            self.EXP_LEN = 5
            self.MANT_LEN = 10
            self.MAX_EXP = 16
            self.MIN_EXP = -14
            self.LEN = 16
            self.EXP_SHIFT = 15
            self.OUTPUT_BYTES = 3
        else:
            self.EXP_LEN = 8
            self.MANT_LEN = 23
            self.MAX_EXP = 128
            self.MIN_EXP = -126
            self.LEN = 32
            self.EXP_SHIFT = 127
            self.OUTPUT_BYTES = 6
        if LOCAL_DEBUG:
            assert len(code) <= self.LEN
            assert rounding in range(4)
        if len(code) > self.LEN: # если на вход дали слишком длинный код, нужно смотреть только на последние self.LEN бит
            code = code[-self.LEN:]
        if len(code) < self.LEN:
            code_copy = code
            code = [0 for _ in range(self.LEN - len(code_copy))]
            code.extend(code_copy)

        self.sign = code[0]
        self.rounding = rounding
        self.half_or_float = half_or_float

        if 1 not in code[1:self.EXP_LEN + 1]:
            self.exp = self.MIN_EXP
            self.denormalized = True
        else:
            self.denormalized = False
            self.exp = 0
            for i in range(self.EXP_LEN, 0, -1):
                self.exp += (code[i] << (self.EXP_LEN - i))
            self.exp -= self.EXP_SHIFT

        self.mant = code[1 + self.EXP_LEN:]
        if LOCAL_DEBUG:
            assert len(self.mant) == self.MANT_LEN
        self.type = Types_USUAL
        if self.exp == self.MAX_EXP:
            if self.mant == [0 for _ in range(self.MANT_LEN)]:
                if self.sign == 0:
                    self.type = Types_PLUS_INF
                else:
                    self.type = Types_MINUS_INF
            else:
                self.type = Types_NaN

        self.integer = 0
        for i in range(self.MANT_LEN - 1, -1, -1):
            self.integer += (self.mant[i] << (self.MANT_LEN - 1 - i))
        if not self.denormalized:
            self.integer += (1 << self.MANT_LEN)

    def __str__(self):
        if self.type == Types_NaN:
            return "nan"
        if self.type == Types_PLUS_INF:
            return "inf"
        if self.type == Types_MINUS_INF:
            return "-inf"
        if self.is_null():
            if self.half_or_float: # float
                return ("-" if self.sign == 1 else "") + "0x0.000000p+0"
            else:
                return ("-" if self.sign == 1 else "") + "0x0.000p+0"
        mant2hex = "" # дописываем к мантиссе от нуля до трёх нулей, чтобы её длина стала делиться на 4 и переводим в 16-ричную систему счисления
        code = self.mant
        if self.denormalized:
            exp = self.MIN_EXP - 1
            idx = 0
            while code[idx] == 0:
                idx += 1
            exp -= idx
            code = code[idx+1:]
            code.extend([0 for _ in range(4 * self.OUTPUT_BYTES - len(code))])
        else:
            code.extend([0 for _ in range(4 * self.OUTPUT_BYTES - len(code))])
            exp = self.exp
        for i in range(self.OUTPUT_BYTES):
            mant2hex += (hex_string[8 * code[4 * i] + 4 * code[4 * i + 1] + 2 * code[4 * i + 2] + code[4 * i + 3]])
        return (("-" if self.sign == 1 else "") + "0x1." + mant2hex + "p" + ('-' if self.exp < 0 else '+') + str(abs(exp))).lower()

    def make_plus_inf(self):
        code_plus_inf = [0 for _ in range(self.LEN)]
        for i in range(1, 1 + self.EXP_LEN):
            code_plus_inf[i] = 1
        return FloatNum(code_plus_inf, Rounding_TOWARD_ZERO, self.half_or_float)

    def make_minus_inf(self):
        code_minus_inf = [0 for _ in range(self.LEN)]
        for i in range(0, 1 + self.EXP_LEN):
            code_minus_inf[i] = 1
        return FloatNum(code_minus_inf, Rounding_TOWARD_ZERO, self.half_or_float)

    def make_inf_with_sign(self, sign):
        if LOCAL_DEBUG:
            assert sign in [0, 1]
        if sign == 0:
            return self.make_plus_inf()
        return self.make_minus_inf()

    def make_nan(self):
        return FloatNum([1 for _ in range(self.LEN)], Rounding_TOWARD_ZERO, self.half_or_float)

    def make_null(self):
        return FloatNum([0 for _ in range(self.LEN)], Rounding_TOWARD_ZERO, self.half_or_float)

    def make_null_with_sign(self, sign):
        code = [sign]
        code.extend([0 for _ in range(self.LEN - 1)])
        return FloatNum(code, Rounding_TOWARD_ZERO, self.half_or_float)

    def is_null(self):
        return not any(self.mant) and self.denormalized


    def get_opposite(self):
        new_code = [1 - self.sign]
        new_code.extend(int2bin(self.exp + self.EXP_SHIFT - self.denormalized, self.EXP_LEN))
        new_code.extend(self.mant)
        return FloatNum(new_code, self.rounding, self.half_or_float)

    def increase_num(self):
        if self.is_null():
            ans = [0 for _ in range(self.LEN)]
            ans[-1] = 1
            return FloatNum(ans, self.rounding, self.half_or_float)
        if self.sign == 1:
            return self.get_opposite().decrease_num().get_opposite()
        if self.denormalized:
            if self.integer + 1 != (1 << self.MANT_LEN): # будет снова денормализованное
                new_code = [0 for _ in range(1 + self.EXP_LEN)]
                new_code.extend(int2bin(self.integer - 1, self.MANT_LEN))
                return FloatNum(new_code, self.rounding, self.half_or_float)
            else: # будет 2^-14
                new_code = [0 for _ in range(self.LEN)]
                new_code[self.EXP_LEN] = 1
                return FloatNum(new_code, self.rounding, self.half_or_float)
        if all(self.mant) == 1: # вся мантисса состоит из единичек
            if self.exp + 1 == self.MAX_EXP:
                return self.make_plus_inf()
            else:
                new_code = [0] # знак положительный
                new_code.extend(int2bin(self.exp + self.EXP_SHIFT + 1, self.EXP_LEN)) # экспоненту увеличили на 1
                new_code.extend([0 for _ in range(self.MANT_LEN)]) # в мантиссе все нули
        else:
            new_code = [0] # знак положительный
            new_code.extend(int2bin(self.exp + self.EXP_SHIFT, self.EXP_LEN))  # экспоненту не поменяли
            new_code.extend(int2bin(self.integer + 1, self.MANT_LEN)) # мантиссу увеличили на 1
        return FloatNum(new_code, self.rounding, self.half_or_float)

    def decrease_num(self):
        if self.is_null():
            ans = [0 for _ in range(self.LEN)]
            ans[0] = 1
            ans[-1] = 1
            return FloatNum(ans, self.rounding, self.half_or_float)
        if self.sign == 1:
            return self.get_opposite().increase_num().get_opposite()
        if self.denormalized:
            new_code = [0 for _ in range(1 + self.EXP_LEN)]
            new_code.extend(int2bin(self.integer - 1, self.MANT_LEN))
            return FloatNum(new_code, self.rounding, self.half_or_float)
        new_code = [0] # знак положительный
        if any(self.mant): # мантисса ненулевая
            new_code.extend(int2bin(self.exp + self.EXP_SHIFT, self.EXP_LEN)) # экспоненту не поменяли
            new_code.extend(int2bin(self.integer - 1, self.MANT_LEN)) # мантиссу уменьшили на 1
        else:
            if self.exp == self.MIN_EXP:
                new_code.extend(int2bin(0, self.EXP_LEN))  # экспонента -15 (временно) -- она перекодируется во все нули
            else:
                new_code.extend(int2bin(self.exp + self.EXP_SHIFT - 1, self.EXP_LEN))  # экспоненту уменьшили на 1
            new_code.extend([1 for _ in range(self.MANT_LEN)])  # мантиссу сделали 1...1
        return FloatNum(new_code, self.rounding, self.half_or_float)

    def rounding_result(self, sign, exponent, code):
        if LOCAL_DEBUG:
            assert sign in [0, 1]
        ans_code = [sign]
        ans_code.extend(int2bin(exponent + self.EXP_SHIFT, self.EXP_LEN))
        ans_code.extend(code[:self.MANT_LEN])
        ans = FloatNum(ans_code, self.rounding, self.half_or_float)

        if self.rounding == Rounding_TOWARD_ZERO:
            return ans

        elif self.rounding == Rounding_TOWARD_NEG_INFINITY:
            if sign == 1 and any(code[self.MANT_LEN:]):
                return ans.decrease_num()
            return ans

        elif self.rounding == Rounding_TOWARD_INFINITY:
            if any(code[self.MANT_LEN:]) and sign == 0:
                return ans.increase_num()
            return ans

        else:
            if len(code) == self.MANT_LEN or code[self.MANT_LEN] == 0:
                return ans
            else:
                if (len(code) == self.MANT_LEN + 1 or (
                not any(code[self.MANT_LEN + 1:]))) and ans_code[-1] == 0:
                    return ans
                else:
                    if ans_code[0] == 1:
                        return ans.decrease_num()
                    else:
                        return ans.increase_num()

    def make_ans_by_sign_exp_and_code(self, sign, exp, code): # code of first_int without leading 1
        if len(code) >= self.MANT_LEN + 1:
            return self.rounding_result(sign, exp, code)
        else:
            new_code = [sign]
            new_code.extend(int2bin(exp + self.EXP_SHIFT, self.EXP_LEN))
            new_code.extend(code[:self.MANT_LEN])
            return FloatNum(new_code, self.rounding, self.half_or_float)

    def ans_if_other_is_too_small(self, other_sign):
        if self.rounding == Rounding_NEAREST_EVEN:
            return self  # because the nearest is self value
        elif self.rounding == Rounding_TOWARD_ZERO:
            if self.sign == other_sign:
                return self
            else:
                if self.sign == 0:
                    return self.decrease_num()
                else:
                    return self.increase_num()
        elif self.rounding == Rounding_TOWARD_INFINITY:
            if self.sign == 0:
                if other_sign == 0:
                    return self.increase_num()
                else:
                    return self
            else:
                if other_sign == 0:
                    return self.increase_num()
                else:
                    return self
        else:
            if self.sign == 0:
                if other_sign == 0:
                    return self
                else:
                    return self.decrease_num()
            else:
                if other_sign == 0:
                    return self
                else:
                    return self.decrease_num()

    def biggest_positive(self):
        if self.rounding == Rounding_TOWARD_INFINITY:
            return self.make_plus_inf()
        code = [1 for _ in range(self.LEN)]
        code[0] = 0
        code[self.EXP_LEN] = 0
        return FloatNum(code, self.rounding, self.LEN == 32)

    def biggest_negative(self):
        if self.rounding == Rounding_TOWARD_NEG_INFINITY:
            return self.make_minus_inf()
        code = [1 for _ in range(self.LEN)]
        code[self.EXP_LEN] = 0
        return FloatNum(code, self.rounding, self.LEN == 32)

    def biggest_with_sign(self, sign):
        if sign == 0:
            return self.biggest_positive()
        return self.biggest_negative()

    def __add__(self, other):
        if self.type == Types_NaN or other.type == Types_NaN: # TESTS A1
            return self.make_nan()
        if (self.type == Types_MINUS_INF and other.type == Types_PLUS_INF) or (other.type == Types_MINUS_INF and self.type == Types_PLUS_INF): # TESTS A2
            return self.make_nan()
        if self.type == Types_MINUS_INF or other.type == Types_MINUS_INF: # TESTS A3
            return self.make_minus_inf()
        if self.type == Types_PLUS_INF or other.type == Types_PLUS_INF: # TESTS A4
            return self.make_plus_inf()
        if self.is_null() and other.is_null(): # 2 nulls
            if self.sign == 1 and other.sign == 1:
                return self.make_null_with_sign(1)
            elif (self.sign == 1 or other.sign == 1) and self.rounding == Rounding_TOWARD_NEG_INFINITY:
                return self.make_null_with_sign(1)
            return self.make_null()
        if self.sign != other.sign:
            if self.integer == other.integer and self.exp == other.exp:
                return self.make_null_with_sign(1 if self.rounding == Rounding_TOWARD_NEG_INFINITY else 0)

        if self.denormalized and other.denormalized:
            first_int = self.integer * (-1 if self.sign == 1 else 1)
            second_int = other.integer * (-1 if other.sign == 1 else 1)
            new_num = first_int + second_int
            new_code = [0 for _ in range(self.LEN)]
            new_code[0] = 0 if new_num >= 0 else 1
            new_num = abs(new_num)
            if new_num < (1 << self.MANT_LEN): # тогда результат - тоже денормализованное число # TESTS A5
                for i in range(self.MANT_LEN):
                    new_code[self.LEN - 1 - i] = 1 if new_num & (1 << i) else 0
            else: # получится нормализованное число -- последний бит экспоненты будет равен 1 (то есть экспонента равна self.MIN_EXP) # TESTS A6
                if LOCAL_DEBUG:
                    assert new_num < (1 << (self.MANT_LEN + 1))
                for i in range(self.MANT_LEN + 1): # в этом цикле последний бит экспоненты  так же сделается единицей
                    new_code[self.LEN - 1 - i] = 1 if new_num & (1 << i) else 0
            return FloatNum(new_code, self.rounding, self.half_or_float)

        if (not self.denormalized) and other.denormalized:
            if other.is_null():
                return self
            first_exp = self.exp
            second_exp = self.MIN_EXP
            first_int = self.integer
            second_int = other.integer
            delta_exp = first_exp - second_exp
            if delta_exp >= self.MANT_LEN + 2: # TESTS A7
                return self.ans_if_other_is_too_small(other.sign)

            else:
                if self.sign != other.sign:
                    second_int *= -1
                first_int <<= (first_exp - self.MIN_EXP)
                L = least_bits_needed(first_int) # L бит занимает число first_int
                if LOCAL_DEBUG:
                    assert (1 << L - 1) <= first_int < (1 << L)
                first_int += second_int

                if first_int >= (1 << L): # степень увеличилась # TESTS A8
                    first_exp += 1
                    if first_exp == self.MAX_EXP: # если она стала 16, то у нас бесконечность со знаком как у self
                        return self.biggest_with_sign(self.sign)
                    code_of_first_int = int2bin(first_int, L) # вообще всего L + 1 бит, но так как старший бит равен 1 и не попадёт в мантиссу, он нам не очень нужен
                    return self.make_ans_by_sign_exp_and_code(self.sign, first_exp, code_of_first_int)

                elif (1 << L) > first_int >= (1 << (L - 1)): # степень не поменялась # TESTS A9
                    code_of_first_int = int2bin(first_int, L - 1)  # вообще всего L бит, но так как старший бит равен 1 и не попадёт в мантиссу, он нам не очень нужен
                    return self.make_ans_by_sign_exp_and_code(self.sign, first_exp, code_of_first_int)

                else: # степень уменьшилась # TESTS A10
                    if first_exp > self.MIN_EXP: # у нас по-прежнему нормализованное число
                        first_exp -= 1
                        code_of_first_int = int2bin(first_int, L - 2)  # вообще всего L - 1 бит, но так как старший бит равен 1 и не попадёт в мантиссу, он нам не очень нужен
                        return self.make_ans_by_sign_exp_and_code(self.sign, first_exp, code_of_first_int)
                    else: # у нас получится денормализованное число
                        new_code = [self.sign]
                        new_code.extend(int2bin(0, self.EXP_LEN))
                        if LOCAL_DEBUG:
                            assert L == self.MANT_LEN + 1
                        new_code.extend(int2bin(first_int, L - 1))  # вообще всего L бит, но так как старший бит равен 1 и не попадёт в мантиссу, он нам не очень нужен)
                        return FloatNum(new_code, self.rounding, self.half_or_float)

        if self.denormalized and (not other.denormalized):
            return other + self

        else:
            if LOCAL_DEBUG:
                assert (not self.denormalized) and (not other.denormalized)
            if self.exp < other.exp or (self.exp == other.exp and self.integer < other.integer):
                return other + self
            first_int = self.integer
            second_int = other.integer
            first_exp = self.exp
            second_exp = other.exp
            if first_exp - second_exp > self.MANT_LEN + 2: # TESTS A11
                return self.ans_if_other_is_too_small(other.sign)

            first_int <<= (first_exp - second_exp)
            L = least_bits_needed(first_int)
            if self.sign != other.sign:
                second_int *= -1
            first_int += second_int # теперь в first_int лежит сумма first_int и second_int
            if first_int >= (1 << L):
                L += 1
                first_exp += 1
            if first_int == 0: # TEST A13
                return FloatNum([0 for _ in range(self.LEN)], self.rounding, self.half_or_float)
            if first_exp == self.MAX_EXP: # TESTS A12
                return self.biggest_with_sign(self.sign)
            idx = 0
            code_of_first_int = int2bin(first_int, L)
            if LOCAL_DEBUG:
                assert(any(code_of_first_int))
            while code_of_first_int[idx] == 0:
                idx += 1
                first_exp -= 1
            if first_exp >= self.MIN_EXP: # TESTS A14
                idx += 1
                code_of_first_int.extend([0 for _ in range(self.MANT_LEN)]) # в конец записи после запятой можно дописать нули, чтобы потом удобнее было считывать мантиссу и округлять
                return self.make_ans_by_sign_exp_and_code(self.sign, first_exp, code_of_first_int[idx:])
            else: # TESTS A15
                x = -(first_exp - self.MIN_EXP)
                if LOCAL_DEBUG:
                    assert x >= 1
                new_code = [self.sign]
                new_code.extend(int2bin(0, self.EXP_LEN))
                code_of_first_int.extend([0 for _ in range(
                    self.MANT_LEN)])  # в конец записи после запятой можно дописать нули, чтобы потом удобнее было считывать мантиссу и округлять
                new_code.extend([0 for _ in range(min(x - 1, self.MANT_LEN))])
                new_code.extend(code_of_first_int[idx:idx+self.MANT_LEN-min(x - 1, self.MANT_LEN)])
                return FloatNum(new_code, self.rounding, self.half_or_float) # округлять денормализованное число не надо:)

    def __sub__(self, other):
        if LOCAL_DEBUG: assert isinstance(other, FloatNum)
        return self + other.get_opposite()
    def round_too_small(self, other):  # если произведение/отношение двух чисел оказалось слишком маленькое по модулю, то выводим либо 0, либо самое +-маленькое по модулю число в зависимости от округления
        if self.rounding in [Rounding_TOWARD_ZERO, Rounding_NEAREST_EVEN] or (
                self.rounding == Rounding_TOWARD_INFINITY and self.sign != other.sign) or (
                self.rounding == Rounding_TOWARD_NEG_INFINITY and self.sign == other.sign):
            return self.make_null_with_sign(0 if self.sign == other.sign else 1)
        else:
            ans = [0 for _ in range(self.LEN)]
            ans[0] = 0 if self.sign == other.sign else 1
            ans[-1] = 1
            return FloatNum(ans, self.rounding, self.half_or_float)


    def __mul__(self, other):
        if self.type == Types_NaN or other.type == Types_NaN: # SPEACIAL CASES: TESTS B1
            return self.make_nan()
        elif self.is_null() and other.type in [Types_MINUS_INF, Types_PLUS_INF]:
            return self.make_nan()
        elif other.is_null() and self.type in [Types_MINUS_INF, Types_PLUS_INF]:
            return self.make_nan()

        if self.is_null() or other.is_null():
            return self.make_null_with_sign(0 if self.sign == other.sign else 1)
        if self.type in [Types_MINUS_INF, Types_PLUS_INF] or other.type in [Types_MINUS_INF, Types_PLUS_INF]:
            return self.make_inf_with_sign(0 if self.sign == other.sign else 1)


        if self.denormalized and other.denormalized: # TESTS B2
            return self.round_too_small(other)

        elif other.denormalized:
            first_exp = self.exp
            first_int = self.integer
            second_exp = other.exp

            if LOCAL_DEBUG:
                assert second_exp == self.MIN_EXP

            x = 1
            while other.mant[x - 1] == 0:
                x += 1
            second_exp -= x
            second_int = other.integer
            first_int *= second_int # теперь first_int - произведение
            first_exp += second_exp # теперь в first_exp лежит сумма экспонент множителей

            L = least_bits_needed(first_int)

            if LOCAL_DEBUG:
                assert (1 << L) > first_int >= (1 << (L - 1))

            if first_exp >= self.MIN_EXP: # получим нормализованное число # TESTS B3
                code_of_first_int = int2bin(first_int, L - 1) # главная единичка нам не нужна
                return self.rounding_result(0 if self.sign == other.sign else 1, first_exp, code_of_first_int)

            elif first_exp < self.MIN_EXP - self.MANT_LEN: # меньше минимального, которое можно закодировать # TESTS B4
                return self.round_too_small(other)

            else: # у нас получится денормализованное число # TESTS B5
                prev_nulls_in_mant = -(first_exp - self.MIN_EXP) - 1 # сколько нулей надо поставить перед мантиссой
                code_of_first_int = [0 for _ in range(prev_nulls_in_mant)]
                code_of_first_int.extend(int2bin(first_int, L))  # главная единичка нам нужна (раз число нормализованное), поэтому L
                return self.make_ans_by_sign_exp_and_code(0 if self.sign == other.sign else 1, self.MIN_EXP - 1, code_of_first_int)
        elif self.denormalized:
            return other * self
        else: # произведение двух нормализованных чисел
            first_exp = self.exp
            first_int = self.integer
            second_exp = other.exp
            second_int = other.integer
            first_int *= second_int # теперь first_int - произведение
            L = least_bits_needed(first_int)
            delta_exp = L - 2 * self.MANT_LEN - 1
            code_of_first_int = int2bin(first_int, L - 1) # ведущая единичка нам не нужна
            first_exp += second_exp + delta_exp
            if first_exp >= self.MAX_EXP: # TESTS B6
                return self.biggest_with_sign(0 if self.sign == other.sign else 1)
            elif first_exp >= self.MIN_EXP: # TESTS B7
                return self.make_ans_by_sign_exp_and_code(0 if self.sign == other.sign else 1, first_exp, code_of_first_int)
            elif first_exp < self.MIN_EXP - self.MANT_LEN: # меньше минимального, которое можно закодировать # TESTS B8
                return self.round_too_small(other)
            else: # число денормализованное # TESTS B9
                prev_nulls_in_mant = -(first_exp - self.MIN_EXP) - 1
                code_of_first_int = [0 for _ in range(prev_nulls_in_mant)]
                code_of_first_int.extend(int2bin(first_int, least_bits_needed(first_int)))
                return self.make_ans_by_sign_exp_and_code(0 if self.sign == other.sign else 1, self.MIN_EXP - 1, code_of_first_int)

    def __truediv__(self, other):
        if self.type == Types_NaN or other.type == Types_NaN:
            return self.make_nan()
        elif self.type in [Types_PLUS_INF, Types_MINUS_INF] and other.type in [Types_PLUS_INF, Types_MINUS_INF]:
            return self.make_nan()
        elif self.is_null() and other.is_null():
            return self.make_nan()
        elif self.is_null() or other.type in [Types_PLUS_INF, Types_MINUS_INF]:
            return self.make_null_with_sign(0 if self.sign == other.sign else 1)
        elif self.type in [Types_PLUS_INF, Types_MINUS_INF] or other.is_null():
            return self.make_inf_with_sign(0 if self.sign == other.sign else 1)

        ans_sign = 0 if self.sign == other.sign else 1

        if not self.denormalized:
            first_exp = self.exp
            first_int = self.integer
        else:
            first_exp = self.MIN_EXP - 1
            idx = 0
            while self.mant[idx] == 0:
                idx += 1
                first_exp -= 1
            code_for_first_int = self.mant[idx:]
            code_for_first_int.extend([0 for _ in range(1 + self.MANT_LEN - len(code_for_first_int))])
            first_int = bin_code2int(code_for_first_int)

        if not other.denormalized:
            second_exp = other.exp
            second_int = other.integer
        else:
            second_exp = self.MIN_EXP - 1
            idx = 0
            while other.mant[idx] == 0:
                idx += 1
                second_exp -= 1
            code_for_second_int = other.mant[idx:]
            code_for_second_int.extend([0 for _ in range(1 + self.MANT_LEN - len(code_for_second_int))])
            second_int = bin_code2int(code_for_second_int)

        L = 1 + self.MANT_LEN
        if LOCAL_DEBUG:
            assert (1 << L) > first_int >= (1 << (L - 1))

        if first_int >= second_int:
            first_int <<= self.MANT_LEN
            first_exp -= second_exp
            div = first_int // second_int
            r = first_int % second_int
        else:
            first_int <<= (self.MANT_LEN+1)
            first_exp -= (second_exp+1)
            div = first_int // second_int # частное
            r = first_int % second_int
        if self.rounding == Rounding_TOWARD_INFINITY and self.sign == 0 and r > 0:
            div += 1
        elif self.rounding == Rounding_TOWARD_NEG_INFINITY and self.sign == 1 and r > 0:
            div += 1
        elif self.rounding == Rounding_NEAREST_EVEN and (2 * r > second_int or (2 * r == second_int and div % 2 == 1)):
            div += 1

        if div >= (1 << L):
            first_exp += 1
            if LOCAL_DEBUG:
                assert div < (1 << (L + 1))

        # while div < (1 << (L - 1)):
        #     print("...")
        #     div <<= 1
        #     first_exp -= 1
        if first_exp >= self.MAX_EXP:
            return self.biggest_with_sign(ans_sign)
        elif first_exp < self.MIN_EXP - self.MANT_LEN:
            return self.round_too_small(other)
        elif first_exp < self.MIN_EXP:
            code_of_res = [0 for _ in range(-(first_exp - self.MIN_EXP) - 1)]
            code_of_res.extend(int2bin(div, L - 1))
            return self.make_ans_by_sign_exp_and_code(ans_sign, self.MIN_EXP - 1, code_of_res)
        else:
            return self.make_ans_by_sign_exp_and_code(ans_sign, first_exp, int2bin(div, L - 1))

