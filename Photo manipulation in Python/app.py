import streamlit as st
from PIL import Image, ImageEnhance
import io

def main():
    st.title("Photo Manipulation App")  # App title
    
    # File uploader for image input
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)  # Open the uploaded image
        st.image(image, caption="Uploaded Image", use_column_width=True)  # Display image
        
        # Image Manipulation Options
        option = st.radio("Choose an operation", ("Grayscale", "Rotate", "Flip", "Enhance"))
        
        if option == "Grayscale":
            processed_img = image.convert("L")  # Convert to grayscale
            st.image(processed_img, caption="Grayscale Image", use_column_width=True)
        
        elif option == "Rotate":
            degree = st.slider("Select rotation angle", -180, 180, 0)
            processed_img = image.rotate(degree)  # Rotate image by selected degrees
            st.image(processed_img, caption=f"Rotated Image ({degree}°)", use_column_width=True)
        
        elif option == "Flip":
            flip_type = st.radio("Choose flip type", ("Horizontal", "Vertical"))
            if flip_type == "Horizontal":
                processed_img = image.transpose(Image.FLIP_LEFT_RIGHT)  # Flip horizontally
            else:
                processed_img = image.transpose(Image.FLIP_TOP_BOTTOM)  # Flip vertically
            st.image(processed_img, caption=f"{flip_type} Flipped Image", use_column_width=True)
        
        elif option == "Enhance":
            factor = st.slider("Enhancement Factor", 0.1, 3.0, 1.0)
            enhancer = ImageEnhance.Contrast(image)
            processed_img = enhancer.enhance(factor)  # Apply contrast enhancement
            st.image(processed_img, caption=f"Enhanced Image (Factor: {factor})", use_column_width=True)
        
        # Download Button
        buf = io.BytesIO()
        processed_img.save(buf, format="PNG")
        st.download_button("Download Image", buf.getvalue(), file_name="edited_image.png", mime="image/png")

if __name__ == "__main__":
    main()
