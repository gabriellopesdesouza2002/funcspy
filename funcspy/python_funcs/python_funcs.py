"""
## Various functions to help you develop any application in Python

### In this module you will find everything from simple functions to complex functions that would take a long time to develop.
"""

################################## IMPORTS #############################################
import os, sys, shutil, platform, re, logging,\
    unicodedata, gc, requests, time, json,\
    threading, base64, random, uuid, locale
from configparser import RawConfigParser
from datetime import datetime, date, timedelta
from fnmatch import fnmatch
from time import sleep
import subprocess as sp
import zipfile
from rich import print
from rich.console import Console
from numpy import unicode_
import holidays
################################## IMPORTS #############################################

def generate_uuid() -> str:
    """Generate uuid

    Returns:
        str: uuid
    """
    return str(uuid.uuid4())

def file_to_base64(file) -> str:
    """Convert any file to base64

    Args:
        file (str): File to convert (path)

    Returns:
        str: file represented in base64
    """
    with open(os.path.abspath(file), "rb") as file:
        base64_ = base64.b64encode(file.read())
        return base64_.decode("utf-8")

def base64_to_file(base64_string:str, output_file:str) -> None:
    """Convert any base64 to file

    Args:
        base64_string (str): base64 represented in string
        base64_string (str): File to convert (path)

    Returns:
        None: None
    """
    with open(output_file, "wb") as f:
        image_data = base64.b64decode(base64_string)
        f.write(image_data)

def random_sleep(min, max) -> None:
    """Run a random sleep when searching for requests to avoid IP blocks

    Args:
        min (int|float): Min value to sleep
        max (int|float): Max value to sleep
    """
    sleep(random.uniform(min, max))

def remove_accents(text:str, encoding:str='utf-8') -> str:
	try:
		text = unicode_(text, encoding=encoding)
	except Exception:
		pass
	text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
	return str(text)

def getsizefile(path_file:str, return_convet_bytes: bool=False) -> int|str:
    """
    getsizefile in bytes, KB, MB, GB, TB, PB
    
    Args:
        path_file (str): Relative path of the file
        return_convet_bytes (str): convert the value of bits -> B = Byte K = Kilo M = Mega G = Giga T = Tera P = Peta
    
    Returns:
        int|str: Value of the function os.path.getsize()
    """
    FILE_PATH_ABSOLUTE = os.path.getsize(os.path.abspath(path_file))
    if return_convet_bytes:
        return convert_bytes(FILE_PATH_ABSOLUTE)
    return FILE_PATH_ABSOLUTE

def execute_garbage_collector(generation :int=False) -> int:
    """
    Run the garbage collector.

    With no arguments, run a full collection. The optional argument may be an integer specifying which generation to collect. A ValueError is raised if the generation number is invalid.

    The number of unreachable objects is returned.
    """
    if generation:
        return gc.collect(generation)
    else:
        return gc.collect()


def check_if_you_are_connected_to_vpn(ping_host :str) -> None:
    """Checking by pinging if you are connected to the VPN IP"""
    PING_HOST = ping_host
    
    output = sp.getoutput(f'ping {PING_HOST} -n 1')  # -n 1 limita a saída
    if ("Time's up" in output) or ('time out' in output):
        log('VPN NOT CONNECTED!', 'w')
    else:
        log("VPN connected successfully!", color='green')


def transform_list_into_string(lista :list) -> str:
    try:
        return ', '.join(lista)
    except TypeError:
        lista = [str(i) for i in lista]
        return ', '.join(lista)


def remove_file_extension(file :str, extension :str) -> str:
    """Removes the extension from a file name.

    Args:
    file (str): file with the extension in its name -> file.xlsx
    extension (str): extension you want to remove

    Returns:
        str: File name without the extension.
    """
    replacement =  file.replace(f'.{extension}', '')
    replacement =  replacement.replace(f'{extension}', '')
    return replacement


def reverse_iter(iterable :str | tuple | list) -> str | tuple | list:
    """Returns any iterable in reverse

    Use:
        Before use: '1234567890'
        Before use: (1,2,3,4,5,6,7,8,9,0)
        Before use: [1,2,3,4,5,6,7,8,9,0]

        After use: '0987654321'
        After use: (0,9,8,7,6,5,4,3,2,1)
        After use: [0,9,8,7,6,5,4,3,2,1]

    * By https://www.geeksforgeeks.org/python-reversing-tuple/#:~:text=Since%20tuples%20are%20immutable%2C%20there,all%20of%20the%20existing%20elements.

    Args:
        iterable (str | tuple | list): Any iterable to have its value reversed

    Returns:
            str | tuple | list: iterable with its values ​​reversed
    """
    return iterable[::-1]


def get_current_path() -> str: 
    """Returns the absolute path of the current execution directory of the Python script
    
    Returns: 
        str: returns the absolute path of the current Python script execution
        
    # The script is running in the mybestscript directory
    # Ultimately it executes os.getcwd()
    Use:
        >>> get_current_path()
        >>> C:/Users/myuser/Documents/myprojects/python/mybestscript/
    """ 
    return os.getcwd() 



def create_dir_in_current_work_dir(dir: str, print_value: bool=False, create_directory: bool=True) -> str:
    """Creates directory in the current working directory

    1 - Gets the current path of script execution

    2 - Concatenates "dir" with the current path of script execution

    3 - Creates the new directory in the current path (optional)

    Args: dir (str): Directory that can be created print_value (bool, optional): Prints the output of the path with the created directory on the screen. Defaults to False.
    create_directory (bool, optional): Creates the directory sent in the path where the script is being used. Defaults to False.

    Returns:
    str: Returns the path of the dir with the absolute path
    """
    current_path = get_current_path()
    path_new_dir = os.path.join(current_path, dir) 
    if print_value: 
        log(path_new_dir) 
        if create_directory: 
            os.makedirs(path_new_dir, exist_ok=True)
            return (path_new_dir)
    else: 
        if create_directory: 
            os.makedirs(path_new_dir, exist_ok=True) 
        return (path_new_dir)

def delete_directory(path_dir: str, use_rmtree: bool=True) -> None:
    """Removes a directory with or without files inside

    Args:
    path_dir (str): relative path of the directory
    use_rmtree (bool, optional): Deletes files and other directories inside the uploaded directory. Defaults to True.
    """
    DIRECTORY = os.path.abspath(path_dir)
    if os.path.exists(DIRECTORY):
        if use_rmtree:
            shutil.rmtree(DIRECTORY)
            sleep(3)
        else:
            os.rmdir(DIRECTORY)
    else:
        ...


def files_with_absolute_file_path(path_dir: str) -> tuple[str]:
    """Returns a tuple with several paths of files and directories

    ### The script will take this relative path, take its absolute path and concatenate it with the file(s) and/or directory(ies) found

    Args:
    path_dir (str): relative path of the directory

    Returns:
    tuple[str]: Returns a tuple with the files and/or directories
    """    
    return tuple(os.path.join(os.path.abspath(path_dir), file) for file in os.listdir(path_dir))


def config_ini_read(path_config: str) -> dict:
    """ 
    # DEPRECATED
    Reads the config.ini file and returns it as a dictionary.

    Returns:
        dict: return all the configs in the config.ini file
    """
    
    configs = RawConfigParser()
    configs.read(path_config)
    config = {s: dict(configs.items(str(s))) for s in configs.sections()}
    return config


def terminal(command:str) -> None:
    """Execute a terminal command

    Args:
        command (str): command to be executed
    """
    os.system(command)


def current_date_and_time_as_string(format: str='%d/%m/%y %Hh %Mm %Ss') -> str:
    """Returns date or time or both as a string

    Args:
    format (str, optional): Time and date format (or just time or just date if you prefer). Defaults to '%d/%m/%y %Hh %Mm %Ss'.

    Returns:
    str: current time/date as a string
    """

    return datetime.now().strftime(format)


def add_date_to_file_path(file_path: str, format: str='%d/%m/%y-%Hh-%Mm-%Ss') -> str:
    """Adds date to the beginning of the file.

    Args:
    date (datetime.datetime): Datetime object
    file_path (str): File path

    Returns:
    str: Returns the file with
    """
    
    if isinstance(format, str):
        sufix = 0
        file_name = os.path.basename(file_path)
        file_path = os.path.dirname(file_path)
        file_name, file_extension = os.path.splitext(file_name)
        file_name = current_date_and_time_as_string(format) + ' ' + file_name
        resultado_path = os.path.join(
            file_path, file_name + file_extension)
        while os.path.exists(resultado_path):  # caso o file exista, haverá sufix
            sufix += 1
            resultado_path = os.path.join(
                file_path, file_name + str(sufix) + file_extension)
        return resultado_path
    else:
        raise TypeError('Send a string in the format_date parameter')


def download_file_via_link(link: str, file_path: str, directory :bool|str=False):
    """Downloads files via a link that must include the file extension.

    ### The file must include its extension in the link; usage example below:

    Use:
    download_file(link='https://filesamples.com/samples/document/xlsx/sample3.xlsx', file_path='myplan.xlsx', directory='donwloads/')

    Args:
    link (str): link to the file that will be downloaded (must include the extension)
    file_path (str): destination of the file that will be downloaded (must include the extension)
    directory (str | bool): destination directory (will be created if it does not exist). If not sent, the file will remain in the current download directory. Optional, Default is False
    """
    if directory:
        create_dir_in_current_work_dir(directory)
        file_path = os.path.join(os.path.abspath(directory), file_path)
        
    r = requests.get(link, allow_redirects=True)
    try:
        with open(file_path, 'wb') as file:
            file.write(r.content)
            print(f'Full download! -> {os.path.abspath(file_path)}')
    except Exception as e:
        print(f'Error:\n{str(e)}')
    finally:
        del r
        gc.collect()


def current_time(seconds: bool=False) -> str:
    """Function returns the current time in hh:mm or hh:mm:ss format with seconds enabled"""
    from datetime import datetime
    e = datetime.now()
    if seconds:
        return f'{e.hour}:{e.minute}:{e.second}'
    else:
        return f'{e.hour}:{e.minute}'


def times() -> str:
    """Function returns the time of day, for example, Good morning, Good afternoon and Good evening

    Returns:
    str: Time of day, for example, Good morning, Good afternoon and Good evening
    """
    current_time = datetime.now()
    if (current_time.hour < 12):
        return 'Good morning!'
    elif (12 <= current_time.hour < 18):
        return 'Good afternoon!'
    else:
        return 'Goodnight!'

def check_if_path_exists(path_file_or_dir: str) -> bool:
    if os.path.exists(path_file_or_dir):
        return True
    else:
        return False

def leave_files_hidden_or_not(path_file_or_dir : str, hidden : bool) -> None:
    """Leaves files or directories hidden or not.

    Use:
    >>> leave_files_hidden_or_not(r'dir\file.txt', False)
    file.txt -> visible
    >>> leave_files_hidden_or_not(r'dir\file.txt', True)
    file.txt -> not visible

    Args:
    path_file_or_dir (str): File or directory you want to hide or leave visible
    hidden (str): Leaves the file or directory hidden
    """

    import ctypes
    from stat import FILE_ATTRIBUTE_ARCHIVE
    FILE_ATTRIBUTE_HIDDEN = 0x02

    if hidden:
        ctypes.windll.kernel32.SetFileAttributesW(path_file_or_dir, FILE_ATTRIBUTE_HIDDEN)
        print(f'O file / diretório {path_file_or_dir} ESTÁ hidden!')
    else:
        ctypes.windll.kernel32.SetFileAttributesW(path_file_or_dir, FILE_ATTRIBUTE_ARCHIVE)
        print(f'O file / diretório {path_file_or_dir} NÃO ESTÁ MAIS hidden!')
        
    # HIDDEN = hidden
    # ARCHIVE = not hidden


def make_requirements_txt() -> None:
    """"""
    os.system("pip freeze > requirements.txt")


def clean_terminal_and_cmd() -> None:
    """This function clears the Terminal / CMD in Linux and Windows"""
    os.system('cls' if os.name == 'nt' else 'clear')



def create_virtual_environment(nome_da_venv: str) -> None:
    nome_da_venv = nome_da_venv.strip()
    nome_da_venv = nome_da_venv.replace('.', '')
    nome_da_venv = nome_da_venv.replace('/', '')
    nome_da_venv = nome_da_venv.replace(',', '')
    os.system(f'python -m venv {nome_da_venv}')
    print(f'Ambiente Virtual com o nome {nome_da_venv} foi criado com sucesso!')
    sleep(2)


def restart_program() -> None:
    os.execl(sys.executable, sys.executable, *sys.argv)


def move_files(path_origin: str, path_destination: str, extension: str) -> None:
    """Move files from one folder to another

    Args:
        path_origin (str): Path to the folder where the files will be moved
        path_destination (str): Path to the folder where the files will be moved
        extension (str): Extension of the files that will be moved
    """

    source_folder_files = os.listdir(path_origin)
    files = [path_origin + "\\" + f for f in source_folder_files if extension in f]
    
    for file in files:
        try:
            shutil.move(file, path_destination)
        except shutil.Error:
            shutil.move(file, path_destination)
            os.remove(file)


def take_only_numbers(string :str) -> str | int:
    """Get only numbers from a string

    Args:
        string (str): string with numbers

    Returns:
        str | int: string with only numbers
    """
    if isinstance(string, (str)):
        r = re.compile(r'\D')
        return r.sub('', string)
    else:
        log('Please send a string like this -> "2122 asfs 245"')
        return ''


def remove_file(file_path : str) -> None:
    os.remove(os.path.abspath(file_path))


def verify_object_size(objeto : object) -> int:
    """Verify the size of an object

    Args:
        objeto (object): Object

    Returns:
        int: Size of the object
    """
    log(sys.getsizeof(objeto))


def read_json(file_json: str, enconding: str='utf-8') -> dict:
    """Reads and returns a dict from a json file

    Args:
        file_json (str): File Json
        enconding (str, optional): Encoding. Defaults to 'utf-8'.

    Returns:
        dict: Dict from the json file
    """
    return json.load(open(file_json, "r", encoding=enconding))


def convert_bytes(_size: int|float):
    """Converts bytes to
    >>> B = Byte

    >>> K = Kilo

    >>> M = Mega

    >>> G = Giga

    >>> T = Tera

    >>> P = Peta

    
    ### Use base 1024 instead of 1000

    Use:
        >>> file_size_in_bytes = os.path.getsize(C:\\MyFile.txt)
        >>> print(file_size_in_bytes)
        >>>> 3923 
        >>> print(convert_bytes(file_size_in_bytes))
        >>>> '3.83 K'

    Args:
        size (int|float): File size in bytes, os.path.getsize(file) can be used

    Returns:
        str: Value of the size in B; K; M; G; T; P -> 
    """
    base = 1024
    kilo = base # K
    mega = base ** 2 # M
    giga = base ** 3 # G
    tera = base ** 4 # T
    peta = base ** 5 # P
    
    # if the size is less than kilo (K) it is Byte
    # if the size is less than mega (M) it is Kb
    # if the size is less than giga (G) it is MB and so on
    
    if isinstance(size, (int, float)):
        pass
    else:
        print('Trying to convert the value of the parameter size...')
        try:
            size = float(size)
        except ValueError as e:
            if 'could not convert string to float' in str(e):
                print(f'Could not convert size++{size}++ to float!')
                return 'ValueError'
    if _size < kilo:
        _size = _size
        _text = 'B'
    elif _size < mega:
        _size /= kilo
        _text = 'K'
    elif _size < giga:
        _size /= mega
        _text = 'M'
    elif _size < tera:
        _size /= giga
        _text = 'G'
    elif _size < peta:
        _size /= tera
        _text = 'T'
    else:
        _size /= peta
        _text = 'P'
        
    _size = round(_size, 2)
    
    return f'{_size} {_text}'.replace('.', ',')


def time_now() -> float:
    """time() -> floating point number

    Returns:
        float: Return the current time in seconds since the Epoch. Fractions of a second may be present if the system clock provides them.
    """
    return time.time()


def last_day_of_current_month(format: str='%d/%m/%Y'):
    """Return the last day of the current month
    
    Args:
        format (str, optional): format of the date. Defaults to '%d/%m/%Y'.

    Use:
        >>> last_day_of_current_month(format='%d/%m/%Y')
        >>>> '31/10/2022'

    Returns:
        str: Return the last day of the current month with format
    """
    from calendar import mdays
    from datetime import datetime
    
    current_month = int(datetime.now().strftime('%m'))
    
    last_day = mdays[current_month]
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    format_ = datetime.strptime(f'{last_day}/{current_month}/{current_year}', '%d/%m/%Y')

    return format_.strftime(format)


def update_all_pip_packages():
    """Updates all pip packages in the current environment (MAY TAKE A LONG TIME)

    If it doesn't work, run this in the terminal: `pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}`
    """
    os.system("""pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}""")


def returns_elapsed_time(init: float|int, end: float|int, format: bool=True):
    """Returns the expression (end - init) / 60

    Args:
        init (float | int): start time of the function, class or block
        end (float | int): end time of the function, class or block
        format (bool, optional): whether to format for example to 0.10 or not. Defaults to True.

    Use:
        >>> from time import time
        >>>
        >>> init = time()
        >>> ... your code ...
        >>> end = time()
        >>> result = returns_elapsed_time(init, end)
        >>> print(result) >>> 0.17

    Returns:
        float|int: Total execution time
    """
    result = (end - init) / 60
    if format:
        return f'{result:.2f}'
    else:
        return result
        

def save_json(old_json: dict, file_json: str, enconding: str="utf-8") -> None:
    """Saves the JSON file with the dict sent in the parameter.

    Args:
        old_json (dict): old dict with the changed data
        file_json (str): file that will be changed
        encoding (str, optional): encoding. Defaults to "utf-8".
    """
    with open(file_json, 'w', encoding=enconding) as f:
        json.dump(old_json, f)


def close_program():
    """Closes the program
    """
    try:
        sys.exit()
    except Exception:
        try:
            quit()
        except NameError:
            pass


def return_home_user() -> str:
    """Expand ~ and ~user constructions. If user or $HOME is unknown, do nothing.
    
    Use:
        >>> home = return_home_user()
        >>> print(home) >>> C:\\Users\\myuser
    
    Returns:
        str: $HOME -> C:\\Users\\myuser
    """
    return os.path.expanduser("~")

    
def close_in_x_seconds(qty_of_seconds_to_close:int) -> None:
    """Espera os seconds enviados para fechar o programa

    Args:
        qty_of_seconds_to_close (int): seconds para fazer regresivamente para fechar o programa
    """
    log(f'Exiting robot in: {qty_of_seconds_to_close} seconds...')
    for i in range(qty_of_seconds_to_close):
        log(str(qty_of_seconds_to_close))
        qty_of_seconds_to_close -= 1
        sleep(1)
    close_program()
    
    
def zip_dirs(folders:list|tuple, zip_filename:str) -> None:
    """Zips multiple directories recursively.

    Args:
        folders (list|tuple): folders
        zip_filename (str): name_file_zip with ``name of file.zip``

    Usage:
        >>> folders = ['folder1', 'folder_with_files2', 'folder3',]
        >>> zip_dirs(folders, 'myzip.zip')
    """
    zip_file = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)

    for folder in folders:
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                zip_file.write(
                    os.path.join(dirpath, filename),
                    os.path.relpath(os.path.join(dirpath, filename), os.path.join(folders[0], '../..')))
    zip_file.close()


# LOG
console = Console()

# Configura o logger globalmente
path_logs_dir = os.path.abspath('logs')
path_logs_file = os.path.join(path_logs_dir, 'logs.log')

if not os.path.exists(path_logs_dir):
    os.mkdir(path_logs_dir)

logging.basicConfig(filename=path_logs_file,
                    encoding='utf-8',
                    filemode='a',  # append mode
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger()

def clear_logs(logs_dir='logs', logs_file='logs.log'):
    """
    Clears the log file if it exists.

    Args:
        logs_dir (str): Directory where the log file is located. Default is 'logs'.
        logs_file (str): Name of the log file to clear. Default is 'logs.log'.

    Usage:
        >>> # Call the function at bot startup to clear the log file
        >>> clear_logs()
        >>> # Specify a different directory and log file
        >>> clear_logs(logs_dir='/path/to/logs', logs_file='my_log.log')
    """
    path_logs_dir = os.path.abspath(logs_dir)
    path_logs_file = os.path.join(path_logs_dir, logs_file)
    
    if os.path.exists(path_logs_file):
        with open(path_logs_file, 'w'):
            pass
        print(f"Log file {path_logs_file} was cleared.")
    else:
        print(f"Log file {path_logs_file} does not exist, no action required.")


def log(msg: str, level: str = 'i', color: None|str=None, format: None|str=None) -> None:
    """Logs to default folder (./logs/botLog.log)

    Args:
        msg (str): "Message of Log"
        level (str): "Log levels"
        color (None|str): Colors Rich; defaut is None
        format (None|str) Log format; defaut is None
    Levels:
        'i' or not passed = info and print
        'i*' = info log only
        'w' = warning
        'c*' = critical / Exception Error exc_info=True
        'c' = critical
        'e' = error

    Use:
    >>> log('@@@@@@@@@@@@@@@@@@@', color='red')
    >>> log('@@@@@@@@@@@@@@@@@@@', color='red', format='b')
    >>> log('@ THE SYSTEM IS DOWN! @', color='red on yellow b i s blink')
    >>> log('@@@@@@@@@@@@@@@@@@@', color='green')
    >>> log('@@@@@@@@@@@@@@@@@@@', color='green b i')

    Rich Formatting:
        Colors: https://rich.readthedocs.io/en/latest/appendix/colors.html
    """
    
    if isinstance(msg, str):
        pass
    
    if isinstance(msg, (object)):
        msg = str(msg)    
    
    if isinstance(level, (str)):
        pass
    else:
        print('PUT A STRING IN THE LEVEL PARAMETER!')

    if isinstance(msg, (str)) and isinstance(level, (str)):
        if level == 'i' or level == '' or level is None:
            logger.setLevel(logging.INFO)
            if isinstance(color, str) and isinstance(format, str):
                console.print(f'[{format}][{color}]{msg}[/{color}][/{format}]')
            elif isinstance(color, str):
                console.print(f'[{color}]{msg}[/{color}]')
            else:
                console.print(msg)
            if r'\n' in msg:
                msg = msg.replace(r"\n", "")
            logger.info(msg)

        elif level == 'i*':
            logger.setLevel(logging.INFO)
            if r'\n' in msg:
                msg = msg.replace(r"\n", "")
            logger.info(msg)

        elif level == 'w':
            logger.setLevel(logging.WARNING)
            logger.warning(msg)
            if isinstance(color, str) and isinstance(format, str):
                console.print(f'[{format}][{color}]{msg}[/{color}][/{format}]')
            elif isinstance(color, str):
                console.print(f'[{color}]{msg}[/{color}]')
            else:
                console.print(msg)

        elif level == 'e':
            logger.setLevel(logging.ERROR)
            logger.error(msg)
            if isinstance(color, str) and isinstance(format, str):
                console.print(f'[{format}][{color}]{msg}[/{color}][/{format}]')
            elif isinstance(color, str):
                console.print(f'[{color}]{msg}[/{color}]')
            else:
                console.print(msg)

        elif level == 'c':
            logger.setLevel(logging.CRITICAL)
            logger.critical(msg)
            if isinstance(color, str) and isinstance(format, str):
                console.print(f'[{format}][{color}]{msg}[/{color}][/{format}]')
            elif isinstance(color, str):
                console.print(f'[{color}]{msg}[/{color}]')
            else:
                console.print(msg)

        elif level == 'c*':
            logger.setLevel(logging.CRITICAL)
            logger.critical(msg, exc_info=True)
            if isinstance(color, str) and isinstance(format, str):
                console.print(f'[{format}][{color}]{msg}[/{color}][/{format}]')
            elif isinstance(color, str):
                console.print(f'[{color}]{msg}[/{color}]')
            else:
                console.print(msg)
# LOGS
    

def return_date_and_time_ahead(days_ahead: int, sep: str='/') -> str:
    """Returns the date and time one day ahead of the current date
    ex: 06/15/2002 18:31 -> days_ahead=3 -> 06/18/2002 18:31
    """
    hj = date.today()
    future = date.fromordinal(hj.toordinal() + days_ahead)
    future_day = future.strftime(f'%d{sep}%m{sep}%Y')
    future_hour = datetime.today().strftime('%H:%M')
    return f'{future_day} {future_hour}'


def add_to_start_of_string(string: str, add_in: str, print_exit: bool = False):
    """Adds a string to the beginning of another string


    Args:
        string (str): The string you want to add something to the front of
        add_in (str): The string that will be added to the front of the string
        print_exit (bool, optional): Prints the resulting value. Defaults to False.


    Returns:
        _type_: _description_
    """
    if print_exit:
        print(add_in + string[:])
    return add_in + string[:]


def retrieve_xlsx_files_from_folder(dir: str) -> list[str]:
    """Returns a list of files that contain .xlsx


    Args:
        dir (str): Relative path of the directory containing the .xlsx file(s)


    Returns:
        list[str]: List of all .xlsx files (with absolute path)
    """
    DIR_PATH = os.path.abspath(dir)
    FILES = os.listdir(DIR_PATH)
    FILES_XLSX = []
    for fil in FILES:
        if '.xlsx' in fil:
            FILES_XLSX.append(DIR_PATH + "\\" + fil)
    return FILES_XLSX
    
def retrieve_files_with_specific_extension_in_folder(dir: str, extension: str = '.xlsx') -> list[str]:
    """Returns a list of files with a specific extension


    Args:
        dir (str): Relative path of the directory containing the files
        extension (str, optional): File extension to filter by. Defaults to '.xlsx'


    Returns:
        list[str]: List of files with the specified extension (with absolute path)
    """
    DIR_PATH = os.path.abspath(dir)
    FILES = os.listdir(DIR_PATH)
    FILES_WITH_EXTENSION = []
    for fil in FILES:
        if extension in fil:
            FILES_WITH_EXTENSION.append(DIR_PATH + "\\" + fil)
    return FILES_WITH_EXTENSION


def create_last_directory_of_file(path: str, print_exit: bool = False):
    """Creates the last directory of a file
    Ex: meudir1\meudir2\meudir3\meufile.txt
        create meudir1\meudir2\meudir3
        https://stackoverflow.com/questions/3925096/how-to-get-only-the-last-part-of-a-path-in-python


    Args:
        path (str): Absolute or relative path of the directory
    """
    PATH_ABS = os.path.abspath(path=path)
    if print_exit:
        print(os.path.basename(os.path.normpath(PATH_ABS)))
    arquivo_para_remover = os.path.basename(os.path.normpath(PATH_ABS))
    PATH = path.replace(arquivo_para_remover, '')
    try:
        os.makedirs(PATH)
    except FileExistsError:
        print('Directory already created earlier...')


def get_date_ahead(days_ahead: int, sep: str = '/') -> str:
    """Returns the date with days ahead of the current date
    ex: 15/06/2002 -> days_ahead=3 -> 18/06/2002
    """
    today = date.today()
    future = date.fromordinal(today.toordinal() + days_ahead)  # today + days_ahead
    return future.strftime(f'%d{sep}%m{sep}%Y')



def search_for_files_and_return_info(dir: str, search_term: str, show: str = 'all_path_file'):
    """Returns a file and returns various data about the file
    #### Available options:
    >>> show='all_path_file' # shows the full path of the file
    >>> show='file_name' # shows the file name (without extension)
    >>> show='file_name_with_ext' # shows the file name (with extension)
    >>> show='ext_file' # shows the file extension (without the name)
    >>> show='size_bytes' # shows the file size in bytes (os.path.getsize())
    >>> show='size' # shows the file size converted to B; K; M; G; T; P


    Args:
        dir (str): Directory to search for files
        search_term (str): Term to search for in file names
        show (str, optional): Option to show specific file information. Defaults to 'all_path_file'.


    Returns:
        _type_: File information based on the selected option
    """
    found = 0
    for root, dirs, files in os.walk(dir):
        for file in files:
            if search_term in file:
                try:
                    full_file_path = os.path.join(root, file)  # joins the root with the file name
                    file_name, file_extension = os.path.splitext(file)
                    file_size_in_bytes = os.path.getsize(full_file_path)
                    found += 1
                    if show == 'all_path_file':
                        return full_file_path
                    elif show == 'file_name':
                        return file_name
                    elif show == 'file_name_with_ext':
                        return file
                    elif show == 'ext_file':
                        return file_extension
                    elif show == 'size_bytes':
                        return file_size_in_bytes
                    elif show == 'size':
                        return convert_bytes(file_size_in_bytes)
                except PermissionError as e:
                    print(f'No permission... {e}')
                except FileNotFoundError as e:
                    print(f'Not found... {e}')
                except Exception as e:
                    print(f'Unknown error... {e}')
    else:
        if found >= 1:
            ...
        else:
            print('No files found!')
            
            
def split_lines_text(text: str) -> list[str]:
    """Splits a string into lines separated by newline characters (\n)


    Example usage:
        >>> string = "this is \nstring example....\nwow!!!"
        >>> print(string.splitlines())
        >>>> ['this is ', 'string example....', 'wow!!!']


    Args:
        text (str): The input string with newline characters (\n)


    Returns:
        list[str]: A list of strings, each representing a line from the input string
    """
    return text.splitlines()


def execute_in_thread(function_to_execute, args: tuple | bool = False):
    """
    Executa uma função em uma thread separada.

    ### Teste a sua função antes de colocar aqui! =)

    Essa é um pequeno resumo do que a classe Thread faz

    Args:
        function_to_execute (CALLABLE): Função que será executada em uma thread
        args (tuple | False): Tupla com os argumentos, ou False se não tiver nenhum argumento

    Use:
        >>> def cria_diretorio(dir_name="diretório"):
        >>>     try:
        >>>         os.mkdir(dir_name)
        >>>         print('diretorio_criado')
        >>>     except FileExistsError:
        >>>         pass
        >>>
        >>> print('Não executou a Thread')
        >>> execute_in_thread(cria_diretorio, ('meu_diretório',))
        >>> print('Executou a Thread')

        >>>> Não executou a Thread
        >>>> diretorio_criado
        >>>> Executou a Thread
    """
    if args is False:
        thread = threading.Thread(target=function_to_execute)
    else:
        thread = threading.Thread(target=function_to_execute, args=args)
    thread.start()


def support_long_paths(dos_path: str, encoding: str = None) -> str:
    """
    Returns a path that supports up to 32,760 characters on Windows.

    Args:
        dos_path (str): The original path to be processed.
        encoding (str, optional): The encoding to be used if the path needs to be decoded.

    Returns:
        str: The adjusted path to support long filenames.

    Source:
    https://stackoverflow.com/questions/36219317/pathname-too-long-to-open
    """
    if not isinstance(dos_path, str) and encoding is not None:
        dos_path = dos_path.decode(encoding)

    path = os.path.abspath(dos_path)

    if path.startswith(u"\\\\"):
        return u"\\\\?\\UNC\\" + path[2:]
    return u"\\\\?\\" + path


def format_to_real(value: str | float, with_symbol: bool = False) -> str:
    """
    Converte um valor para real (BRL)

    É necessário enviar um valor que tenha , na última casa
    -> 13076,9 ou enviar um valor float

    Exemplos:
        Sem símbolo:
            >>> format_to_real(192213.12)
            >>>> 192.213,12

        Com símbolo:
            >>> format_to_real(192213.12, True)
            >>>> R$ 192.213,12

    Args:
        value (str | float): valor a ser convertido para real
        with_symbol (bool): inclui o símbolo do real na frente

    Returns:
        str: valor formatado como real
    """
    if not value:
        return ''

    if isinstance(value, float):
        pass
    else:
        try:
            value = float(str(value).replace(',', '.'))  # converte valor para float
        except ValueError:
            if with_symbol:
                return 'R$ ' + value
            return value

    value = f'{value:_.2f}'
    value = value.replace('.', ',').replace('_', '.')

    if with_symbol:
        return 'R$ ' + value
    return value


def get_min_or_max_date(dates: list[str | datetime], max_date: bool = True, input_format: str = '%d/%m/%Y %H:%M', output_format: str = '%d/%m/%Y %H:%M'):
    """
    ## Returns the MAX or MIN date from a list of dates

    ### If the list of dates is already in datetime format, no conversion will be performed


    ### It is necessary that all dates are in the format specified in the input_format parameter


    Args:
        dates (list[str | datetime]): List of dates
        max_date (bool, optional): If True, returns the maximum date (most recent). If False, returns the minimum date (oldest). Defaults to True.
        input_format (str, optional): Format of the dates to be converted. Defaults to '%d/%m/%Y %H:%M'.
        output_format (str, optional): Format of the returned date. Defaults to '%d/%m/%Y %H:%M'.


    Returns:
        str: The minimum or maximum date in the specified format
    """
    dates_datetime = []

    for date in dates:
        if isinstance(date, datetime):
            dates_datetime.append(date)
        else:
            dates_datetime.append(datetime.strptime(date, input_format))

    if max_date:
        return max(dates_datetime).strftime(output_format)
    else:
        return min(dates_datetime).strftime(output_format)



def date_with_days_more_or_less(date: datetime, days: int = 0, less: bool = True, format_exit: str = '%d/%m/%Y') -> str | datetime:
    """Function returns the date with days more or less depending on the choice


    Args:
        date (datetime): Date in datetime class format
        days (int, optional): Days ahead or days behind. Defaults to 0.
        less (bool, optional): If you want to see days behind, leave as True, if you want to see days ahead, leave as False. Defaults to True.
        format_exit (str, optional): Date format, if you send None or '' or False, it will return a Datetime object. Defaults to '%d/%m/%Y'.


    Returns:
        str | datetime: Date


    Use:
        >>> # Let's say the current date is: 07/12/2022 it will return 05/12/2022 -> With format enabled
        >>> In [1]: date_with_days_more_or_less(datetime.now(), 2)
        >>> In [2]: type(date_with_days_more_or_less(datetime.now(), 2))
        >>> Out [1]: 05/12/2022
        >>> Out [2]: <class 'str'>




        >>> # Let's say the current date is: 07/12/2022 it will return 05/12/2022 -> With format not defined
        >>> In [1]: date_with_days_more_or_less(datetime.now(), 2, format_exit=None)
        >>> In [2]: type(date_with_days_more_or_less(datetime.now(), 2, format_exit=None))
        >>> Out [1]: 2022-12-05 11:01:37.476540
        >>> Out [2]: <class 'datetime.datetime'>
    """
    if less:
        date = date - timedelta(days=days)
        if (format_exit == '') or (format_exit is None) or (isinstance(format_exit, bool)):
            return date
        date_ = date.strftime(format_exit)
        return date_
    else:
        date = date + timedelta(days=days)
        if (format_exit == '') or (format_exit is None) or (isinstance(format_exit, bool)):
            return date
        date_ = date.strftime(format_exit)
        return date_


def remove_special_chars(input_string):
    """Removes special characters from the input string.


    Args:
        input_string (str): String with special characters.


    Returns:
        str: String without special characters.
    """
    special_chars = r'[./,_=\|`~\'"#;:@!()\$%+&^\*\{\}\[\]\\]'
    input_string = re.sub(special_chars, '', str(input_string))
    input_string = input_string.strip()
    return input_string


def remove_duplicates_from_list(iterable: list | tuple, convert_to_str: bool = False):
    """Removes duplicates from a list


    Args:
        iterable (list | tuple): List or tuple with duplicate values
        convert_to_str (bool): Automatically converts values to strings if a TypeError occurs (e.g., when mixing int, float, and str values)


    Returns:
        list
    """
    if isinstance(iterable, tuple):
        iterable = list(iterable)
    try:
        return sorted(set(iterable))
    except TypeError:
        if convert_to_str:
            iterable = [str(i) for i in iterable]
            return sorted(set(iterable))
        else:
            return None


def humanize_time(time: datetime|int=datetime.now()):
    """
    Obtenha um objeto datetime ou um carimbo de data/hora int() Epoch e retorne um
    string bonita como 'uma hora atrás', 'Ontem', '3 meses atrás',
    'agora', etc
    
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    
    Referência: https://stackoverflow.com/questions/1551382/user-friendly-time-format-in-python

    Args:
        time (datetime | int, optional): data preferencialmente datetime class. Defaults to datetime.now().

    Returns:
        str: data como por exemplo em redes sociais, um dia atrás, etc...
    """
    
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = 0
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "Agora mesmo"
        if second_diff < 60:
            return str(second_diff) + " segundo(s) atrás"
        if second_diff < 120:
            return "A um minuto atrás"
        if second_diff < 3600:
            return str(second_diff // 60) + " minuto(s) atrás"
        if second_diff < 7200:
            return "A uma hora atrás"
        if second_diff < 86400:
            return str(second_diff // 3600) + " hora(s) atrás"
    if day_diff == 1:
        return "Ontem"
    if day_diff < 7:
        return str(day_diff) + " dia(s) atrás"
    if day_diff < 31:
        return str(day_diff // 7) + " semana(s) atrás"
    if day_diff < 365:
        return str(day_diff // 30) + " mese(s) atrás"
    return str(day_diff // 365) + " ano(s) atrás"


def retrieve_files_with_extension(directory=get_current_path(), filter='*.pdf') -> list:
    """
    Retrieves all files with the specified extension that exist in the current directory, including subdirectories


    Args:
        directory (str, optional): Directory that the script will search. Defaults to 'get_current_path()'.
        filter (str, optional): filter for searching file types. Defaults to '*.pdf'.
    """
    files_with_extension = []
    for path, subdirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(path, file)
            if fnmatch.fnmatch(file, filter):
                files_with_extension.append(file_path)
    return files_with_extension


def file_with_absolute_path(dir:str|list|tuple, filename:str, create_dirs:bool=True) -> str:
    """Usa join para unir os caminhos enviados por ti para que funcionem em qualquer sistema operacional
    ele recupera o caminho absoluto do(s) diretorio(s) enviado e concatena com o file enviado

    Args:
        dir (str|list|tuple): Diretório ou diretórios que deseja unir.
        filename (str): Arquivo que deseja usar.
        create_dirs (bool, optional): Cria os diretórios para os files, Defaults is True

    Returns:
        str: caminho com o caminho absoluto
        
    Use:
        >>> # With list/tuple
        >>> file_db = file_with_absolute_path(['bin', 'database'], 'database.db') # -> CAMINHO_ABS/bin/database/database.db
        >>>
        >>> # With string
        >>> file_db = file_with_absolute_path('bin', 'database.db') # -> CAMINHO_ABS/bin/database.db
    """
    if isinstance(dir, (tuple, list)):
        if create_dirs:
            try:
                os.makedirs(os.path.join(os.path.abspath(dir[0]), *dir[1:]))
            except FileExistsError:
                pass        
            return os.path.join(os.path.abspath(dir[0]), *dir[1:], filename)
    else:
        if create_dirs:
            try:
                os.makedirs(os.path.abspath(dir))
            except FileExistsError:
                pass 
        return os.path.join(os.path.abspath(dir), filename)


def delete_files_with_keyword(directory: str, keyword: str, basename: bool = True):
    """
    Retrieves and deletes files based on the keyword sent


    Args:
        directory (str): Directory where you want to delete files
        keyword (str): Keyword in the file name or path that you want to delete the file
        basename (bool, optional): Whether to search in the file name or the full path. Defaults to True.
    """
    files = files_with_absolute_file_path(directory)
    for file in files:
        if basename:
            if keyword in os.path.basename(file):
                os.remove(file)
        else:
            if keyword in file:
                os.remove(file)


def object_type(obj):
    """Prints the type of the object"""
    return print(type(obj))


def check_for_duplicate_files_in_directory(directory: str):
    """
    Checks if there are files with the same name in the specified directory.


    Args:
        directory (str): The path of the directory to be checked.


    Returns:
        bool: Returns True if there are files with the same name in the directory, False otherwise.
    """
    path = os.path.abspath(directory)
    files = files_with_absolute_file_path(path)
    exists = []
    for file in files:
        if file in exists:
            return True
        else:
            exists.append(file)
    else:
        return False
    
def convert_to_float(value):
    """
    Converts a string of monetary value in Brazilian format to float.


    Args:
        value (str): String containing the monetary value to be converted,
        with possible prefix 'R$', thousand separators and decimal comma.


    Returns:
        float: Value converted to float.
    """
    number = value.replace('R$', '').strip()
    if number.count('.') > 1:
        parts = number.rsplit('.', 1)
        number = parts[0].replace('.', '') + '.' + parts[1]
    else:
        number = number.replace('.', '').replace(',', '.')
    return float(number)


def date_in_portuguese():
    """
    Returns the current date in the format "day Month year" in Portuguese.


    ### Returns:
    - A string containing the current date in the format "day Month year" (for example, "13 October 2024").


    ### Example usage:
    ```python
    current_date = date_in_portuguese()
    print(current_date)  # Output: "13 October 2024"
    ```
    """
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    return datetime.now().strftime('%d de %B de %Y')


def is_business_day(date):
    """
    Checks if a date is a business day in Brazil.


    ### Args:
        date (datetime.date): Date to be checked.


    ### Returns:
        bool: True if the date is a business day, False otherwise.


    ### Example usage:
    ```python
    from datetime import date
    date_obj = date(2024, 10, 13)
    if is_business_day(date_obj):
        print("It's a business day")
    else:
        print("It's not a business day")
    ```
    """
    return date.weekday() < 5 and date not in holidays.Brazil()


def get_business_days(start_date):
    """
    Retrieves the next two business days starting from a given date.


    ### Args:
        start_date (datetime.date): Initial date to start searching for business days.


    ### Returns:
        list: A list of the next two business days.


    ### Example usage:
    ```python
    from datetime import date, timedelta
    start_date = date(2024, 10, 13)
    business_days = get_business_days(start_date)
    print(business_days)
    ```
    """
    business_days = []
    current_date = start_date
    while len(business_days) < 2:
        current_date += timedelta(days=1)
        if is_business_day(current_date):
            business_days.append(current_date)
    return business_days


def clean_directory(directory: str, timeout_for_clear: int = 5, max_attempts: int = 3, support_long_names: bool = False):
    """
    Cleans a directory and attempts to remove files with long names if necessary.


    Args:
        directory (str): Path to the directory to clean.
        timeout_for_clear (int): Time in seconds to wait before retrying in case of a PermissionError. Default is 5.
        max_attempts (int): Maximum number of attempts to clean the directory. Default is 3.
        support_long_names (bool): If True, attempts to handle files with long names. Default is False.


    Returns:
        None


    Raises:
        PermissionError: If unable to clean the directory after the specified number of attempts.


    Example Usage:
    ```python
    import os

    # Define the directory to clean
    directory_to_clean = os.path.join(os.getcwd(), "example_directory")

    # Clean the directory with default settings
    clean_directory(directory_to_clean)

    # Clean the directory with custom settings
    clean_directory(directory_to_clean, timeout_for_clear=10, max_attempts=5, support_long_names=True)
    ```
    """

    DIRECTORY = os.path.abspath(directory)

    def try_create_dir(directory):
        """
        Attempts to create the directory if it does not exist.
        """
        try:
            os.makedirs(directory)
        except FileExistsError:
            pass

    if os.path.exists(DIRECTORY):
        attempts = 0
        success = False
        while not success and attempts < max_attempts:
            try:
                if support_long_names:
                    shutil.rmtree(support_long_paths(DIRECTORY))
                else:
                    shutil.rmtree(DIRECTORY)
                success = True
            except PermissionError:
                attempts += 1
                log(f"Attempt {attempts} failed. Trying again in {timeout_for_clear} seconds...")
                time.sleep(timeout_for_clear)
        if not success:
            raise PermissionError(f"Unable to clean directory {DIRECTORY} after {attempts} attempts.")

        try_create_dir(DIRECTORY)
    else:
        try_create_dir(DIRECTORY)