
import json
import zlib
from pathlib import Path
from PIL import Image
import numpy as np

def compress_image(input_path, output_path):
    img = Image.open(input_path).convert("RGB")

    # Reduce to a max of 256 colors for smaller storage
    img_p = img.convert("P", palette=Image.ADAPTIVE, colors=256)

    palette = img_p.getpalette()[:768]  # First 256 colors (256 * 3 RGB)
    palette = [palette[i:i+3] for i in range(0, len(palette), 3)]

    arr = np.array(img_p)

    data = {
        "size": img.size,
        "palette": palette,
        "pixels": arr.flatten().tolist()
    }

    # Convert to JSON and compress with zlib
    compressed_data = zlib.compress(json.dumps(data).encode("utf-8"), level=9)

    with open(output_path, "wb") as f:
        f.write(compressed_data)

    print(f"Wrote {output_path} | {img.size[0]}x{img.size[1]} | palette entries: {len(palette)}")

if __name__ == "__main__":
    import sys
    compress_image(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else sys.argv[1] + ".genesis")
