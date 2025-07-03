
import os

# Parameters
m = 5
n = m ** 3
a_start = 1
a_end = 1
b_start = 0
b_end = 7

# Precompute x^2 and y^2 for x, y in 0..n-1
x2 = [x * x for x in range(n)]
y2 = [y * y for y in range(n)]

total_solutions = 0

for a in range(a_start, a_end + 1):
    for b in range(b_start, b_end + 1):
        for c in range(n):
            solution_count = 0
            for x_sq in x2:
                for y_sq in y2:
                    if (a * x_sq + b * y_sq) % n == c:
                        solution_count += 1
            total_solutions += solution_count

print(f"Total number of solutions: {total_solutions}")
print(f"Total number of solutions divided by m={m}: {total_solutions / m}")
print(f"Total number of solutions divided by n={n}: {total_solutions / n}")
