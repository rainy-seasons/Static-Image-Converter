import os
import sys
from PIL import Image

def convert(file, target_type):
    filename, _ = os.path.splitext(os.path.basename(file))
    output_file = f"{filename}.{target_type.lower()}"

    with Image.open(file) as img:
        img.save(output_file)

    print(f"Saved as {output_file}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Too few arguments")
    elif len(sys.argv) > 1:
        if sys.argv[2] in valid_types:
            convert(sys.argv[1], sys.argv[2])
