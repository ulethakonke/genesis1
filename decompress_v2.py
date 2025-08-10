import json
import zlib
from PIL import Image
import numpy as np

def decompress_image(input_path, output_path):
    # Read compressed data
    with open(input_path, "rb") as f:
        compressed_data = f.read()

    # Decompress and parse JSON
    data = json.loads(zlib.decompress(compressed_data).decode("utf-8"))

    size = tuple(data["size"])
    palette = data["palette"]
    pixels = np.array(data["pixels"], dtype=np.uint8).reshape(size[1], size[0])

    img_p = Image.fromarray(pixels, mode="P")

    # Flatten palette list back to a single array
    flat_palette = []
    for rgb in palette:
        flat_palette.extend(rgb)
    img_p.putpalette(flat_palette)

    # Convert back to RGB
    img_rgb = img_p.convert("RGB")
    img_rgb.save(output_path)
    print(f"Wrote reconstructed image to {output_path}")

if __name__ == "__main__":
    import sys
    decompress_image(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else sys.argv[1].replace(".genesis", ".recon.png"))
