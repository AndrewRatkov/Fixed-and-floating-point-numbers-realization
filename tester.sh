#!/bin/bash


# Для вывода результатов всевозможных операций с всевозможными округлениями
check=0
format=8.8
x=0xffff
y=0x0f00

if [[ $check == 1 ]]; then
    echo Умножение
    for (( i=0; i<4; i++ )); do
        python3.11 main.py $format $i $x \* $y
    done
    echo Сложение
    for (( i=0; i<4; i++ )); do
        python3.11 main.py $format $i $x + $y
    done
    echo Вычитание
    for (( i=0; i<4; i++ )); do
        python3.11 main.py $format $i $x - $y
    done
    echo Деление
    for (( i=0; i<4; i++ )); do
        python3.11 main.py $format $i $x / $y
    done
fi

# вывод каких-то чисел h
check_half_str=0
if [[ $check_half_str == 1 ]]; then
    python3.11 main.py h 2 0x666D
    python3.11 main.py h 2 0x999D
    python3.11 main.py h 2 0xFFFF
    python3.11 main.py h 2 0xFC00
    python3.11 main.py h 2 0x7C00
    python3.11 main.py h 2 0x1111
    python3.11 main.py h 2 0x3030
    python3.11 main.py h 2 0x0000
    python3.11 main.py h 2 0x8000
    python3.11 main.py h 2 0x8300
fi


basic_tests_for_add_h=(
# Test 1
  "h 0 0x3400 + 0x0001" "0x1.000p-2" # 1
  "h 1 0x3400 + 0x0001" "0x1.000p-2" # 2
  "h 2 0x3400 + 0x0001" "0x1.004p-2" # 3
  "h 3 0x3400 + 0x0001" "0x1.000p-2" # 4
# Test 2
  "h 0 0x3400 + 0x8001" "0x1.ffcp-3" # 5
  "h 1 0x3400 + 0x8001" "0x1.000p-2" # 6
  "h 2 0x3400 + 0x8001" "0x1.000p-2" # 7
  "h 3 0x3400 + 0x8001" "0x1.ffcp-3" # 8
# Test 3
  "h 0 0x0C00 + 0x8001" "0x1.ffcp-13" # 9
  "h 1 0x0C00 + 0x8001" "0x1.000p-12" # 10
  "h 2 0x0C00 + 0x8001" "0x1.000p-12" # 11
  "h 3 0x0C00 + 0x8001" "0x1.ffcp-13" # 12
# Test 4
  "h 0 0x0C11 + 0x8001" "0x1.040p-12" # 13
  "h 1 0x0C11 + 0x8001" "0x1.044p-12" # 14
  "h 2 0x0C11 + 0x8001" "0x1.044p-12" # 15
  "h 3 0x0C11 + 0x8001" "0x1.040p-12" # 16
# Test 5
  "h 0 0x7800 + 0x0001" "0x1.000p+15" # 17
  "h 1 0x7800 + 0x0001" "0x1.000p+15" # 18
  "h 2 0x7800 + 0x0001" "0x1.004p+15" # 19
  "h 3 0x7800 + 0x0001" "0x1.000p+15" # 20
# Test 6
  "h 0 0x7800 + 0x00AA" "0x1.000p+15" # 21
  "h 1 0x7800 + 0x00AA" "0x1.000p+15" # 22
  "h 2 0x7800 + 0x00AA" "0x1.004p+15" # 23
  "h 3 0x7800 + 0x00AA" "0x1.000p+15" # 24
# Test 7
  "h 0 0x0400 + 0x8001" "0x1.ff8p-15" # 25
  "h 1 0x0400 + 0x8001" "0x1.ff8p-15" # 26
  "h 2 0x0400 + 0x8001" "0x1.ff8p-15" # 27
  "h 3 0x0400 + 0x8001" "0x1.ff8p-15" # 28
# Test 8
  "h 0 0x7BFF + 0x0001" "0x1.ffcp+15" # 29
  "h 1 0x7BFF + 0x0001" "0x1.ffcp+15" # 30
  "h 2 0x7BFF + 0x0001" "inf" # 31
  "h 3 0x7BFF + 0x0001" "0x1.ffcp+15" # 32
# Test 9
  "h 0 0xFBFF + 0x8001" "-0x1.ffcp+15" # 33
  "h 1 0xFBFF + 0x8001" "-0x1.ffcp+15" # 34
  "h 2 0xFBFF + 0x8001" "-0x1.ffcp+15" # 35
  "h 3 0xFBFF + 0x8001" "-inf" # 36
# Test 10
  "h 0 0xAAAA + 0xAAAA" "-0x1.aa8p-4" # 37
  "h 1 0xAAAA + 0xAAAA" "-0x1.aa8p-4" # 38
  "h 2 0xAAAA + 0xAAAA" "-0x1.aa8p-4" # 39
  "h 3 0xAAAA + 0xAAAA" "-0x1.aa8p-4" # 40
# Test 11
  "h 0 0x7800 + 0x7801" "0x1.ffcp+15" # 41
  "h 1 0x7800 + 0x7801" "0x1.ffcp+15" # 42
  "h 2 0x7800 + 0x7801" "inf" # 43
  "h 3 0x7800 + 0x7801" "0x1.ffcp+15" # 44
# Test 12
  "h 0 0x3400 + 0x3400" "0x1.000p-1" # 45
  "h 1 0x3400 + 0x3400" "0x1.000p-1" # 46
  "h 2 0x3400 + 0x3400" "0x1.000p-1" # 47
  "h 3 0x3400 + 0x3400" "0x1.000p-1" # 48
# Test 13
  "h 0 0x0002 + 0x0001" "0x1.800p-23" # 49
  "h 1 0x0002 + 0x0001" "0x1.800p-23" # 50
  "h 2 0x0002 + 0x0001" "0x1.800p-23" # 51
  "h 3 0x0002 + 0x0001" "0x1.800p-23" # 52
# Test 14
  "h 0 0x0500 + 0x0100" "0x1.800p-14" # 53
  "h 1 0x0500 + 0x0100" "0x1.800p-14" # 54
  "h 2 0x0500 + 0x0100" "0x1.800p-14" # 55
  "h 3 0x0500 + 0x0100" "0x1.800p-14"  # 56
)

debug_basic_tests_for_summ_h=1
if [[ $debug_basic_tests_for_summ_h == 1 ]]; then
  echo Testing first_tests_for_summ_h...
  length_basic_tests=${#basic_tests_for_add_h[@]}
  for (( i=0; i<$(($length_basic_tests / 2)); ++i)); do
    z=`python3.11 main.py ${basic_tests_for_add_h[$((2*$i))]}`
    if [[ $z != ${basic_tests_for_add_h[$((2*$i + 1))]} ]]; then
      echo "Error in test $(( $i + 1 )): calculating the ${basic_tests_for_add_h[$((3*$i))]}, $z found, but ${basic_tests_for_add_h[$((2*$i + 1))]} expected"
    fi
  done
fi

testsA=(
    "h 0 0xFC00 + 0xFF00" "nan" "A1"
    "h 1 0x0000 + 0xFF00" "nan" "A1"
    "h 1 0x0 + 0xFF00" "nan" "A1"

    "h 1 0x7C00 + 0xFC00" "nan" "A2"
    "h 0 0xFC00 + 0x7C00" "nan" "A2"

    "h 1 0xFC00 + 0xFC00" "-inf" "A3"
    "h 2 0xFC00 + 0x7A00" "-inf" "A3"

    "h 0 0x7C00 + 0x3C00" "inf" "A4"
    "h 3 0x7C00 + 0x7C00" "inf" "A4"

    "h 0 0x0002 + 0x0001" "0x1.800p-23" "A5"
    "h 0 0x2 + 0x1" "0x1.800p-23" "A5"
    "h 1 0x8002 + 0x0001" "-0x1.000p-24" "A5"
    "h 1 0x8002 + 0x8001" "-0x1.800p-23" "A5"
    "h 2 0x0000 + 0x0003" "0x1.800p-23" "A5"
    "h 3 0x0002 + 0x0000" "0x1.000p-23" "A5"
    "h 0 0x02AA + 0x0155" "0x1.ff8p-15" "A5"
    "h 1 0x02AA + 0x0155" "0x1.ff8p-15" "A5"
    "h 2 0x02AA + 0x0155" "0x1.ff8p-15" "A5"
    "h 3 0x0155 + 0x0155" "0x1.550p-15" "A5"

    "h 0 0x02AA + 0x02AA" "0x1.550p-14" "A6"
    "h 1 0x02AA + 0x02aa" "0x1.550p-14" "A6"
    "h 2 0x02AA + 0x02aa" "0x1.550p-14" "A6"
    "h 3 0x02AA + 0x02aa" "0x1.550p-14" "A6"

    "h 0 0x3400 + 0x0001" "0x1.000p-2" "A7"
    "h 1 0x3400 + 0x0001" "0x1.000p-2" "A7"
    "h 2 0x3400 + 0x0001" "0x1.004p-2" "A7"
    "h 3 0x3400 + 0x0001" "0x1.000p-2" "A7"
    "h 0 0x3400 + 0x8001" "0x1.ffcp-3" "A7"
    "h 1 0x3400 + 0x8001" "0x1.000p-2" "A7"
    "h 2 0x3400 + 0x8001" "0x1.000p-2" "A7"
    "h 3 0x3400 + 0x8001" "0x1.ffcp-3" "A7"

    "h 0 0x1fff + 0x0200" "0x1.00cp-7" "A8"
    "h 1 0x1fff + 0x0200" "0x1.010p-7" "A8"
    "h 2 0x1fff + 0x0200" "0x1.010p-7" "A8"
    "h 3 0x1fff + 0x0200" "0x1.00cp-7" "A8"
    "h 0 0x9fff + 0x8200" "-0x1.00cp-7" "A8"
    "h 1 0x9fff + 0x8200" "-0x1.010p-7" "A8"
    "h 2 0x9fff + 0x8200" "-0x1.00cp-7" "A8"
    "h 3 0x9fff + 0x8200" "-0x1.010p-7" "A8"

    "h 0 0x1f3a + 0x0200" "0x1.d08p-8" "A9"
    "h 1 0x0200 + 0x1f3a" "0x1.d08p-8" "A9"
    "h 2 0x1f3a + 0x0200" "0x1.d08p-8" "A9"
    "h 3 0x1f3a + 0x0200" "0x1.d08p-8" "A9"

    "h 0 0x1c00 + 0x8200" "0x1.fc0p-9" "A10"
    "h 1 0x1c00 + 0x8200" "0x1.fc0p-9" "A10"
    "h 2 0x8200 + 0x1c00" "0x1.fc0p-9" "A10"
    "h 3 0x8200 + 0x1c00" "0x1.fc0p-9" "A10"
    "h 0 0x0400 + 0x8100" "0x1.800p-15" "A10"
    "h 2 0x8100 + 0x0400" "0x1.800p-15" "A10"

    "h 0 0x30ee + 0x6400" "0x1.000p+10" "A11"
    "h 1 0x30fd + 0x6400" "0x1.000p+10" "A11"
    "h 2 0x6400 + 0x30aa" "0x1.004p+10" "A11"
    "h 3 0x6400 + 0x309a" "0x1.000p+10" "A11"

    "h 0 0x78ae + 0x7800" "0x1.ffcp+15" "A12"
    "h 1 0x7bff + 0x5000" "0x1.ffcp+15" "A12"

    "h 1 0xf7ff + 0x77ff" "0x0.000p+0" "A13"
    "h 1 0xf5ae + 0x75ae" "0x0.000p+0" "A13"

    "h 0 0x34ee + 0x6400" "0x1.000p+10" "A14"
    "h 1 0x34fd + 0x6400" "0x1.000p+10" "A14"
    "h 2 0x6400 + 0x34aa" "0x1.004p+10" "A14"
    "h 3 0x6400 + 0x349a" "0x1.000p+10" "A14"
    "h 0 0x4d55 + 0x4955" "0x1.ffcp+4" "A14"
    "h 1 0x4d55 + 0x4955" "0x1.000p+5" "A14"
    "h 2 0x4d55 + 0x4955" "0x1.000p+5" "A14"
    "h 3 0x4d55 + 0x4955" "0x1.ffcp+4" "A14"

    "h 0 0x0800 + 0x8900" "-0x1.000p-15" "A15"
    "h 1 0x0800 + 0x8900" "-0x1.000p-15" "A15"
    "h 2 0x8800 + 0x0900" "0x1.000p-15" "A15"
    "h 3 0x8800 + 0x0900" "0x1.000p-15" "A15"

    "f 0 0x414587dd + 0x42ebf110" "0x1.04a20ap+7" "From ci.yaml"
    "f 1 0x414587dd + 0x42ebf110" "0x1.04a20cp+7" "From ci.yaml"
    "f 2 0x414587dd + 0x42ebf110" "0x1.04a20cp+7" "From ci.yaml"
    "f 3 0x414587dd + 0x42ebf110" "0x1.04a20ap+7" "From ci.yaml"

    "h 0 0x8000 + 0x0" "0x0.000p+0" "From ci.yaml"
)
debug_tests_A=1

if [[ $debug_tests_A == 1 ]]; then
  echo Testing tests_for_summ_h for all ifs...
  lengthA=${#testsA[@]}
  for (( i=0; i<$(($lengthA / 3)); ++i)); do
    z=`python3.11 main.py ${testsA[$((3*$i))]}`
    if [[ $z != ${testsA[$((3*$i + 1))]} ]]; then
      echo "Error in test $i (type = ${testsA[$((3*$i + 2))]}): calculating the ${testsA[$((3*$i))]}, $z found, but ${testsA[$((3*$i + 1))]} expected"
    fi
  done
fi

testsB=(
    "h 0 0xFC00" "0xFF00" "nan" "B1"
    "h 1 0x0000" "0xFC00" "nan" "B1"
    "h 1 0x7C00" "0xFC00" "-inf" "B1"
    "h 0 0xFC00" "0x7C00" "-inf" "B1"
    "h 1 0xFC00" "0xFC00" "inf" "B1"
    "h 2 0xFC00" "0x7A00" "-inf" "B1"
    "h 0 0x7C00" "0x3C00" "inf" "B1"
    "h 3 0x7C00" "0x7C00" "inf" "B1"
    "h 2 0x0000" "0x7A00" "0x0.000p+0" "B1"

    "h 0 0x00f0" "0x00da" "0x0.000p+0" "B2"
    "h 2 0x01ff" "0x02ff" "0x1.000p-24" "B2"
    "h 3 0x01ff" "0x02ff" "0x0.000p+0" "B2"
    "h 2 0x01ff" "0x82ff" "-0x0.000p+0" "B2"
    "h 3 0x01ff" "0x82ff" "-0x1.000p-24" "B2"

    "h 0 0xf800" "0x0200" "-0x1.000p+0" "B3"
    "h 1 0xf800" "0x0200" "-0x1.000p+0" "B3"

    "h 0 0x1400" "0x0200" "0x0.000p+0" "B4"
    "h 1 0x1400" "0x0200" "0x0.000p+0" "B4"
    "h 2 0x1400" "0x0200" "0x1.000p-24" "B4"
    "h 3 0x1400" "0x0200" "0x0.000p+0" "B4"

    "h 0 0x1800" "0x0200" "0x1.000p-24" "B5"
    "h 1 0x1800" "0x0200" "0x1.000p-24" "B5"
    "h 2 0x1800" "0x0200" "0x1.000p-24" "B5"
    "h 3 0x1800" "0x0200" "0x1.000p-24" "B5"

    "h 0 0xf800" "0xf800" "0x1.ffcp+15" "B6"
    "h 1 0xf800" "0x7800" "-0x1.ffcp+15" "B6"
    "h 3 0x7400" "0x4400" "0x1.ffcp+15" "B6"
    "h 2 0x4400" "0x7400" "inf" "B6"

    "h 0 0x2400" "0x1C00" "0x1.000p-14" "B7"

    "h 0 0x2400" "0x1C00" "0x1.000p-14" "B7"

    "h 0 0x0800" "0x8c00" "-0x0.000p+0" "B8"
    "h 1 0x0800" "0x8c00" "-0x0.000p+0" "B8"
    "h 2 0x0800" "0x8c00" "-0x0.000p+0" "B8"
    "h 3 0x0800" "0x8c00" "-0x1.000p-24" "B8"

    "h 0 0x1400" "0x1800" "0x1.000p-19" "B9"
    "h 1 0x1800" "0x1400" "0x1.000p-19" "B9"
    "h 2 0x0C00" "0x0C00" "0x1.000p-24" "B9"

    "f 0 0x414587dd" "0x42ebf110" "0x1.6c1b72p+10" "From ci.yaml"
    "f 1 0x414587dd" "0x42ebf110" "0x1.6c1b72p+10" "From ci.yaml"
    "f 2 0x414587dd" "0x42ebf110" "0x1.6c1b74p+10" "From ci.yaml"
    "f 3 0x414587dd" "0x42ebf110" "0x1.6c1b72p+10" "From ci.yaml"

    "h 0 0x4145" "0x42eb" "0x1.238p+3" "From ci.yaml"
    "h 1 0x4145" "0x42eb" "0x1.23cp+3" "From ci.yaml"
    "h 2 0x4145" "0x42eb" "0x1.23cp+3" "From ci.yaml"
    "h 0 0x4145" "0x42eb" "0x1.238p+3" "From ci.yaml"

"8.8 0 0x40bf" "0x3aa2" "-43.757" "extra"
"8.8 1 0x40bf" "0x3aa2" "-43.754" "extra"
"8.8 2 0x40bf" "0x3aa2" "-43.753" "extra"
"8.8 3 0x40bf" "0x3aa2" "-43.758" "extra"
"8.8 0 0x2446" "0x7483" "-125.722" "extra"
"8.8 1 0x2446" "0x7483" "-125.719" "extra"
"8.8 2 0x2446" "0x7483" "-125.718" "extra"
"8.8 3 0x2446" "0x7483" "-125.723" "extra"
"8.8 0 0x4d2f" "0x3c45" "43.816" "extra"
"8.8 1 0x4d2f" "0x3c45" "43.820" "extra"
"8.8 2 0x4d2f" "0x3c45" "43.821" "extra"
"8.8 3 0x4d2f" "0x3c45" "43.816" "extra"
"8.8 0 0x68b2" "0x6b2a" "-44.425" "extra"
"8.8 1 0x68b2" "0x6b2a" "-44.426" "extra"
"8.8 2 0x68b2" "0x6b2a" "-44.421" "extra"
"8.8 3 0x68b2" "0x6b2a" "-44.426" "extra"
"8.8 0 0x3093" "0x6933" "-10.031" "extra"
"8.8 1 0x3093" "0x6933" "-10.031" "extra"
"8.8 2 0x3093" "0x6933" "-10.027" "extra"
"8.8 3 0x3093" "0x6933" "-10.032" "extra"
"8.8 0 0x4205" "0x4ec4" "80.066" "extra"
"8.8 1 0x4205" "0x4ec4" "80.070" "extra"
"8.8 2 0x4205" "0x4ec4" "80.071" "extra"
"8.8 3 0x4205" "0x4ec4" "80.066" "extra"
"8.8 0 0x3451" "0x356a" "-21.570" "extra"
"8.8 1 0x3451" "0x356a" "-21.566" "extra"
"8.8 2 0x3451" "0x356a" "-21.566" "extra"
"8.8 3 0x3451" "0x356a" "-21.571" "extra"
"8.8 0 0x52e4" "0x0a7c" "101.054" "extra"
"8.8 1 0x52e4" "0x0a7c" "101.055" "extra"
"8.8 2 0x52e4" "0x0a7c" "101.059" "extra"
"8.8 3 0x52e4" "0x0a7c" "101.054" "extra"
"8.8 0 0x4190" "0x5bac" "122.234" "extra"
"8.8 1 0x4190" "0x5bac" "122.238" "extra"
"8.8 2 0x4190" "0x5bac" "122.239" "extra"
"8.8 3 0x4190" "0x5bac" "122.234" "extra"
"8.8 0 0x24da" "0x56d0" "127.175" "extra"
"8.8 1 0x24da" "0x56d0" "127.176" "extra"
"8.8 2 0x24da" "0x56d0" "127.180" "extra"
"8.8 3 0x24da" "0x56d0" "127.175" "extra"
"8.8 0 0x463c" "0x7178" "33.406" "extra"
"8.8 1 0x463c" "0x7178" "33.406" "extra"
"8.8 2 0x463c" "0x7178" "33.411" "extra"
"8.8 3 0x463c" "0x7178" "33.406" "extra"
"8.8 0 0x40d1" "0x0c76" "39.671" "extra"
"8.8 1 0x40d1" "0x0c76" "39.672" "extra"
"8.8 2 0x40d1" "0x0c76" "39.676" "extra"
"8.8 3 0x40d1" "0x0c76" "39.671" "extra"
"8.8 0 0x01d8" "0x4867" "-122.511" "extra"
"8.8 1 0x01d8" "0x4867" "-122.508" "extra"
"8.8 2 0x01d8" "0x4867" "-122.507" "extra"
"8.8 3 0x01d8" "0x4867" "-122.512" "extra"
"8.8 0 0x38b7" "0x2280" "-91.339" "extra"
"8.8 1 0x38b7" "0x2280" "-91.336" "extra"
"8.8 2 0x38b7" "0x2280" "-91.335" "extra"
"8.8 3 0x38b7" "0x2280" "-91.340" "extra"
"8.8 0 0x06c7" "0x1394" "-123.312" "extra"
"8.8 1 0x06c7" "0x1394" "-123.312" "extra"
"8.8 2 0x06c7" "0x1394" "-123.308" "extra"
"8.8 3 0x06c7" "0x1394" "-123.313" "extra"
"8.8 0 0x10f5" "0x4fee" "75.367" "extra"
"8.8 1 0x10f5" "0x4fee" "75.371" "extra"
"8.8 2 0x10f5" "0x4fee" "75.372" "extra"
"8.8 3 0x10f5" "0x4fee" "75.367" "extra"
"8.8 0 0x7d4c" "0x0136" "-104.273" "extra"
"8.8 1 0x7d4c" "0x0136" "-104.273" "extra"
"8.8 2 0x7d4c" "0x0136" "-104.269" "extra"
"8.8 3 0x7d4c" "0x0136" "-104.274" "extra"
"8.8 0 0x6ed1" "0x0a03" "85.460" "extra"
"8.8 1 0x6ed1" "0x0a03" "85.461" "extra"
"8.8 2 0x6ed1" "0x0a03" "85.465" "extra"
"8.8 3 0x6ed1" "0x0a03" "85.460" "extra"
"8.8 0 0x5781" "0x0728" "114.199" "extra"
"8.8 1 0x5781" "0x0728" "114.199" "extra"
"8.8 2 0x5781" "0x0728" "114.204" "extra"
"8.8 3 0x5781" "0x0728" "114.199" "extra"
"8.8 0 0x0df7" "0x1d98" "-98.730" "extra"
"8.8 1 0x0df7" "0x1d98" "-98.727" "extra"
"8.8 2 0x0df7" "0x1d98" "-98.726" "extra"
"8.8 3 0x0df7" "0x1d98" "-98.731" "extra"
"8.8 0 0x5fd6" "0x0e5f" "97.265" "extra"
"8.8 1 0x5fd6" "0x0e5f" "97.266" "extra"
"8.8 2 0x5fd6" "0x0e5f" "97.270" "extra"
"8.8 3 0x5fd6" "0x0e5f" "97.265" "extra"
"8.8 0 0x0c59" "0x2a4c" "10.265" "extra"
"8.8 1 0x0c59" "0x2a4c" "10.266" "extra"
"8.8 2 0x0c59" "0x2a4c" "10.270" "extra"
"8.8 3 0x0c59" "0x2a4c" "10.265" "extra"
"8.8 0 0x17a1" "0x5e9f" "-68.210" "extra"
"8.8 1 0x17a1" "0x5e9f" "-68.207" "extra"
"8.8 2 0x17a1" "0x5e9f" "-68.207" "extra"
"8.8 3 0x17a1" "0x5e9f" "-68.211" "extra"
"8.8 0 0x460b" "0x583d" "36.468" "extra"
"8.8 1 0x460b" "0x583d" "36.473" "extra"
"8.8 2 0x460b" "0x583d" "36.473" "extra"
"8.8 3 0x460b" "0x583d" "36.468" "extra"
"8.8 0 0x3813" "0x7e47" "-87.097" "extra"
"8.8 1 0x3813" "0x7e47" "-87.098" "extra"
"8.8 2 0x3813" "0x7e47" "-87.093" "extra"
"8.8 3 0x3813" "0x7e47" "-87.098" "extra"
"8.8 0 0x3280" "0x65b4" "16.007" "extra"
"8.8 1 0x3280" "0x65b4" "16.008" "extra"
"8.8 2 0x3280" "0x65b4" "16.008" "extra"
"8.8 3 0x3280" "0x65b4" "16.007" "extra"
"8.8 0 0x375f" "0x454c" "-2.957" "extra"
"8.8 1 0x375f" "0x454c" "-2.957" "extra"
"8.8 2 0x375f" "0x454c" "-2.953" "extra"
"8.8 3 0x375f" "0x454c" "-2.958" "extra"
"8.8 0 0x2abb" "0x6e5e" "108.039" "extra"
"8.8 1 0x2abb" "0x6e5e" "108.043" "extra"
"8.8 2 0x2abb" "0x6e5e" "108.043" "extra"
"8.8 3 0x2abb" "0x6e5e" "108.039" "extra"
"8.8 0 0x46a0" "0x6214" "14.765" "extra"
"8.8 1 0x46a0" "0x6214" "14.766" "extra"
"8.8 2 0x46a0" "0x6214" "14.770" "extra"
"8.8 3 0x46a0" "0x6214" "14.765" "extra"
"8.8 0 0x65a2" "0x7ea2" "70.046" "extra"
"8.8 1 0x65a2" "0x7ea2" "70.051" "extra"
"8.8 2 0x65a2" "0x7ea2" "70.051" "extra"
"8.8 3 0x65a2" "0x7ea2" "70.046" "extra"
)
debug_tests_B=1
if [[ $debug_tests_B == 1 ]]; then
  echo Testing tests_for_mul_h...
  lengthB=${#testsB[@]}
  for (( i=0; i<$(($lengthB / 4)); ++i)); do
    z=`python3.11 main.py ${testsB[$((4*$i))]} \* ${testsB[$((4*$i + 1))]}`
    if [[ $z != ${testsB[$((4*$i + 2))]} ]]; then
      echo "Error in test $i (type = ${testsB[$((4*$i + 3))]}): calculating the ${testsB[$((4*$i))]} * ${testsB[$((4*$i + 1))]}, $z found, but ${testsB[$((4*$i + 2))]} expected"
    fi
  done
fi

testsC=(
  "h 0 0x5401 / 0x4400" "0x1.004p+4" "C"
  "h 1 0x5401 / 0x4400" "0x1.004p+4" "C"
  "h 2 0x5401 / 0x4400" "0x1.004p+4" "C"
  "h 3 0x5401 / 0x4400" "0x1.004p+4" "C"

  "h 0 0x1C00 / 0x2400" "0x1.000p-2" "C"
  "h 0 0x2400 / 0x2400" "0x1.000p+0" "C"
  "h 0 0x2400 / 0x1C00" "0x1.000p+2" "C"

  "f 0 0x1 / 0x0" "inf" "From ci.yaml"
  "f 0 0xff800000 / 0x7f800000" "nan" "From ci.yaml"

  "f 0 0x414587dd / 0x42ebf110" "0x1.aca5aep-4" "From ci.yaml"
  "f 1 0x414587dd / 0x42ebf110" "0x1.aca5aep-4" "From ci.yaml"
  "f 2 0x414587dd / 0x42ebf110" "0x1.aca5b0p-4" "From ci.yaml"
  "f 3 0x414587dd / 0x42ebf110" "0x1.aca5aep-4" "From ci.yaml"

  "h 0 0x4400 / 0x47ff" "0x1.000p-1" "C"
  "h 1 0x4400 / 0x47ff" "0x1.004p-1" "C"
  "h 2 0x4400 / 0x47ff" "0x1.004p-1" "C"
  "h 3 0x4400 / 0x47ff" "0x1.000p-1" "C"
)
debug_tests_C=1
if [[ $debug_tests_C == 1 ]]; then
  echo Testing tests_for_div_h...
  lengthC=${#testsC[@]}
  for (( i=0; i<$(($lengthC / 3)); ++i)); do
    z=`python3.11 main.py ${testsC[$((3*$i))]}`
    if [[ $z != ${testsC[$((3*$i + 1))]} ]]; then
      echo "Error in test $i (type = ${testsC[$((3*$i + 2))]}): calculating the ${testsC[$((3*$i))]}, $z found, but ${testsC[$((3*$i + 1))]} expected"
    fi
  done
fi


testsO=(
  "16.12 0 0x17360" "23.210"
  "16.12 1 0x17360" "23.211"
  "8.8 2 0x9c9f" "-99.378"
  "8.8 3 0x9c9f" "-99.379"
  "f 0 0xB9CD542" "0x1.39aa84p-104"
  "f 1 0x3" "0x1.800000p-148"
  "8.8 0 0x9c9f + 0x1736" "-76.167"
  "8.8 1 0x9c9f + 0x1736" "-76.168"
  "16.16 2 0x6f7600 + 0x173600" "134.672"
  "16.16 3 0x6f7600 + 0x173600" "134.671"
  "f 0 0x0" "0x0.000000p+0"
  "f 0 0x7f800000" "inf"
  "f 0 0xff800000" "-inf"
  "f 0 0x7fc00000" "nan"
  "f 0 0x1 / 0x0" "inf"
  "f 0 0xff800000 / 0x7f800000" "nan"
  "f 0 0x80000000 + 0x80000000" "-0x0.000000p+0"
  "f 1 0x80000000 + 0x80000000" "-0x0.000000p+0"
  "f 2 0x80000000 + 0x80000000" "-0x0.000000p+0"
  "f 3 0x80000000 + 0x80000000" "-0x0.000000p+0"
  "f 3 0x80000000 + 0x00000000" "-0x0.000000p+0"
  "f 3 0x00000000 + 0x80000000" "-0x0.000000p+0"
  "f 3 0xdfa2562d + 0x5fa2562d" "-0x0.000000p+0"
  "f 3 0x11111111 + 0x91111111" "-0x0.000000p+0"
  "f 3 0x2aaaaaaa + 0xaaaaaaaa" "-0x0.000000p+0"
  "f 2 0x80000000 + 0x00000000" "0x0.000000p+0"
  "f 2 0x00000000 + 0x80000000" "0x0.000000p+0"
  "f 2 0xdfa2562d + 0x5fa2562d" "0x0.000000p+0"
  "f 2 0x11111111 + 0x91111111" "0x0.000000p+0"
  "f 2 0x2aaaaaaa + 0xaaaaaaaa" "0x0.000000p+0"
  "f 1 0x80000000 + 0x00000000" "0x0.000000p+0"
  "f 1 0x00000000 + 0x80000000" "0x0.000000p+0"
  "f 1 0xdfa2562d + 0x5fa2562d" "0x0.000000p+0"
  "f 1 0x11111111 + 0x91111111" "0x0.000000p+0"
  "f 1 0x2aaaaaaa + 0xaaaaaaaa" "0x0.000000p+0"
  "f 0 0x80000000 + 0x00000000" "0x0.000000p+0"
  "f 0 0x00000000 + 0x80000000" "0x0.000000p+0"
  "f 0 0xdfa2562d + 0x5fa2562d" "0x0.000000p+0"
  "f 0 0x11111111 + 0x91111111" "0x0.000000p+0"
  "f 0 0x2aaaaaaa + 0xaaaaaaaa" "0x0.000000p+0"
)
debug_tests_O=1
if [[ $debug_tests_O == 1 ]]; then
  echo Testing tests_for_output_and_some_other...
  lengthO=${#testsO[@]}
  for (( i=0; i<$(($lengthO / 2)); ++i)); do
    z=`python3.11 main.py ${testsO[$((2*$i))]}`
    if [[ $z != ${testsO[$((2*$i + 1))]} ]]; then
      echo "Error in test $i (type = O): calculating the ${testsO[$((2*$i))]}, $z found, but ${testsO[$((2*$i + 1))]} expected"
    fi
  done
fi

testsN=(
"12.8 0 0x4a595 / 0x2848b" "1.843"
"12.8 1 0x4a595 / 0x2848b" "1.844"
"12.8 2 0x4a595 / 0x2848b" "1.848"
"12.8 3 0x4a595 / 0x2848b" "1.843"
"12.8 0 0x40145 / 0x43504" "0.949"
"12.8 1 0x40145 / 0x43504" "0.953"
"12.8 2 0x40145 / 0x43504" "0.954"
"12.8 3 0x40145 / 0x43504" "0.949"
"12.8 0 0x1e180 / 0x56193" "0.347"
"12.8 1 0x1e180 / 0x56193" "0.348"
"12.8 2 0x1e180 / 0x56193" "0.352"
"12.8 3 0x1e180 / 0x56193" "0.347"
"12.8 0 0x25df9 / 0x69f25" "0.355"
"12.8 1 0x25df9 / 0x69f25" "0.359"
"12.8 2 0x25df9 / 0x69f25" "0.360"
"12.8 3 0x25df9 / 0x69f25" "0.355"
"12.8 0 0x0c6f5 / 0x49dd1" "0.167"
"12.8 1 0x0c6f5 / 0x49dd1" "0.168"
"12.8 2 0x0c6f5 / 0x49dd1" "0.172"
"12.8 3 0x0c6f5 / 0x49dd1" "0.167"
"12.8 0 0x67f19 / 0x2b3f5" "2.402"
"12.8 1 0x67f19 / 0x2b3f5" "2.402"
"12.8 2 0x67f19 / 0x2b3f5" "2.407"
"12.8 3 0x67f19 / 0x2b3f5" "2.402"
"12.8 0 0x6ae67 / 0x06b4e" "15.937"
"12.8 1 0x6ae67 / 0x06b4e" "15.941"
"12.8 2 0x6ae67 / 0x06b4e" "15.942"
"12.8 3 0x6ae67 / 0x06b4e" "15.937"
"12.8 0 0x1788a / 0x4e91a" "0.296"
"12.8 1 0x1788a / 0x4e91a" "0.301"
"12.8 2 0x1788a / 0x4e91a" "0.301"
"12.8 3 0x1788a / 0x4e91a" "0.296"
"12.8 0 0x3a5ca / 0x5e10e" "0.617"
"12.8 1 0x3a5ca / 0x5e10e" "0.621"
"12.8 2 0x3a5ca / 0x5e10e" "0.622"
"12.8 3 0x3a5ca / 0x5e10e" "0.617"
"12.8 0 0x3268f / 0x1596a" "2.332"
"12.8 1 0x3268f / 0x1596a" "2.336"
"12.8 2 0x3268f / 0x1596a" "2.336"
"12.8 3 0x3268f / 0x1596a" "2.332"
"12.8 0 0x30953 / 0x1fe3b" "1.523"
"12.8 1 0x30953 / 0x1fe3b" "1.523"
"12.8 2 0x30953 / 0x1fe3b" "1.528"
"12.8 3 0x30953 / 0x1fe3b" "1.523"
"12.8 0 0x0e696 / 0x4e16b" "0.183"
"12.8 1 0x0e696 / 0x4e16b" "0.184"
"12.8 2 0x0e696 / 0x4e16b" "0.188"
"12.8 3 0x0e696 / 0x4e16b" "0.183"
"12.8 0 0x1ef61 / 0x0c22d" "2.550"
"12.8 1 0x1ef61 / 0x0c22d" "2.551"
"12.8 2 0x1ef61 / 0x0c22d" "2.555"
"12.8 3 0x1ef61 / 0x0c22d" "2.550"
"12.8 0 0x444ac / 0x22a85" "1.968"
"12.8 1 0x444ac / 0x22a85" "1.969"
"12.8 2 0x444ac / 0x22a85" "1.973"
"12.8 3 0x444ac / 0x22a85" "1.968"
"12.8 0 0x337c5 / 0x7d094" "0.410"
"12.8 1 0x337c5 / 0x7d094" "0.410"
"12.8 2 0x337c5 / 0x7d094" "0.415"
"12.8 3 0x337c5 / 0x7d094" "0.410"
"12.8 0 0x038e9 / 0x47eeb" "0.046"
"12.8 1 0x038e9 / 0x47eeb" "0.051"
"12.8 2 0x038e9 / 0x47eeb" "0.051"
"12.8 3 0x038e9 / 0x47eeb" "0.046"
"12.8 0 0x2e160 / 0x74e9b" "0.390"
"12.8 1 0x2e160 / 0x74e9b" "0.395"
"12.8 2 0x2e160 / 0x74e9b" "0.395"
"12.8 3 0x2e160 / 0x74e9b" "0.390"
"12.8 0 0x77d36 / 0x1b538" "4.382"
"12.8 1 0x77d36 / 0x1b538" "4.387"
"12.8 2 0x77d36 / 0x1b538" "4.387"
"12.8 3 0x77d36 / 0x1b538" "4.382"
"12.8 0 0x16884 / 0x25b3d" "0.593"
"12.8 1 0x16884 / 0x25b3d" "0.598"
"12.8 2 0x16884 / 0x25b3d" "0.598"
"12.8 3 0x16884 / 0x25b3d" "0.593"
"12.8 0 0x0b0c5 / 0x20c68" "0.335"
"12.8 1 0x0b0c5 / 0x20c68" "0.336"
"12.8 2 0x0b0c5 / 0x20c68" "0.340"
"12.8 3 0x0b0c5 / 0x20c68" "0.335"
"12.8 0 0x70e4d / 0x70ed0" "0.996"
"12.8 1 0x70e4d / 0x70ed0" "1.000"
"12.8 2 0x70e4d / 0x70ed0" "1.000"
"12.8 3 0x70e4d / 0x70ed0" "0.996"
"12.8 0 0x424ac / 0x510b8" "0.816"
"12.8 1 0x424ac / 0x510b8" "0.816"
"12.8 2 0x424ac / 0x510b8" "0.821"
"12.8 3 0x424ac / 0x510b8" "0.816"
"12.8 0 0x1069a / 0x436d4" "0.242"
"12.8 1 0x1069a / 0x436d4" "0.242"
"12.8 2 0x1069a / 0x436d4" "0.247"
"12.8 3 0x1069a / 0x436d4" "0.242"
"12.8 0 0x274d9 / 0x3228e" "0.781"
"12.8 1 0x274d9 / 0x3228e" "0.785"
"12.8 2 0x274d9 / 0x3228e" "0.786"
"12.8 3 0x274d9 / 0x3228e" "0.781"
"12.8 0 0x4ec95 / 0x0c427" "6.425"
"12.8 1 0x4ec95 / 0x0c427" "6.426"
"12.8 2 0x4ec95 / 0x0c427" "6.430"
"12.8 3 0x4ec95 / 0x0c427" "6.425"
"12.8 0 0x06c01 / 0x7ebbb" "0.050"
"12.8 1 0x06c01 / 0x7ebbb" "0.055"
"12.8 2 0x06c01 / 0x7ebbb" "0.055"
"12.8 3 0x06c01 / 0x7ebbb" "0.050"
"12.8 0 0x12adc / 0x592ca" "0.207"
"12.8 1 0x12adc / 0x592ca" "0.211"
"12.8 2 0x12adc / 0x592ca" "0.211"
"12.8 3 0x12adc / 0x592ca" "0.207"
"12.8 0 0x15977 / 0x1e500" "0.710"
"12.8 1 0x15977 / 0x1e500" "0.711"
"12.8 2 0x15977 / 0x1e500" "0.715"
"12.8 3 0x15977 / 0x1e500" "0.710"
"12.8 0 0x6a806 / 0x424f3" "1.605"
"12.8 1 0x6a806 / 0x424f3" "1.605"
"12.8 2 0x6a806 / 0x424f3" "1.610"
"12.8 3 0x6a806 / 0x424f3" "1.605"
"12.8 0 0x247ab / 0x1050d" "2.234"
"12.8 1 0x247ab / 0x1050d" "2.234"
"12.8 2 0x247ab / 0x1050d" "2.239"
"12.8 3 0x247ab / 0x1050d" "2.234"

)

debug_tests_N=1
if [[ $debug_tests_N == 1 ]]; then
  echo Testing New_tests...
  lengthO=${#testsN[@]}
  for (( i=0; i<$(($lengthO / 2)); ++i)); do
    z=`python3.11 main.py ${testsN[$((2*$i))]}`
    if [[ $z != ${testsN[$((2*$i + 1))]} ]]; then
      echo "Error in test $i (type = O): calculating the ${testsN[$((2*$i))]}, $z found, but ${testsN[$((2*$i + 1))]} expected"
    fi
  done
fi

echo Check finished