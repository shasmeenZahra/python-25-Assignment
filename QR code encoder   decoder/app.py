import streamlit as st        # For building the web UI
import qrcode                 # To generate QR codes
import cv2                    # For decoding QR codes

# 🔧 Function to generate and save QR code image
def generate_qr(data):
    qr = qrcode.make(data)          # Generate QR code image from input data
    qr.save("qr_code.png")          # Save the QR code image locally
    return "qr_code.png"            # Return the file path

# 🔍 Function to decode a QR code image using OpenCV
def decode_qr(image_path):
    img = cv2.imread(image_path)    # Read the uploaded image
    qr_code_detector = cv2.QRCodeDetector()  # Initialize QR code detector
    data, _, _ = qr_code_detector.detectAndDecode(img)  # Try to detect and decode QR code
    return data if data else "No QR code found."  # Return decoded data or fallback message

# 🖼️ Streamlit UI Setup
st.title("📱 QR Code Generator & Decoder")

# 📤 Section for QR Code Generation
st.subheader("Generate QR Code")
input_text = st.text_input("Enter text or URL")  # Text input from user
if st.button("Generate"):                        # Button to trigger QR generation
    qr_path = generate_qr(input_text)            # Generate QR and get path
    st.image(qr_path, caption="Generated QR Code")  # Display the generated QR code

# 📥 Section for QR Code Decoding
st.subheader("Decode QR Code")
uploaded_file = st.file_uploader("Upload a QR Code image", type=["png", "jpg", "jpeg"])  # File upload component
if uploaded_file is not None:
    with open("uploaded_qr.png", "wb") as f:         # Save uploaded file temporarily
        f.write(uploaded_file.getbuffer())
    decoded_data = decode_qr("uploaded_qr.png")      # Decode the saved image
    st.write("Decoded Data:", decoded_data)          # Display the result
