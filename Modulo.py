import matplotlib.pyplot as plt

# Define the value of n and coefficients a, b
n = 5
a = 1  # Coefficient for x^2
b = 1  # Coefficient for y^2

# Loop through all values of c from 0 to n-1
for c in range(n):
    solutions = []
    for x in range(21):
        for y in range(21):
            if (a * x**2 + b * y**2) % n == c:
                solutions.append((x, y))

    x_values = [x for x, y in solutions]
    y_values = [y for x, y in solutions]

    plt.scatter(x_values, y_values, color='blue', label=f'c = {c}')
    plt.xlabel('x')
    plt.ylabel('y')
    equation_text = f"({a}x² + {b}y²) ≡ {c} (mod {n})"
    plt.text(0.5, 1.05, equation_text, fontsize=12, ha='center', transform=plt.gca().transAxes)
    plt.xticks(range(21))
    plt.yticks(range(21))
    plt.grid(True)
    plt.legend()
    plt.show()
