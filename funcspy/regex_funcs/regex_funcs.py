"""	
Here you will find some functions using Regex

If necessary, collaborate =)
"""

########### imports ##############
import re
from funcspy.python_funcs.python_funcs import *
########### imports ##############

def extract_dates(text: str, pattern: str) -> list:
    """
    ### Returns dates in the chosen format


    Args:
        text (str): Text containing dates
        pattern (str): Regex pattern -> \d{2}.\d{2}.\d{4}|\d{2} for example


    Returns:
        list: Date(s)
    """
    dates = re.findall(pattern, text.lower())
    return dates if dates else []


def extract_cpfs(text: str) -> list:
    """
    ### Retrieves CPFs


    Args:
        text (str): Text containing CPF(s)


    Returns:
        list: CPF(s)
    """
    cpfs = re.findall("\d{3}.\d{3}.\d{3}-\d{2}", text)
    if not cpfs:
        cpfs = re.findall("\d{3}.\d{3}.\d{3} -\d{2}", text)
        if cpfs:
            cpfs = [''.join(i for i in cpf if i.isdigit() or i in ['.', '-']) for cpf in cpfs]
    return cpfs if cpfs else []


def extract_number_without_characters(string):
    """
    ### Extracts a number from a string without any characters.


    Args:
        string (str): The input string.


    Returns:
        str: The extracted number.
    """
    nums_list = re.findall('\d', string)
    num = ''.join(nums_list)
    return num


def extract_email(text: str) -> list:
    """
    ### Returns the extracted emails
    Validation/Search for emails with the RFC2822 pattern
    https://regexr.com/2rhq7


    Args:
        text (str): Text containing the email(s)


    Returns:
        list: email(s)
    """
    email = re.findall(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", text, re.IGNORECASE)
    return email if email else []


def extract_cnpjs(text: str, get_one=False, drop_duplicates=False) -> tuple|str:
    """
    ### Extracts CNPJ(s) from the string


    Args:
        text (str): Text that may contain CNPJ(s)
        get_one (bool): Return only the first CNPJ (default: False)
        drop_duplicates (bool): Remove duplicate CNPJs (default: False)


    Returns:
        tuple|str: CNPJ(s)
    """
    cnpjs = tuple(re.findall("\d{2}.\d{3}.\d{3}\/\d{4}-\d{2}", text))
    if drop_duplicates:
        cnpjs = tuple(set(cnpjs))
    if get_one and cnpjs:
        return cnpjs[0]
    return cnpjs


def extract_dates(text: str, get_one=False, drop_duplicates=False) -> tuple|str:
    """
    ### Returns dates in the format \d{2}/\d{2}/\d{4} -> 00/00/0000


    Args:
        text (str): Text that contains dates
        get_one (bool): Return only the first date (default: False)
        drop_duplicates (bool): Remove duplicate dates (default: False)


    Returns:
        tuple|str: date(s)
    """
    dates = tuple(re.findall("\d{2}/\d{2}/\d{4}", text.lower()))
    if drop_duplicates:
        dates = tuple(set(dates))
    if get_one and dates:
        return dates[0]
    return dates



def format_cpf_cnpj(nums_cpf_cnpj: str) -> str:
    """Formats a CPF or CNPJ
    Example:
        cpf -> 00000000000 input
        cpf -> 000.000.000-00 output
        
        cnpj -> 00000000000100 input
        cnpj -> 00.000.000/0001-00 output


    Args:
        nums_cpf_cnpj (str): CNPJ or CPF


    Returns:
        str: Formatted CPF or CNPJ
    """
    nums_cpf_cnpj = take_only_numbers(nums_cpf_cnpj)
    if len(nums_cpf_cnpj) == 11:
        return f'{nums_cpf_cnpj[:3]}.{nums_cpf_cnpj[3:6]}.{nums_cpf_cnpj[6:9]}-{nums_cpf_cnpj[9:]}'
    elif len(nums_cpf_cnpj) == 14:
        return f'{nums_cpf_cnpj[:2]}.{nums_cpf_cnpj[2:5]}.{nums_cpf_cnpj[5:8]}/{nums_cpf_cnpj[8:12]}-{nums_cpf_cnpj[12:]}'
    else:
        raise ValueError('len nums_cpf_cnpj != 11 or 14')