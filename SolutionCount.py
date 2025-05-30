import matplotlib.pyplot as plt
import os
from PIL import Image

# Parameters
n_start = 5   # Start of n range (inclusive)
n_end = 7     # End of n range (inclusive)
a = 1
b = 1

desktop_path = os.path.expanduser('~/Desktop')
vertical_stacks = []

for n in range(n_start, n_end + 1):
    img_folder = f"n={n}_a={a}_b={b}"
    os.makedirs(img_folder, exist_ok=True)
    img_paths = []

    # Generate and save each plot for current n
    for c in range(n):
        solutions = [(x, y) for x in range(21) for y in range(21) if (a * x**2 + b * y**2) % n == c]
        x_values = [x for x, y in solutions]
        y_values = [y for x, y in solutions]
        solution_count = len(solutions)

        plt.figure(figsize=(4, 4))
        plt.scatter(x_values, y_values, color='blue', label=f'c = {c}')
        plt.xlabel('x')
        plt.ylabel('y')
        equation_text = f"({a}x² + {b}y²) ≡ {c} (mod {n})"
        plt.text(0.5, 1.05, equation_text, fontsize=12, ha='center', transform=plt.gca().transAxes)
        # Add solution count in red at top-right
        plt.text(0.98, 0.02, f'{solution_count}', color='red', fontsize=20,
                 ha='right', va='bottom', transform=plt.gca().transAxes)
        plt.xticks(range(0, 21, 1))
        plt.yticks(range(0, 21, 1))
        plt.grid(True)
        plt.legend()
        img_path = os.path.join(img_folder, f"{c}.png")
        plt.savefig(img_path, bbox_inches='tight')
        plt.close()
        img_paths.append(img_path)

    # Stack images vertically for this n
    images = [Image.open(p) for p in img_paths]
    width = max(img.width for img in images)
    total_height = sum(img.height for img in images)
    stacked_img = Image.new('RGB', (width, total_height), color=(255, 255, 255))

    y_offset = 0
    for img in images:
        stacked_img.paste(img, (0, y_offset))
        y_offset += img.height

    vertical_stacks.append(stacked_img)

# Assemble all vertical stacks horizontally
total_width = sum(img.width for img in vertical_stacks)
max_height = max(img.height for img in vertical_stacks)
final_img = Image.new('RGB', (total_width, max_height), color=(255, 255, 255))

x_offset = 0
for img in vertical_stacks:
    final_img.paste(img, (x_offset, 0))
    x_offset += img.width

final_path = os.path.join(desktop_path, f"total_assembly_n{n_start}_to_n{n_end}_a={a}_b={b}.png")
final_img.save(final_path)
print(f"Combined image saved to {final_path}")
