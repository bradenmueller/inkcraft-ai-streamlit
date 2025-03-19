 
import streamlit as st
from PIL import Image, ImageEnhance
import io

# Function to enhance and duplicate the uploaded image
def enhance_image(image):
    # Increase sharpness, contrast, and color saturation
    enhancer_sharpness = ImageEnhance.Sharpness(image)
    enhanced_image = enhancer_sharpness.enhance(2.0)  # Increase sharpness

    enhancer_contrast = ImageEnhance.Contrast(enhanced_image)
    enhanced_image = enhancer_contrast.enhance(1.5)  # Increase contrast

    enhancer_color = ImageEnhance.Color(enhanced_image)
    enhanced_image = enhancer_color.enhance(1.3)  # Boost colors slightly
    
    return enhanced_image

# Streamlit UI
st.title("InkCraft AI - Ultra-Quality Image Enhancer & Duplicator")

st.write("Upload an image to enhance it with **maximum sharpness, contrast, and color accuracy** while duplicating it at full quality.")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Display original image
    st.image(image, caption="Original Image", use_column_width=True)

    # Enhance image
    with st.spinner("Enhancing image..."):
        enhanced_image = enhance_image(image)
    
    # Display enhanced image
    st.image(enhanced_image, caption="Enhanced Image", use_column_width=True)
    
    # Convert enhanced image to bytes for downloading
    img_byte_arr = io.BytesIO()
    enhanced_image.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()
    
    # Provide download button
    st.download_button(label="Download Enhanced Image", data=img_byte_arr, file_name="enhanced_image.png", mime="image/png")
