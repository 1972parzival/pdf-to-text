import fitz 
import pytesseract
from PIL import Image
import io
import os

def pdf_to_text(pdf_filename, output_txt_filename):
  
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    pdf_path = os.path.join(script_dir, pdf_filename)
    output_txt_path = os.path.join(script_dir, output_txt_filename)
    
    print(f"PDF Path: {pdf_path}")
    print(f"Output Text Path: {output_txt_path}")
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file {pdf_path} does not exist.")
        return
    
    try:

        pdf_document = fitz.open(pdf_path)
        print(f"Opened PDF file: {pdf_filename}")
        
        full_text = ""
        
        for page_num in range(pdf_document.page_count):
            print(f"Processing page {page_num + 1} of {pdf_document.page_count}")
            
            page = pdf_document.load_page(page_num)
            
            image_list = page.get_images(full=True)
            print(f"Found {len(image_list)} images on page {page_num + 1}")
            
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    image = Image.open(io.BytesIO(image_bytes))
                    print(f"Extracted image {img_index + 1} on page {page_num + 1}")
                    
                    text = pytesseract.image_to_string(image)
                    print(f"Extracted text from image {img_index + 1} on page {page_num + 1}")
                    
                    full_text += text + "\n"
                except Exception as e:
                    print(f"Error processing image {img_index + 1} on page {page_num + 1}: {e}")
        
        with open(output_txt_path, "w") as text_file:
            text_file.write(full_text)
        print(f"Text extraction complete. Saved to {output_txt_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

pdf_filename = "input.pdf"
output_txt_filename = "output.txt"  
pdf_to_text(pdf_filename, output_txt_filename)
