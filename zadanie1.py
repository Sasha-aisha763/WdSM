import math
import random

# Generator U(0,1)

a = 16807
b = 0
c = 2147483647
x = 1  # ziarno

def set_seed(seed=None):
    global x
    if seed is None:
        x = random.randint(1, c-1)  # losowe ziarno
    else:
        x = seed

def GenU():
    global x
    x = (a * x + b) % c
    return x / c


# Rozkład Poissona

def poisson(lam):
    X = -1
    S = 1.0
    q = math.exp(-lam)

    while S > q:
        U = GenU()
        S *= U
        X += 1

    return X


# Rozkład Normalny

def normal(mu, sigma):
    U1 = GenU()
    U2 = GenU()

    Z = math.sqrt(-2 * math.log(U1)) * math.cos(2 * math.pi * U2)
    return mu + sigma * Z
print("Generator U(0,1) z ziarnem 1000:")
set_seed(1000)

# Histogram tekstowy

def histogram(data, bins=10):
    minimum = min(data)
    maximum = max(data)
    width = (maximum - minimum) / bins

    counts = [0] * bins

    for value in data:
        index = int((value - minimum) / width)
        if index == bins:
            index -= 1
        counts[index] += 1

    for i in range(bins):
        print(f"{round(minimum + i*width,2):>6} - "
              f"{round(minimum + (i+1)*width,2):>6} | "
              + "*" * (counts[i] // 10))


n = 1000        # liczba generowanych liczb
lam = 3         # parametr Poissona
mu = 0          # średnia
sigma = 1       # odchylenie standardowe

use_seed = True  # True = z ziarnem, False = bez

if use_seed:
    set_seed(1000)
else:
    set_seed()

# Generowanie
poisson_data = [poisson(lam) for _ in range(n)]
normal_data = [normal(mu, sigma) for _ in range(n)]

print("\nHistogram Poissona ")
histogram(poisson_data, bins=10)

print("\n Histogram Normalny")
histogram(normal_data, bins=10)