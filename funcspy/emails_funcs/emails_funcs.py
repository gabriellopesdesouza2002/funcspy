import platform
my_os = platform.system()

from funcspy.regex_funcs.regex_funcs import extract_email
from funcspy.python_funcs.python_funcs import transform_list_into_string
from pretty_html_table import build_table
from email import encoders
from email.mime.base import MIMEBase
import os
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from funcspy.python_funcs.python_funcs import *
from funcspy.regex_funcs.regex_funcs import extract_email
import smtplib
import win32com.client as win32

def send_email_outlook(to: list|str, subject: str='E-mail subject', body: str='<p>Olá!</p>', attachments :list|tuple|str|bool=False, send_dateframe_on_body: list|tuple|bool=False) -> None:
    """Function that sends e-mails via outlook (natively from the system)
    ## It is very important to have an Outlook account
    ### It is possible to send 
    
    Args:
        to (list | str) -> list or string of recipient(s)
        
        subject (str) -> E-mail subject. Default is E-mail subject
        
        body (str) -> Email body (HTML preferable) Default is <p>Hello!</p>
        
        attachments (list | tuple | str | bool=False) -> List, tuple, or string containing the path of the file that will be added to the e-mail (if you send True without sending anything, an error will occur!)
        
        send_dateframe_on_body (list | tuple | bool) -> If this variable is a list or tuple, it will be unpacked in pretty_html_table's build_table() function. You can then send any parameter in the order of the function (if you send True without sending anything, you'll get an error!)
        https://pypi.org/project/pretty-html-table/
        
        
    Returns:
        None
    """
    #--- Converte para string para verificação ---#
    emails = transform_list_into_string(to)
    emails = extract_email(emails)
    
    if send_dateframe_on_body:
        # (df, 'theme_on_pretty_html_table')
        if isinstance(send_dateframe_on_body, list) or isinstance(send_dateframe_on_body, tuple):
            html_table = build_table(*send_dateframe_on_body)
            body = f"""{body}
            {html_table}"""

    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    if isinstance(to, str):
        mail.To = to
    if isinstance(to, list) or  isinstance(to, tuple):
        mail.To = ";".join(emails)
    mail.Subject = subject
    
    if attachments:
        if isinstance(attachments, str):
            mail.Attachments.Add(attachments)
        if isinstance(attachments, list) or isinstance(attachments, tuple):
            for att in attachments:
                mail.Attachments.Add(att)

    mail.HTMLBody = (body)
    try:
        mail.Send()
    except Exception as e:
        exception = str(e)
        if 'Check that you have entered at least one name' in exception:
            print('We need to know who to send this to. Make sure you enter at least one name.')
            return
        
    print('Email sent successfully!')

def send_email_gmail(
    email_app_google: str,
    passwd_app_gmail: str,
    emails_to: str|tuple|list,
    subject: str,
    body_msg,
    attachments: tuple|list|bool = False,
    ):
    """Function to send a complete email in Google Gmail

    ### First, check if the email you will be sending is configured.

    If not, follow the step-by-step instructions below to configure the email.
    ### Step-by-step instructions to enable sending emails in Gmail
    1- Enable two-step verification in Gmail: https://myaccount.google.com/signinoptions/two-step-verification

    2- Go to this link to create an app password: https://myaccount.google.com/apppasswords
    2a - Select App, Email
    2b - Select device, Other (custom name)
    2c - Capture the password to add to the function.

    ### Tip for using a body:
    Use template:
    file: template.html:
    <!DOCTYPE html>
    <html>
    <body>
    <p>Hello <strong>$name_placeholder</strong>, today is <strong>$data_placeholder</strong>.</p>
    </body>
    </html>
    >>> from string import Template
    >>> with open('template.html', 'r', encoding='utf-8') as html:
    >>> template = Template(html.read())
    >>> nome = 'Nome'
    >>> date_atual = datetime.now().strftime('%d/%m/%Y')
    >>> body_msg = template.substitute(nome_placeholder=nome, data_placeholder=date_atual)

    Args:
    email_app_google (str): Email to send to recipients, (emails_to)
    passwd_app_gmail (str): Email passwd to send to recipients, (emails_to)
    emails_to (str|tuple|list): Recipient(s)
    subject (str): Email subject
    body_msg (str): Body of the E-mail attachments (tuple | list | bool): Attachments, optional, default = False 
    """

    msg = MIMEMultipart()

    # para quem está indo a msg
    if isinstance(emails_to, str):
        emails_to = extract_email(emails_to)
        if len(emails_to) == 0:
            print(f'Could not understand the email sent: {emails_to}')
            return
    emails_to = ';'.join(emails_to)
    msg['to'] = emails_to

    # subject
    msg['subject'] = subject

    # body
    body = MIMEText(body_msg, 'html')
    msg.attach(body)

    # insert attachments
    if isinstance(attachments, (tuple, list)):
        for att in attachments:
            attachment_abspath = os.path.abspath(att)
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(attachment_abspath, "rb").read())
            encoders.encode_base64(part)
            file_name = attachment_abspath.split("\\")[-1]
            print(f'Retrieving attachment: {file_name}')
            part.add_header(f'Content-Disposition', f'attachment; filename={file_name}')
            msg.attach(part)
    elif isinstance(attachments, str):
        attachment_abspath = os.path.abspath(attachments)
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(attachment_abspath, "rb").read())
        encoders.encode_base64(part)
        file_name = attachment_abspath.split("\\")[-1]
        print(f'Retrieving attachment: {file_name}')
        part.add_header('Content-Disposition', f'attachment; filename={file_name}')
        msg.attach(part)

    # open connection with smtp
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        try:
            smtp.login(email_app_google, passwd_app_gmail)
        except smtplib.SMTPAuthenticationError as e:
            print(f'Email not sent:\n\tInvalid username or password!\n\n{e.smtp_error}')
            return
        smtp.send_message(msg)
        print('Email sent successfully!')