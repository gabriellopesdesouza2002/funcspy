from funcspy.python_funcs.python_funcs import *
from tqdm import tqdm
from PIL import Image
import numpy as np
import fitz, uuid, os, pytesseract, base64

def make_ocr_in_pdf_offline(path_pdf: str, export_from_file_txt: str = False) -> str:
    """
    Convert pdf(s) to text with fitz (PyMuPDF)
        
    Attention, it only works correctly on PDF's where the text is selectable!
    
    Args:
        path_pdf (str): path of the pdf
        export_from_file_txt (bool | str): pass a txt file path for the text to output
    Returns:
        str: text from PDF
    """

    text = []
    doc = fitz.open(path_pdf)
    for page in doc:
        text.append(page.get_text())
    text = "\n".join(text)
    
    if export_from_file_txt:
        with open(export_from_file_txt, 'w', encoding='utf-8') as f:
            f.write(text)
            
    return text

def ocr_google_vision(pdf, api_key, dpi=300, file_output=uuid.uuid4(), return_text=True, limit_pages=None, is_image=False):
    def detect_text(files_png: list[str], api_key) -> str:
        """Retrieves text from images
        Args:
            files_png (list[str]): List of images from the pdf
        Raises:
            Exception: != from 200 to response
        Returns:
            str: The text of the PDF
        """
        url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
        requests_json = []
        result = ''
        counter = len(files_png)
        while counter != 0:  # enquanto existir imagens...
            log(f'Retrieving 16 images from {counter} images | If you actually have 16, otherwise take the rest')
            files_png_temp = files_png[:16]
            for filepath in files_png_temp:  # faz uma lista de requests para o post
                with open(filepath, mode='rb') as file:
                    bytes_content = file.read()
                    requests_json.append(
                        {
                            "image": {
                                "content": base64.b64encode(bytes_content).decode("utf-8")
                            },
                            "features": [{"type": "TEXT_DETECTION"}]
                        }
                    )
            else:
                for i in files_png_temp:
                    files_png.remove(i)
                    

                r = requests.post(url=url, json={"requests": requests_json})
                requests_json = []  # clean for the next 10
                if r.status_code == 200:
                    # log(r.text)
                    r_json = r.json()
                    for resp in r_json['responses']:
                        try:
                            result = result + str(resp['textAnnotations'][0]['description']).strip()
                        except Exception as e:
                            log(repr(e))
                            raise Exception(repr(e))
                    else:
                        counter = len(files_png)
                else:
                    raise Exception(r.json()['error']['message'])

        return remove_accents(result.lower().strip())
    
    if is_image == False:
        with fitz.open(pdf) as pdf_fitz:
            create_dir_in_current_work_dir('pages')
            clean_directory('pages')
            log(f'Converting PDF to...')
            number_of_pages = len(pdf_fitz) if limit_pages is None else min(limit_pages, len(pdf_fitz))
            with tqdm(total=number_of_pages, desc='EXTRACT PAGES') as bar:
                for i, page in enumerate(pdf_fitz):
                    if i >= number_of_pages:
                        break
                    page = pdf_fitz.load_page(i)
                    mat = fitz.Matrix(dpi/72, dpi/72)  # Matriz de transformação usando DPI
                    pix = page.get_pixmap(matrix=mat)
                    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    image.save(f'pages/{i}.png')
                    bar.update(1)
            
        log('Sending to Google Vision...')
        files = list(files_with_absolute_file_path('pages'))
        text_ocr = detect_text(files, api_key)
        clean_directory('pages')
        if return_text:
            return text_ocr
        else:
            file_path = file_with_absolute_path('tempdir', f'{file_output}.txt')
            with open(file_path, 'w') as f:
                text_ocr.write(f)
            return file_path
    else:
        files = [pdf]
        text_ocr = detect_text(files, api_key)
        if return_text:
            return text_ocr
        else:
            file_path = file_with_absolute_path('tempdir', f'{file_output}.txt')
            with open(file_path, 'w') as f:
                text_ocr.write(f)
            return file_path
    
    
    
def ocr_tesseract_v2(pdf, dpi=300, file_output=uuid.uuid4(), return_text=True, config_tesseract='', limit_pages=None, lang='por', timeout=120, download_tesseract=False):
    """Performs OCR on a PDF file using Tesseract, with advanced customization options.

    This advanced feature allows customization of several OCR parameters, such as DPI, language, page limit, and timeout. If the Tesseract binaries are not present, it performs a single request to the Paycon organization's GitHub to download the necessary binaries. This request is crucial for the functionality of the feature but raises important questions about data security.

    Importance of Data Security in the Request:

    - Although the Tesseract ZIP file is public and hosted in a trusted repository, it is essential to validate the source before downloading to prevent the execution of malicious software.

    - During development, it is advisable to have Tesseract pre-installed in the project, eliminating the need for download and reducing the attack surface.

    - For production environments, one should consider implementing integrity checks, such as checksum validation, to ensure the authenticity of the downloaded binaries.

    Args:
    pdf (str): Path to the PDF file to perform OCR on.
    dpi (int, optional): DPI resolution for converting PDF pages to images. Default is 300.
    file_output (str, optional): Name of the output file where the OCRed text will be saved. Generates a UUID by default.
    return_text (bool, optional): If True, returns the extracted text; if False, returns the path to the text file.
    Default is True.
    config_tesseract (str, optional): Additional settings for Tesseract. Default is ''.
    limit_pages (int, optional): Limits the number of PDF pages to be processed. Default is None.
    lang (str, optional): Language code used by Tesseract for OCR. Default is 'por' (Portuguese).
    timeout (int, optional): Timeout in seconds for OCR processing of each page. Default is 120.

    Returns:
    str|bool: Returns the extracted text or the path to the text file if `return_text` is False.

    Returns False if OCR processing fails.

    Note:
    - The function attempts to download Tesseract binaries only if they are not present, to avoid unnecessary downloads and mitigate security risks.
    - Data security and software integrity are paramount, especially when downloading from external sources.

    Raises:
    Exception: May throw an exception if an error occurs during binary download, OCR processing, or if the integrity of the downloaded file is questionable.
    """
    path_exit = file_with_absolute_path('temp_tess', 'Tesseract-OCR.zip')
    path_tesseract_extract = file_with_absolute_path('bin', 'Tesseract-OCR')
    path_tesseract = file_with_absolute_path(('bin', 'Tesseract-OCR'), 'tesseract.exe')

    if not os.path.exists(path_tesseract):
        while not os.path.exists(path_tesseract):
            log('*** PLACE THE TESSERACT BINARIES IN THE BIN FOLDER (THE FOLDER NAME OF THE BINARIES MUST BE “Tesseract-OCR”) ***')
            sleep(10)
        else:
            pass
    pytesseract.pytesseract.tesseract_cmd = path_tesseract

    with fitz.open(pdf) as pdf_fitz:
        create_dir_in_current_work_dir('pages')
        clean_directory('pages')
        log(f'Converting PDF to pages...')
        number_of_pages = len(pdf_fitz) if limit_pages is None else min(limit_pages, len(pdf_fitz))
        with tqdm(total=number_of_pages, desc='EXTRACT PAGES') as bar:
            for i, page in enumerate(pdf_fitz):
                if i >= number_of_pages:
                    break
                page = pdf_fitz.load_page(i)
                mat = fitz.Matrix(dpi/72, dpi/72)  # Matriz de transformação usando DPI
                pix = page.get_pixmap(matrix=mat)
                pix.save(file_with_absolute_path('pages', f'{i}.png'))
                bar.update(1)
        

        files = files_with_absolute_file_path('pages')
        with tqdm(total=len(files), desc='OCR') as bar:
            for i, image in enumerate(files):
                try:
                    text = pytesseract.image_to_string(image, config=config_tesseract, lang=lang, timeout=timeout)
                except Exception as e:
                    return False
                with open(file_with_absolute_path('tempdir', f'{file_output}.txt'), 'a', encoding='utf-8') as f:
                    f.write(text)
                bar.update(1)
            else:
                clean_directory('pages')
                if return_text:
                    text_all = ''
                    with open(file_with_absolute_path('tempdir', f'{file_output}.txt'), 'r', encoding='utf-8') as f:
                        text_all = f.read()
                    os.remove(file_with_absolute_path('tempdir', f'{file_output}.txt'))
                    return text_all
                else:
                    return os.path.abspath(file_with_absolute_path('tempdir', f'{file_output}.txt'))