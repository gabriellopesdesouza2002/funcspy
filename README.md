# funcspy - Functions to help you develop any program or script you want
## Functions for the main technologies

* Functions for your any project with **Python**, for any moments
* Functions for send emails easly with **Outlook** and **Gmail**
* Functions for used in your **GUI** with **Tkinter**
* Functions for use in your projects with **Openai**
* Functions most used in projects with **PDF**, exemple, **OCR**
* Functions for auxiliary in your projects with **Selenium** and **BeautifulSoup**

## Instalation

`pip install -U funcspy`

### Libraryes instalated automaticaly
* selenium
* bs4
* requests
* html5lib
* webdriver-manager
* pretty-html-table
* xlsxwriter
* pandas
* sqlalchemy
* rich
* pyinstaller
* filetype
* pytesseract
* tqdm
* pillow
* PyMuPDF
* holidays
* numpy==1.26.0

## Example of using some of the most important functions

### Emails

#### Example Usage of `send_email_gmail` Function

Below is an example of how to use the `send_email_gmail` function to send an email with multiple recipients and attachments.

```python
from funcspy.emails_funcs.emails_funcs import send_email_gmail

# Email settings
email_app_google = "your_email@gmail.com"
passwd_app_gmail = "your_app_password"
emails_to = ["recipient1@example.com", "recipient2@example.com"]
subject = "Email subject"
body_msg = "Email body in HTML format"

# Attachments (optional)
attachments = ["path/to/file1.pdf", "path/to/file2.docx"]

# Send the email
send_email_gmail(email_app_google, passwd_app_gmail, emails_to, subject, body_msg, attachments)

```

#### Example Usage of `send_email_outlook` Function

Below is an example of how to use the `send_email_outlook` function to send an email with Outlook, including options for recipients, subject, HTML body, attachments, and embedding a DataFrame.

```python
from funcspy.emails_funcs.emails_funcs import send_email_outlook

# Email settings
to = ["recipient1@example.com", "recipient2@example.com"]
subject = "E-mail Subject"
body = "<p>Hello!</p>"

# Attachments (optional)
attachments = ["path/to/file1.pdf", "path/to/file2.docx"]

# DataFrame to be embedded in email body (optional)
# Example format: [df, 'theme_on_pretty_html_table']
send_dateframe_on_body = False  # Set to [dataframe, 'theme'] if using pretty_html_table

# Send the email
send_email_outlook(to, subject, body, attachments, send_dateframe_on_body)
```

### GUI

#### Example Usage of `show_popup` Function

Below is an example of how to use the `show_popup` function to display a popup window with a specified title and message text.

```python
from funcspy.gui_funcs.gui_funcs import show_popup

# Popup settings
title = "Popup Title"
text = "This is the message displayed in the popup."

# Show the popup
show_popup(title, text)
```

### OpenAI (GPT/DALL-E/Whisper)

#### Example Usage of `api_chat_completions` Function

Below is an example of how to use the `api_chat_completions` function to send a chat completion request to the OpenAI API.

```python
from funcspy.openai_funcs.openai_funcs import api_chat_completions

# API settings
api_key = 'your_api_key'
model = 'gpt-4-turbo'
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
]

# Send the request
response = api_chat_completions(api_key, model, messages)
print(response)
```

#### Example Usage of `api_image_generation` Function

Below is an example of how to use the `api_image_generation` function to generate images via the OpenAI API.

```python
from funcspy.openai_funcs.openai_funcs import api_image_generation

# API settings
api_key = 'your_api_key'
model = 'dall-e-3'
prompt = 'a photograph of an astronaut riding a horse'
size = '1024x1024'
quality = 'standard'

# Send the request
response = api_image_generation(api_key, prompt, model, size, quality)
print(response)
```

#### Example Usage of `api_vision` Function

Below is an example of how to use the `api_vision` function to process images and answer questions about them using GPT-4 Turbo with Vision.

```python
from funcspy.openai_funcs.openai_funcs import api_vision

# API settings
api_key = 'your_api_key'
model = 'gpt-4-turbo'
messages = {
    "role": "user",
    "content": [
        {"type": "text", "text": "What’s in this image?"},
        {
            "type": "image_url",
            "image_url": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
            },
        },
    ],
}

# Send the request
response = api_vision(api_key, messages, model)
print(response)
```

#### Example Usage of `api_audio_transcription` Function

Below is an example of how to use the `api_audio_transcription` function to transcribe audio using the OpenAI API.

```python
from funcspy.openai_funcs.openai_funcs import api_audio_transcription

# API settings
api_key = 'your_api_key'
file_path = 'audio_file.mp3'
model = 'whisper-1'

# Send the request
response = api_audio_transcription(api_key, file_path, model)
print(response)
```

### PDF (OCR/Google Vision/Others)

#### Example Usage of `ocr_tesseract` Function

***It is very important to download the tesseract binaries available in the root of our library on Github***

Below is an example of how to use the `ocr_tesseract` function to perform OCR on a PDF file using Tesseract with customizable settings.

```python
from funcspy.pdf_funcs.ocr_funcs import ocr_tesseract

# OCR settings
pdf = 'path/to/your_pdf_file.pdf'
dpi = 300
file_output = 'output_filename'
return_text = True
config_tesseract = ''
limit_pages = None
lang = 'eng'
timeout = 120

# Perform OCR on the PDF
result = ocr_tesseract(
    pdf=pdf,
    dpi=dpi,
    file_output=file_output,
    return_text=return_text,
    config_tesseract=config_tesseract,
    limit_pages=limit_pages,
    lang=lang,
    timeout=timeout
)

# Output the result
print(result)
```

#### Example Usage of `ocr_google_vision` Function

Below is an example of how to use the `ocr_google_vision` function to perform OCR on a PDF file using Google Vision API with customizable settings.

```python
from funcspy.pdf_funcs.ocr_funcs import ocr_google_vision

# OCR settings
pdf = 'path/to/your_pdf_file.pdf'
api_key = 'your_google_api_key'
dpi = 300
file_output = 'output_filename'
return_text = True
limit_pages = None
is_image = False

# Perform OCR on the PDF
result = ocr_google_vision(
    pdf=pdf,
    api_key=api_key,
    dpi=dpi,
    file_output=file_output,
    return_text=return_text,
    limit_pages=limit_pages,
    is_image=is_image
)

# Output the result
print(result)
```

#### Example Usage of `make_ocr_in_pdf_offline` Function

Below is an example of how to use the `make_ocr_in_pdf_offline` function to extract text from a PDF file offline. This function only works with PDFs where the text is selectable.

```python
from funcspy.pdf_funcs.ocr_funcs import make_ocr_in_pdf_offline

# OCR settings
path_pdf = 'path/to/your_pdf_file.pdf'
export_from_file_txt = 'output_text_file.txt'  # Set to False if you do not want to export to a file

# Perform OCR on the PDF
result = make_ocr_in_pdf_offline(path_pdf, export_from_file_txt)

# Output the result
print(result)
```

#### Example Usage of `extract_pages` Function

Below is an example of how to use the `extract_pages` function to extract a specified number of pages from a PDF file and create a new PDF file.

```python
from funcspy.pdf_funcs.pdfutils.pdfutils import extract_pages

# PDF settings
original_pdf_path = 'path/to/original_pdf_file.pdf'
new_pdf_path = 'path/to/new_pdf_file.pdf'
num_pages = 10  # Number of pages to extract

# Extract pages from the original PDF
extract_pages(original_pdf_path, new_pdf_path, num_pages)
```

#### Example Usage of `split_pdf` Function

Below is an example of how to use the `split_pdf` function to split a PDF file into multiple files based on a specified page interval.

```python
from funcspy.pdf_funcs.pdfutils.pdfutils import split_pdf

# PDF settings
input_path = 'path/to/input_pdf_file.pdf'
output_dir = 'output_split'
interval = 30  # Number of pages in each split PDF

# Split the PDF
split_pdf(input_path, output_dir, interval)
```

#### Example Usage of `text_to_pdf` Function

Below is an example of how to use the `text_to_pdf` function to convert text into a PDF file with specified margins, font, and font size.

```python
from funcspy.pdf_funcs.pdfutils.pdfutils import text_to_pdf

# PDF settings
text = """This is a sample text to be converted into a PDF file.
You can customize the left and bottom margins, font, and font size."""
filename = 'output_text_pdf.pdf'
left_margin = 70
bottom_margin = 40
font = 'Helvetica'
font_size = 12

# Convert text to PDF
text_to_pdf(text, filename, left_margin, bottom_margin, font, font_size)
```

### Utils for any moments

#### Example Usage of `remove_accents` Function

Below is an example of how to use the `remove_accents` function to remove accents from a given text string.

```python
from funcspy.python_funcs.python_funcs import remove_accents

# Text settings
text = "Olá, como você está?"

# Remove accents from text
result = remove_accents(text)
print(result)
```

#### Example Usage of `random_sleep` Function

Below is an example of how to use the `random_sleep` function to pause execution for a random amount of time between specified minimum and maximum values.

```python
from funcspy.python_funcs.python_funcs import random_sleep

# Sleep settings
min_time = 1  # Minimum sleep time in seconds
max_time = 5  # Maximum sleep time in seconds

# Execute random sleep
random_sleep(min_time, max_time)
```

#### Example Usage of `create_dir_in_current_work_dir` Function

Below is an example of how to use the `create_dir_in_current_work_dir` function to create a directory in the current working directory.

```python
from funcspy.python_funcs.python_funcs import create_dir_in_current_work_dir

# Directory settings
dir_name = 'new_directory'
print_value = True
create_directory = True

# Create directory in the current working directory
result = create_dir_in_current_work_dir(dir_name, print_value, create_directory)
print(result)
```

#### Example Usage of `files_with_absolute_file_path` Function

Below is an example of how to use the `files_with_absolute_file_path` function to get a tuple of absolute file paths from a specified directory.

```python
from funcspy.python_funcs.python_funcs import files_with_absolute_file_path

# Directory path
path_dir = 'your_directory'

# Get absolute file paths
result = files_with_absolute_file_path(path_dir)
print(result)
```

#### Example Usage of `download_file_via_link` Function

Below is an example of how to use the `download_file_via_link` function to download a file from a specified link.

```python
from funcspy.python_funcs.python_funcs import download_file_via_link

# Download settings
link = 'https://filesamples.com/samples/document/xlsx/sample3.xlsx'
file_path = 'myplan.xlsx'
directory = 'downloads'  # Set to False if no directory is needed

# Download the file
download_file_via_link(link, file_path, directory)
```

#### Example Usage of `take_only_numbers` Function

Below is an example of how to use the `take_only_numbers` function to extract only the numeric characters from a given string.

```python
from funcspy.python_funcs.python_funcs import take_only_numbers

# String with numbers and other characters
string = "2122 asfs 245"

# Extract only numbers
result = take_only_numbers(string)
print(result)
```

#### Example Usage of `read_json` Function

Below is an example of how to use the `read_json` function to read a JSON file and return its contents as a dictionary.

```python
from funcspy.python_funcs.python_funcs import read_json

# JSON file path
file_json = 'path/to/your_file.json'

# Read JSON file
result = read_json(file_json)
print(result)
```

#### Example Usage of `zip_dirs` Function

Below is an example of how to use the `zip_dirs` function to zip multiple directories into a single zip file.

```python
from funcspy.python_funcs.python_funcs import zip_dirs

# Folders to be zipped
folders = ['folder1', 'folder_with_files2', 'folder3']
zip_filename = 'myzip.zip'

# Zip the directories
zip_dirs(folders, zip_filename)
```

#### Example Usage of `log` Function

Below is an example of how to use the `log` function to log messages with various levels, colors, and formats.

```python
from funcspy.python_funcs.python_funcs import log

# Basic log message with color
log('This is an informational message', color='green')

# Log message with color and format
log('This is a formatted message', color='red', format='b')

# Warning level log with custom styling
log('This is a warning message!', level='w', color='yellow on black b i')

# Critical level log
log('Critical error occurred!', level='c', color='red on yellow b i s blink')

# Error level log
log('An error has been encountered', level='e', color='purple')
```

#### Example Usage of `support_long_paths` Function

Below is an example of how to use the `support_long_paths` function to adjust a path for long filename support on Windows.

```python
from funcspy.python_funcs.python_funcs import support_long_paths

# Path settings
dos_path = 'your/very/long/path/to/a/directory/or/file'
encoding = None  # Set to specific encoding if needed

# Get long path support
result = support_long_paths(dos_path, encoding)
print(result)
```

#### Example Usage of `humanize_time` Function

Below is an example of how to use the `humanize_time` function to get a human-readable string representing the time elapsed from a given datetime or timestamp.

```python
from funcspy.python_funcs.python_funcs import humanize_time
from datetime import datetime, timedelta

# Time settings
time = datetime.now() - timedelta(days=1, hours=5)  # Example: 1 day and 5 hours ago

# Get human-readable time
result = humanize_time(time)
print(result)
```

#### Example Usage of `clean_directory` Function

Below is an example of how to use the `clean_directory` function to delete all contents of a specified directory, with options for handling files with long names and retrying on permission errors.

```python
from funcspy.python_funcs.python_funcs import clean_directory
import os

# Define the directory to clean
directory_to_clean = os.path.join(os.getcwd(), "example_directory")

# Clean the directory with default settings
clean_directory(directory_to_clean)

# Clean the directory with custom settings
clean_directory(directory_to_clean, timeout_for_clear=10, max_attempts=5, support_long_names=True)
```

## References

* [Rich Formatting for Colors](https://chatgpt.com/c/671e9e2b-8e9c-8008-83aa-61459c33d0ef#:~:text=Rich%20Formatting%20for%20Colors)
* [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
* [Google Vision API](https://cloud.google.com/vision/docs)

# License

MIT License

# Contact

Questions, thanks and even financial help? Just call me on

* Linkedin:
  * [in/gabriel-lopes2002](https://www.linkedin.com/in/gabriel-lopes2002/)
