import streamlit as st
from PIL import Image
import io
import cv2
import numpy as np

# Function to process the uploaded image
def process_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    
    # Apply edge detection
    edges = cv2.Canny(gray, threshold1=50, threshold2=150)

    # Invert the colors (so black lines appear on a white background)
    inverted_edges = cv2.bitwise_not(edges)
    
    # Convert back to RGB format for displaying in Streamlit
    processed_image = cv2.cvtColor(inverted_edges, cv2.COLOR_GRAY2RGB)
    
    return Image.fromarray(processed_image)

# Streamlit UI
st.title("InkCraft AI - Image to Line Art Processor")

st.write("Upload an image to convert it into black-and-white line art with a white background.")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Display original image
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Process image
    with st.spinner("Processing image..."):
        processed_image = process_image(image)
    
    # Display processed image
    st.image(processed_image, caption="Processed Line Art", use_column_width=True)
    
    # Download processed image
    img_byte_arr = io.BytesIO()
    processed_image.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()
    
    st.download_button(label="Download Processed Image", data=img_byte_arr, file_name="processed_image.png", mime="image/png")
