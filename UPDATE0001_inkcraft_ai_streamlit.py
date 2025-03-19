 
import streamlit as st
from PIL import Image
import io
import cv2
import numpy as np

# Function to process the uploaded image
def process_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    
    # Use Adaptive Thresholding to capture more details
    adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Apply Canny edge detection with lower thresholds for fine details
    edges = cv2.Canny(gray, threshold1=30, threshold2=120)

    # Invert the edges (so black lines appear on a white background)
    inverted_edges = cv2.bitwise_not(edges)

    # Use morphological transformations to refine lines
    kernel = np.ones((2,2), np.uint8)  # Adjust thickness
    refined_edges = cv2.dilate(inverted_edges, kernel, iterations=1)
    refined_edges = cv2.erode(refined_edges, kernel, iterations=1)

    # Convert back to RGB format for displaying in Streamlit
    processed_image = cv2.cvtColor(refined_edges, cv2.COLOR_GRAY2RGB)
    
    return Image.fromarray(processed_image)

# Streamlit UI
st.title("InkCraft AI - Enhanced Line Art Processor")

st.write("Upload an image to convert it into **high-detail black-and-white line art.** This version emphasizes **every shape and contour with enhanced precision.**")

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
