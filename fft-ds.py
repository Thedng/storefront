import math

class Complex:
    def __init__(self, re=0.0, im=0.0):
        self.re = re
        self.im = im

    def __add__(self, other):
        return Complex(self.re + other.re, self.im + other.im)

    def __sub__(self, other):
        return Complex(self.re - other.re, self.im - other.im)

    def __mul__(self, other):
        return Complex(self.re * other.re - self.im * other.im,
                       self.re * other.im + self.im * other.re)

    def __str__(self):
        re = f"{self.re:.4f}"
        im = f"{self.im:+.4f}j"
        return re + im


def parse_complex(s: str) -> Complex:
    s = s.replace(" ", "")
    if 'j' not in s: 
        return Complex(float(s), 0)

    jpos = s.find('j')
    num = s[:jpos]

    if '+' not in num and '-' not in num[1:]:
        return Complex(0, float(num))

    pos = max(num.rfind('+'), num.rfind('-'))  
    if pos > 0:
        re = float(num[:pos])
        im = float(num[pos:])
    else:
        re = 0
        im = float(num)
    return Complex(re, im)


def fft(a: list[Complex]):
    n = len(a)
    if n <= 1:
        return

    even = a[0::2]
    odd = a[1::2]

    fft(even)
    fft(odd)

    for k in range(n // 2):
        angle = -2.0 * math.pi * k / n
        w = Complex(math.cos(angle), math.sin(angle))
        t = w * odd[k]
        a[k] = even[k] + t
        a[k + n // 2] = even[k] - t


def main():
    N = int(input("Number of points (power of 2): "))
    x = []
    print("Enter the samples (e.g., 1+2j or -3j or 5):")
    for i in range(N):
        s = input(f"x[{i}] = ")
        x.append(parse_complex(s))

    fft(x)

    print("\nFFT result:")
    for i in range(N):
        print(f"X[{i}] = {x[i]}")


if __name__ == "__main__":
    main()
