 
import streamlit as st
from PIL import Image
import io
import cv2
import numpy as np

# Function to process the uploaded image with extreme detail
def process_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    
    # Apply a stronger Gaussian Blur to smooth out noise while keeping details
    blurred = cv2.GaussianBlur(gray, (3,3), 0)

    # Use Canny edge detection with fine-tuned thresholds for maximum detail extraction
    edges = cv2.Canny(blurred, threshold1=20, threshold2=250)  # Lower first value for more details

    # Find contours for extreme detail extraction
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_image = np.ones_like(gray) * 255  # Create a white background
    cv2.drawContours(contour_image, contours, -1, (0,0,0), 1)  # Draw ultra-fine black lines

    # Apply additional sharpening to enhance line precision
    kernel_sharpen = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(contour_image, -1, kernel_sharpen)

    # Convert back to RGB format for displaying in Streamlit
    processed_image = cv2.cvtColor(sharpened, cv2.COLOR_GRAY2RGB)

    return Image.fromarray(processed_image)

# Streamlit UI
st.title("InkCraft AI - Ultra-High-Detail Line Art Processor")

st.write("Upload an image to convert it into **extremely detailed black-and-white line art** with ultra-precise contour detection, like a **Marvel or DC comic book illustration**.")

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
    st.image(processed_image, caption="Ultra-High-Detail Line Art", use_column_width=True)
    
    # Download processed image
    img_byte_arr = io.BytesIO()
    processed_image.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()
    
    st.download_button(label="Download Processed Image", data=img_byte_arr, file_name="ultra_high_detail_line_art.png", mime="image/png")
