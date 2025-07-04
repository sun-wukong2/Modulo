import os
from PIL import Image, ImageDraw, ImageFont

# Parameters
n_start = 5
n_end = 10
a_start = 1
a_end = 1
b_start = -4
b_end = 4

cell_width, cell_height = 200, 200
font_size = 80
axis_font_size = 40
label_font_size = 36
label_height = 50  # Height for the blue label at the top

desktop_path = os.path.expanduser('~/Desktop')

try:
    font = ImageFont.truetype("Arial.ttf", font_size)
    axis_font = ImageFont.truetype("Arial.ttf", axis_font_size)
    label_font = ImageFont.truetype("Arial.ttf", label_font_size)
except:
    font = ImageFont.load_default()
    axis_font = ImageFont.load_default()
    label_font = ImageFont.load_default()

images = []

for a in range(a_start, a_end + 1):
    for b in range(b_start, b_end + 1):
        vertical_stacks = []
        for n in range(n_start, n_end + 1):
            cell_images = []
            for c in range(n):
                solution_count = len([
                    (x, y) for x in range(21) for y in range(21)
                    if (a * x**2 + b * y**2) % n == c
                ])
                img = Image.new('RGB', (cell_width, cell_height), color=(255, 255, 255))
                draw = ImageDraw.Draw(img)
                text = str(solution_count)
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                x = (cell_width - text_width) // 2
                y = (cell_height - text_height) // 2
                draw.text((x, y), text, fill='red', font=font)
                cell_images.append(img)
            total_height = cell_height * len(cell_images)
            stack_img = Image.new('RGB', (cell_width, total_height), color=(255, 255, 255))
            for idx, img in enumerate(cell_images):
                stack_img.paste(img, (0, idx * cell_height))
            vertical_stacks.append(stack_img)
        max_c = max(n for n in range(n_start, n_end + 1))
        num_ns = n_end - n_start + 1
        axis_x_height = axis_font_size + 20
        axis_y_width = axis_font_size + 20
        total_width = axis_y_width + cell_width * num_ns
        total_height = axis_x_height + cell_height * max_c
        final_img = Image.new('RGB', (total_width, total_height), color=(255, 255, 255))
        draw = ImageDraw.Draw(final_img)
        for idx, n in enumerate(range(n_start, n_end + 1)):
            n_text = f"n={n}"
            bbox = draw.textbbox((0, 0), n_text, font=axis_font)
            text_width = bbox[2] - bbox[0]
            x = axis_y_width + idx * cell_width + (cell_width - text_width) // 2
            y = (axis_x_height - axis_font_size) // 2
            draw.text((x, y), n_text, fill='black', font=axis_font)
        for c in range(max_c):
            c_text = f"c={c}"
            bbox = draw.textbbox((0, 0), c_text, font=axis_font)
            text_height = bbox[3] - bbox[1]
            x = (axis_y_width - bbox[2] + bbox[0]) // 2
            y = axis_x_height + c * cell_height + (cell_height - text_height) // 2
            draw.text((x, y), c_text, fill='black', font=axis_font)
        for n_idx, stack_img in enumerate(vertical_stacks):
            n = n_start + n_idx
            for c in range(n):
                y_offset = axis_x_height + c * cell_height
                x_offset = axis_y_width + n_idx * cell_width
                final_img.paste(stack_img.crop((0, c * cell_height, cell_width, (c + 1) * cell_height)),
                                (x_offset, y_offset))
        # Add blue label at the top
        labeled_img = Image.new('RGB', (final_img.width, final_img.height + label_height), color=(255, 255, 255))
        labeled_img.paste(final_img, (0, label_height))
        label_draw = ImageDraw.Draw(labeled_img)
        label_text = f"a={a}, b={b}"
        bbox = label_draw.textbbox((0, 0), label_text, font=label_font)
        text_width = bbox[2] - bbox[0]
        x = (labeled_img.width - text_width) // 2
        y = (label_height - label_font_size) // 2
        label_draw.text((x, y), label_text, fill='blue', font=label_font)
        images.append(labeled_img)

# --- Combine all images into a PDF with 4 images per page (2x2 grid) and lines between them ---
img_w = max(img.width for img in images)
img_h = max(img.height for img in images)
page_w = img_w * 2
page_h = img_h * 2
pages = []

for i in range(0, len(images), 4):
    page = Image.new('RGB', (page_w, page_h), color=(255, 255, 255))
    for j in range(4):
        if i + j >= len(images):
            break
        img = images[i + j]
        x = (j % 2) * img_w
        y = (j // 2) * img_h
        page.paste(img, (x, y))
    # Draw lines to separate images
    draw = ImageDraw.Draw(page)
    draw.line([(img_w, 0), (img_w, page_h)], fill='black', width=4)
    draw.line([(0, img_h), (page_w, img_h)], fill='black', width=4)
    pages.append(page)

pdf_path = os.path.join(desktop_path, f"SolutionGOG_{n_start}-{n_end}_a{a_start}-{a_end}_b{b_start}-{b_end}.pdf")
pages[0].save(pdf_path, save_all=True, append_images=pages[1:])
print(f"PDF saved to {pdf_path}")
