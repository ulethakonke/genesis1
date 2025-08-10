import streamlit as st
from compress import compress_image
from decompress import decompress_image
from pathlib import Path
import tempfile

st.set_page_config(page_title="SoulGenesis", page_icon="✨", layout="centered")
st.title("✨ SoulGenesis – Image Compression & Reconstruction")

st.write("Upload an image to compress it into a `.genesis` file, or upload a `.genesis` file to reconstruct the image.")

# Compression section
st.header("📦 Compress Image to .genesis")
img_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"], key="img_upload")

if img_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(img_file.name).suffix) as tmp_in:
        tmp_in.write(img_file.read())
        tmp_in_path = tmp_in.name

    out_path = Path(tempfile.gettempdir()) / (Path(img_file.name).stem + ".genesis")
    compress_image(tmp_in_path, out_path)
    st.success(f"Image compressed and saved as: {out_path.name}")

    with open(out_path, "rb") as f:
        st.download_button("⬇️ Download .genesis file", f, file_name=out_path.name)

# Decompression section
st.header("🔄 Reconstruct Image from .genesis")
genesis_file = st.file_uploader("Choose a .genesis file", type=["genesis"], key="genesis_upload")

if genesis_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".genesis") as tmp_in:
        tmp_in.write(genesis_file.read())
        tmp_in_path = tmp_in.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_out:
        tmp_out_path = tmp_out.name

    decompress_image(tmp_in_path, tmp_out_path)

    from PIL import Image
    img = Image.open(tmp_out_path)
    st.image(img, caption="Reconstructed Image", use_container_width=True)

    with open(tmp_out_path, "rb") as f:
        st.download_button("⬇️ Download Reconstructed Image", f, file_name="reconstructed.png")
