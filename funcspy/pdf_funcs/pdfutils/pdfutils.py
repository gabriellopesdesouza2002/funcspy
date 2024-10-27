from funcspy.python_funcs.python_funcs import *
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import fitz, io

def extract_pages(original_pdf_path, new_pdf_path, num_pages):
    """
    Extracts a specified number of pages from a given PDF file and creates a new PDF file using PyMuPDF (fitz).
    
    :param original_pdf_path: A string representing the path to the original PDF file.
    :param new_pdf_path: A string representing the path to the new PDF file.
    :param num_pages: An integer representing the number of pages to extract.
    
    :return: None
    
    This function uses the fitz.open function to read the original PDF file and creates a new PDF file with the
    specified number of pages using the same library. If the number of pages to extract is greater than the total number
    of pages in the original PDF file, it extracts all the available pages.

    Example:
        >>> extract_pages_fitz('input.pdf', 'output.pdf', 10)
    """
    # Open the original PDF
    doc = fitz.open(original_pdf_path)
    total_pages = doc.page_count
    
    # Calculate the number of pages to extract
    num_pages_to_extract = min(num_pages, total_pages)
    
    # Create a new PDF document for the output
    new_doc = fitz.open()  # New, empty PDF document
    
    # Loop through the specified range and add each page to the new document
    for page_num in range(num_pages_to_extract):
        page = doc.load_page(page_num)  # Load the current page
        new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)  # Insert the page into the new document
    
    # Save the new document to the specified path
    new_doc.save(new_pdf_path)
    
    # Close the documents
    doc.close()
    new_doc.close()

def split_pdf(input_path, output_dir='output_split', interval=30):
    """
    Splits a PDF file into multiple files with a specified page interval using PyMuPDF (fitz).
    
    :param input_path: The path to the input PDF file.
    :param output_dir: The directory where the output PDF files will be saved. Defaults to 'output_split'.
    :param interval: The number of pages in each output PDF file. Defaults to 30.
    """
    # Cria o diretório de saída, se não existir
    create_dir_in_current_work_dir(output_dir)
    clean_directory(output_dir)

    doc = fitz.open(input_path)
    total_pages = doc.page_count

    for start in range(0, total_pages, interval):
        end = min(start + interval, total_pages)
        output_doc = fitz.open()
        output_doc.insert_pdf(doc, from_page=start, to_page=end-1)  # to_page é inclusivo em fitz
        output_path = os.path.join(output_dir, f'output_{start + 1}-{end}.pdf')
        output_doc.save(output_path)
        output_doc.close()

    doc.close()
    return files_with_absolute_file_path(output_dir)


def text_to_pdf(text:str, filename:str, left_margin:int=70, bottom_margin:int=40, font:str='Helvetica', font_size:int=12) -> str:
    """Convert docstring to PDF

    Args:
        text (str): Docstring text for input to PDF
        filename (_type_): filename for output

    Returns:
        str: returns filename of PDF
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Set margins
    right_margin = width - left_margin
    top_margin = height - bottom_margin
    
    # Prepare text
    text = text.strip().split('\n')
    
    # Start Y position from top margin
    y_position = top_margin
    x_position = left_margin

    # Create a function to add pages if the text overflows
    def add_page_if_needed(c, y_position, bottom_margin):
        if y_position < bottom_margin:
            c.showPage()
            return top_margin  # Reset Y position back to top
        else:
            return y_position

    # Write the text line by line
    for line in text:
        # Text wrapping: split the line into a list of words
        words = line.split()
        text_line = ''
        
        for word in words:
            # Check the width of the line or word
            line_width = c.stringWidth(text_line + " " + word, font, font_size)
            
            # If the line is too wide, draw it and start a new one
            if line_width > (right_margin - left_margin):
                c.drawString(x_position, y_position, text_line)
                y_position -= 15
                y_position = add_page_if_needed(c, y_position, bottom_margin)
                text_line = word
            else:
                # Add word to line
                text_line += (" " + word) if text_line else word

        # Draw the last line for the current sentence and move to next line
        c.drawString(x_position, y_position, text_line)
        y_position -= 15
        y_position = add_page_if_needed(c, y_position, bottom_margin)

    # End writing and save the PDF
    c.showPage()
    c.save()
    
    # Move buffer position to the beginning and save PDF to file
    buffer.seek(0)
    with open(filename, 'wb') as f:
        f.write(buffer.read())

    # Close the buffer
    buffer.close()
    
    return filename