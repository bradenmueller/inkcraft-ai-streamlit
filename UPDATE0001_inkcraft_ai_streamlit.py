 
import streamlit as st
from PIL import Image
import io
import cv2
import numpy as np

# Function to process the uploaded image with better edge detection
def process_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    
    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (3,3), 0)

    # Apply Stronger Edge Detection
    edges = cv2.Canny(blurred, threshold1=50, threshold2=200)  # Increased thresholds

    # Find and draw contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_image = np.ones_like(gray) * 255  # Create white background
    cv2.drawContours(contour_image, contours, -1, (0,0,0), 1)  # Draw black lines

    # Convert back to RGB format for displaying in Streamlit
    processed_image = cv2.cvtColor(contour_image, cv2.COLOR_GRAY2RGB)

    return Image.fromarray(processed_image)

# Streamlit UI
st.title("InkCraft AI - High-Detail Line Art Processor")

st.write("Upload an image to convert it into **high-detail black-and-white line art** with enhanced edge clarity.")

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
    st.image(processed_image, caption="Processed High-Detail Line Art", use_column_width=True)
    
    # Download processed image
    img_byte_arr = io.BytesIO()
    processed_image.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()
    
    st.download_button(label="Download Processed Image", data=img_byte_arr, file_name="high_detail_line_art.png", mime="image/png")
