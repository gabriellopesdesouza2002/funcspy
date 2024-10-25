import json
import os
from base64 import b64decode
from subprocess import getoutput
from time import sleep
from selenium import Chrome
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from webdriver_manager.chrome import ChromeDriverManager
from funcspy.python_funcs.python_funcs import *
from funcspy.regex_funcs.regex_funcs import extract_email
from funcspy.utils_funcs.utils_funcs import *
import pickle

def current_url(driver) -> str:
    """
    ### Function RETURNS the current URL


    Args:
        driver (WebDriver): Your Webdriver (Chrome, Firefox, Opera...)


    Returns:
        (str): Current URL of the current window
    """
    return driver.current_url


def refresh_current_page(driver) -> None:
    """
    ### Function updates the current page of the current window


    Args:
        driver (WebDriver): Your Webdriver (Chrome, Firefox, Opera...)
    """
    driver.refresh()


def wait_and_click_on_multiple_elements(wdw:WebDriverWait, locator: tuple, in_dom=False) -> None:
    """
    ### Function waits for multiple elements to be present and then clicks on them


    Args:
        wdw (WebDriverWait): WebDriverWait instance
        locator (tuple): Locator tuple for the elements
        in_dom (bool): Whether to wait for a single element or multiple elements (default: False)


    Returns:
        None
    """
    driver = wdw._driver
    if in_dom:
        wdw.until(EC.presence_of_element_located(locator))
    else:
        wdw.until(EC.presence_of_all_elements_located(locator))
    elements = driver.find_elements(*locator)
    len_elements = len(elements)

    for i in range(len_elements):
        elements[i].click()
        sleep(0.5)


def wait_for_element_and_click(wdw:WebDriverWait, locator: tuple, in_dom:bool=False) -> None:
    """
    ### Waits for the element to be available for click and clicks


    Args:
        wdw (WebDriverWait): WebDriverWait instance
        locator (tuple): Element location -> (By.CSS_SELECTOR, '.b')
        in_dom (bool): Whether to wait for presence or clickability (default: False)


    Returns:
        None
    """
    if in_dom:
        return wdw.until(EC.presence_of_element_located(locator))
    else:
        wdw.until(EC.element_to_be_clickable(locator)).click()


def wait_for_element(wdw:WebDriverWait, locator: tuple, in_dom:bool=False) -> WebElement:
    """
    ### Function that waits for the element sent by the locator


    Args:
        wdw (WebDriverWait): Your WebDriverWait instance
        locator (tuple): The location of the element in the DOM (By.CSS_SELECTOR, '#IdButton')
        in_dom (bool): Whether to verify if the element is present in the DOM


    Returns:
        WebElement: The waited element
    """
    if in_dom:
        return wdw.until(EC.presence_of_element_located(locator))
    else:
        return wdw.until(EC.element_to_be_clickable(locator))


def set_page_zoom(driver, zoom: int):
    """
    ### Sets the zoom of the current page


    Args:
        driver (WebDriver): WebDriver instance
        zoom (int): The zoom level to set


    Returns:
        None
    """
    driver.execute_script(f"document.body.style.zoom='{zoom}%'")


def wait_for_element_and_send_keys(wdw:WebDriverWait, string, locator: tuple, in_dom=False) -> None:
    """
    ### Function that waits for the element sent by the locator and sends send_keys to the input or textarea as soon as possible


    Args:
        wdw (WebDriverWait): Your WebDriverWait instance
        string (str): The string to send to the element
        locator (tuple): The location of the element in the DOM (By.CSS_SELECTOR, '#IdButton')
        in_dom (bool): Whether to wait for presence or clickability (default: False)


    Returns:
        None
    """
    driver = wdw._driver
    if in_dom:
        wdw.until(EC.presence_of_element_located(locator))
    else:
        wdw.until(EC.element_to_be_clickable(locator))

    driver.find_element(*locator).send_keys(string)


def set_zoom_page(driver, zoom: int) -> None:
    """Seta o zoom da página atual

    Args:
        driver (WebDriver): WebDriver
        zoom (int): O zoom para setar.
    """
    driver.execute_script(f"document.body.style.zoom='{zoom}%'")


def wait_and_return_element_list(wdw:WebDriverWait, locator: tuple, in_dom=False) -> list[WebElement]:
    """
    ### Function waits and returns a list of elements indicated by the locator


    Args:
        wdw (WebDriverWait): Your WebDriverWait instance
        locator (tuple): The tuple indicating the location of the element in the DOM ("BY_SELECTOR", "#list_arms")


    Returns:
        list: List of elements in object format (list of objects)
    """
    driver = wdw._driver
    if in_dom:
        wdw.until(EC.presence_of_element_located(locator))
    else:
        wdw.until(EC.element_to_be_clickable(locator))
    return driver.find_elements(*locator)


def download_file_with_link_no_ext_pdf(link: str, driver, back_to_page: bool=False):
    """
    ### Downloads the pdf with the link from the href, it will enter the pdf and print the page


    Args:
        link (str): Link of the file you want to download
        driver (WebDriver): WebDriver instance
        back_to_page (bool): If you want to go back to the previous page. Optional, default is False


    Use:
        >>> link = wait_and_return_attribute_content(DRIVER, WDW3, 'href', (By.CSS_SELECTOR, 'div>a'))
        >>> download_file_with_link_no_ext_pdf(link, mywebdriver, False)
    """
    driver.get(link)
    sleep(3)
    driver.print_page()
    if back_to_page:
        driver.back()
        driver.refresh()


def wait_and_return_element_list_text_from_id(wdw:WebDriverWait, locator: tuple, in_dom=False) -> list[str]:
    """
    ### Function waits and returns a list of elements with id


    Args:
        wdw (WebDriverWait): Your WebDriverWait instance
        locator (tuple): The tuple indicating the location of the element in the DOM ("BY_SELECTOR", "#list_arms")


    Returns:
        list: List of texts of elements with id -> [adv 1, adv 2, adv 3, adv 4, adv 5]
    """
    driver = wdw._driver
    if in_dom:
        wdw.until(EC.presence_of_element_located(locator))
    else:
        wdw.until(EC.element_to_be_clickable(locator))

    webelements = driver.find_elements(*locator)
    id = 1
    elements_with_id = []
    for element in webelements:
        if element.text == ' ':
            elements_with_id.append(element.text)
        else:
            elements_with_id.append(f'{element.text} {id}')
        id += 1
    return elements_with_id


def wait_and_return_element_list_text(wdw:WebDriverWait, locator: tuple, in_dom=False, upper_mode: bool=False, strip_mode: bool=False) -> list[str]:
    """
    ### Function waits and returns a list with the texts of the elements


    Args:
        wdw (WebDriverWait): Your WebDriverWait instance
        locator (tuple): The tuple indicating the location of the element in the DOM ("BY_SELECTOR", "#list_arms")
        in_dom (bool): Whether to wait for presence or clickability (default: False)
        upper_mode (bool): Whether to return the texts in uppercase (default: False)
        strip_mode (bool): Whether to remove leading and trailing whitespaces from the texts (default: False)


    Returns:
        list: List of texts of the elements
    """
    driver = wdw._driver
    if in_dom:
        wdw.until(EC.presence_of_element_located(locator))
    else:
        wdw.until(EC.element_to_be_clickable(locator))
    elements = driver.find_elements(*locator)
    if upper_mode:
        return [element.text.upper() for element in elements]
    if strip_mode:
        return [element.text.strip() for element in elements]
    return [element.text for element in elements]


def wait_for_element_to_be_visible(wdw:WebDriverWait, locator: tuple) -> WebElement|None:
    """
    ### Waits for the element to be visible on the screen


    Args:
        wdw (WebDriverWait): WebDriverWait instance
        locator (tuple): Locator tuple


    Returns:
        WebElement|None: The visible WebElement or None
    """
    driver = wdw._driver
    element = driver.find_element(*locator)
    return wdw.until(EC.visibility_of(element))


def download_pdf_via_base64_headless_only(wdw: WebDriver, file_pdf_with_extension: str='MyPDF.pdf', locator: tuple=(By.CSS_SELECTOR, 'html'), in_dom=False):
    """
    ### Works only with headless mode!
    Requires the driver to be already opened, passing only the locator to convert to PDF


    Args:
        file_pdf_with_extension (str, optional): File name with extension. Defaults to 'MyPDF.pdf'.
        locator (tuple, optional): Locator tuple. Defaults to (By.CSS_SELECTOR, 'html').


    Raises:
        ValueError: If the PDF file signature is missing
    """
    FILE_PDF = os.path.abspath(file_pdf_with_extension)
    driver = wdw._driver
    if in_dom:
        element = wdw.until(EC.presence_of_element_located(locator))
    else:
        element = driver.find_element(*locator)

    ActionChains(driver).click(element).click_and_hold().move_by_offset(0, 0).perform()

    element = driver.execute_cdp_cmd("Page.printToPDF", {"path": 'html-page.pdf', "format": 'A4'})

    b64 = element['data']

    bytes = b64decode(b64, validate=True)

    if bytes[0:4] != b'%PDF':
        raise ValueError('Missing the PDF file signature')

    try:
        with open(FILE_PDF, 'wb') as f:
            f.write(bytes)
    except FileNotFoundError:
        create_last_directory_of_file(FILE_PDF)
        with open(FILE_PDF, 'wb') as f:
            f.write(bytes)


def check_vpn_connection(ping_host: str):
    """
    ### Checks if VPN is connected by pinging the specified host
    """
    PING_HOST = ping_host

    log('Verifying VPN connection via IP from config.ini')
    
    output = getoutput(f'ping {PING_HOST} -n 1')  # -n 1 limits the output
    if 'Esgotado o tempo' in output or 'time out' in output:
        log('VPN NOT CONNECTED!', 'w')
    else:
        log("VPN connected successfully!")


def wait_for_element_to_be_visible_active_and_clickable(wdw:WebDriverWait, locator: tuple, in_dom=False) -> WebElement|None:
    """
    ### Waits for the element to be visible, active, and clickable


    Args:
        wdw (WebDriverWait): WebDriverWait instance
        locator (tuple): Selenium locator tuple


    Returns:
        WebElement|None: The visible, active, and clickable WebElement or None
    """
    driver = wdw._driver
    element = driver.find_element(*locator)
    if in_dom:
        wdw.until(EC.presence_of_element_located(locator))
    else:
        wdw.until(EC.element_to_be_clickable(locator))
    return wdw.until(EC.visibility_of(element))


def wait_and_return_element_attribute_text(wdw:WebDriverWait, attribute: str, locator: tuple, in_dom=False) -> str:
    """
    ### Function that waits for the element and returns the text of the chosen attribute


    Args:
        wdw (WebDriverWait): Your WebDriverWait instance
        attribute (str): The attribute you want to retrieve, such as href, id, class, etc.
        locator (tuple): The location of the element in the DOM ("By.CSS_SELECTOR", "body > div > a").


    Returns:
        str: Returns a string with the value of the element's attribute
    """
    driver = wdw._driver
    if in_dom:
        wdw.until(EC.presence_of_element_located(locator))
    else:
        wdw.until(EC.element_to_be_clickable(locator))

    return driver.find_element(*locator).get_attribute(attribute)


def wait_and_return_elements_attributes_text(wdw:WebDriverWait, attribute: str, locator: tuple, in_dom=False) -> list:
    """
    ### Function waits and returns the values of attributes from multiple elements


    Args:
        wdw (WebDriverWait): Your WebDriverWait instance
        attribute (str): Attribute (this must exist in all elements)
        locator (tuple): Position of elements in the DOM ("By.CSS_SELECTOR", "#list_works").


    Returns:
        list: List of attributes from all elements (it is necessary that the sent attribute exists in all elements, such as an href)
    """
    driver = wdw._driver
    if in_dom:
        wdw.until(EC.presence_of_element_located(locator))
    else:
        wdw.until(EC.element_to_be_clickable(locator))

    elements = driver.find_elements(*locator)
    elements_attributes = [element.get_attribute(attribute) for element in elements]
    return elements_attributes


def wait_and_return_element_text(wdw:WebDriverWait, locator: tuple, in_dom=False) -> str:
    """
    ### Function waits for the element and returns its text


    Args:
        wdw (WebDriverWait): Your WebDriverWait instance
        locator (tuple): Location of the element in the DOM ("By.CSS_SELECTOR", "#name")


    Returns:
        str: Returns the text of the element as a string
    """
    driver = wdw._driver
    if in_dom:
        wdw.until(EC.presence_of_element_located(locator))
    else:
        wdw.until(EC.element_to_be_clickable(locator))
    return driver.find_element(*locator).text
    
    
def switch_to_first_window(driver) -> None:
    """
    ### Switches to the first window, usually the one that is initially opened


    Args:
        driver (WebDriver): WebDriver instance
    """
    window_ids = driver.window_handles  # IDs of all windows
    driver.switch_to.window(window_ids[0])
    
    
def wait_for_n_windows_and_switch_to_last(wdw:WebDriverWait, num_windows: int=2) -> None:
    """
    ### Waits for the specified number of windows to open and then switches to the last one


    Args:
        wdw (WebDriverWait): WebDriverWait instance
        num_windows (int): Number of windows expected to open. Defaults to 2.
    """
    driver = wdw._driver
    try:
        wdw.until(EC.number_of_windows_to_be(num_windows))
        window_ids = driver.window_handles
        driver.switch_to.window(window_ids[-1])  # Switch to the last window
    except TimeoutException:
        return False
    
    
def switch_to_window_by_title(driver, title_contain_switch: str) -> None:
    """
    ### Switches to the window that contains the specified title


    Args:
        driver (WebDriver): WebDriver instance
        title_contain_switch (str): At least one part of the title that should exist to switch to the page
    """
    window_ids = driver.window_handles  # IDs of all windows

    for window in window_ids:
        driver.switch_to.window(window)  # Switch to the current window
        if title_contain_switch in driver.title:
            break
    else:
        print(f'Window not found!\n'
            f'Check the value sent {title_contain_switch}')
    
    
def close_current_window(driver) -> None:
    """
    ### Closes the current window


    Args:
        driver (WebDriver): Your WebDriver instance (Chrome, Firefox)
    """
    driver.close()


def close_last_window(driver) -> None:
    """
    ### Closes the last opened window and switches back to the first one


    Args:
        driver (WebDriver): Your WebDriver instance
    """
    while len(driver.window_handles) != 1:
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
    driver.switch_to.window(driver.window_handles[0])


def go_back_pages(driver, num_pages_to_go_back: int = 1, wait_time_per_page: int | float = 0) -> None:
    """
    ### This function goes back (back) the number of pages you want


    Args:
        driver (WebDriver): Your WebDriver instance
        num_pages_to_go_back (int): The number of pages to go back. The default is one page (1).
        wait_time_per_page (int or float, optional): If you want to wait a certain time before going back a page. The default is 0.

    Usage:
        go_back_pages(driver=chrome, num_pages_to_go_back=3, wait_time_per_page=1)
    """
    if wait_time_per_page == 0:
        for _ in range(num_pages_to_go_back):
            driver.back()
            driver.refresh()
    else:
        for _ in range(num_pages_to_go_back):
            sleep(wait_time_per_page)
            driver.back()
            driver.refresh()


def create_user_agent() -> str:
    """
    ### Creates a user agent automatically with the fake_useragent library


    Returns:
        str: user_agent
    """
    from random import choice
    user_agent = choice(USER_AGENTS)
    return user_agent


def wait_input_clear_and_send_keys_press_esc(wdw:WebDriverWait, keys: str, locator: tuple, in_dom=False) -> None:
    """
    ### Function waits for the input or textarea indicated by the locator, clears it and sends the data


    Args:
        driver (WebDriver): Your webdriver
        wdw (WebDriverWait): WebDriverWait created in your code
        keys (str): Your string to send to the input or textarea
        locator (tuple): Tuple containing the form and path of the element (By.CSS_SELECTOR, '#myelementid')
    """
    driver = wdw._driver
    try:
        if in_dom:
            wdw.until(EC.presence_of_element_located(locator))
        else:
            wdw.until(EC.element_to_be_clickable(locator))
        driver.find_element(*locator).click()
        driver.find_element(*locator).send_keys(Keys.ESCAPE)
        driver.find_element(*locator).clear()
        driver.find_element(*locator).send_keys(keys)
    except StaleElementReferenceException:
        if in_dom:
            wdw.until(EC.presence_of_element_located(locator))
        else:
            wdw.until(EC.element_to_be_clickable(locator))
        driver.find_element(*locator).click()
        driver.find_element(*locator).send_keys(Keys.ESCAPE)
        driver.find_element(*locator).clear()
        driver.find_element(*locator).send_keys(keys)

    
def wait_input_clear_and_send_keys(wdw:WebDriverWait, keys: str, locator: tuple, click: bool = True, in_dom: bool = False) -> None:
    """
    ### Function waits for the input or textarea indicated by the locator, clears it and sends the data


    Args:
        driver (WebDriver): Your webdriver
        wdw (WebDriverWait): WebDriverWait created in your code
        keys (str): Your string to send to the input or textarea
        locator (tuple): Tuple containing the form and path of the element (By.CSS_SELECTOR, '#myelementid')
        click (bool): Clicks or not on the element
    """
    driver = wdw._driver
    try:
        if in_dom:
            wdw.until(EC.presence_of_element_located(locator))
        else:
            wdw.until(EC.element_to_be_clickable(locator))
        if click:
            driver.find_element(*locator).click()
        driver.find_element(*locator).clear()
        driver.find_element(*locator).send_keys(keys)
    except StaleElementReferenceException:
        if in_dom:
            wdw.until(EC.presence_of_element_located(locator))
        else:
            wdw.until(EC.element_to_be_clickable(locator))
        if click:
            driver.find_element(*locator).click()
        driver.find_element(*locator).clear()
        driver.find_element(*locator).send_keys(keys)

        
def wait_for_element_to_leave_dom(wdw:WebDriverWait, locator) -> WebElement:
    """
    ### Waits for the element to be removed from the DOM


    Args:
        wdw (WebDriverWait): WebDriverWait created in your code
        locator (tuple): Tuple containing the form and path of the element (By.CSS_SELECTOR, '#myelementid')


    Returns:
        WebElement: The element that was removed from the DOM
    """
    return wdw.until_not(EC.presence_of_element_located(locator))


def wait_for_element_to_be_active_and_click(wdw:WebDriverWait, locator: tuple, in_dom: bool = False) -> None:
    """
    ### Waits for the element to be active and then clicks on it


    Args:
        wdw (WebDriverWait): WebDriverWait created in your code
        locator (tuple): Tuple containing the form and path of the element (By.CSS_SELECTOR, '#myelementid')
        in_dom (bool): Whether to wait for the element to be present in the DOM or not


    Note:
        If in_dom is True, the function will wait for the element to be present in the DOM.
        If in_dom is False, the function will wait for the element to be not selected.
    """
    driver = wdw._driver
    if in_dom:
        wdw.until(EC.presence_of_element_located(locator))
    else:
        wdw.until_not(EC.element_to_be_selected(driver.find_element(*locator)))

    driver.find_element(*locator).click()
        
        
def wait_for_element_to_no_longer_be_visible(wdw:WebDriverWait, locator) -> WebElement:
    """
    ### Waits for the element to no longer be visible


    Args:
        wdw (WebDriverWait): WebDriverWait created in your code
        locator (tuple): Tuple containing the form and path of the element (By.CSS_SELECTOR, '#myelementid')


    Returns:
        WebElement: The element that is no longer visible
    """
    return wdw.until_not(EC.visibility_of(*locator))


def wait_for_element_to_be_visible(wdw:WebDriverWait, locator, with_visibility_of: bool = True):
    """
    ### Waits for the element to be visible


    Args:
        wdw (WebDriverWait): WebDriverWait created in your code
        locator (tuple): Tuple containing the form and path of the element (By.CSS_SELECTOR, '#myelementid')
        with_visibility_of (bool): Whether to use the visibility_of condition or the element_to_be_clickable condition


    Returns:
        WebElement: The element that is visible


    Note:
        If with_visibility_of is True, the function will wait for the element to be visible.
        If with_visibility_of is False, the function will wait for the element to be clickable.
    """
    driver = wdw._driver
    if with_visibility_of:
        element = driver.find_element(*locator)
        return wdw.until(EC.visibility_of(element))
    else:
        element = driver.find_element(*locator)
        return wdw.until(EC.element_to_be_clickable(locator))
        

def find_window_to_title_contain(driver, title_contain_switch: str) -> None:
    """
    ### This function switches to a window when the title contains at least part of the parameter sent


    Args:
        driver: The webdriver instance
        title_contain_switch (str): The string to search for in the window title


    Note:
        The function will switch to the first window that has a title containing the specified string.
        If no window is found, it will print an error message.
    """
    window_ids = driver.window_handles  # ids of all windows

    for window in window_ids:
        driver.switch_to_window(window)
        if title_contain_switch in driver.title:
            break
    else:
        print(f'Window not found!\n'
              f'Check the value sent {title_contain_switch}')
    
    
def find_window_to_url(driver, url_switch: str) -> None:
    """
    ### This function switches to a window when the URL matches the parameter sent


    Args:
        driver: The webdriver instance
        url_switch (str): The URL to search for


    Note:
        The function will switch to the first window that has a URL matching the specified string.
        If no window is found, it will print an error message.
    """
    window_ids = driver.window_handles  # ids of all windows

    for window in window_ids:
        driver.switch_to_window(window)
        if driver.current_url == url_switch:
            break
    else:
        print(f'Window not found!\n'
              f'Check the value sent "{url_switch}"')
    

def find_window_to_url_contain(driver, contain_url_switch: str) -> None:
    """
    ### This function switches to a window when the URL contains the parameter sent


    Args:
        driver: The webdriver instance
        contain_url_switch (str): The string to search for in the URL


    Note:
        The function will switch to the first window that has a URL containing the specified string.
        If no window is found, it will print an error message.
    """
    window_ids = driver.window_handles  # ids of all windows

    for window in window_ids:
        driver.switch_to.window(window)
        if contain_url_switch in driver.current_url:
            break
    else:
        print(f'Window not found!\n'
              f'Check the value sent "{contain_url_switch}"')

        
def get_element_source_code(wdw:WebDriverWait, locator: tuple, in_dom: bool = False) -> str:
    """Returns the entire source code of the element


    Args:
        wdw (WebDriverWait): WebDriverWait instance
        locator (tuple): Tuple containing the form and path of the element (By.ID, '.b')
        in_dom (bool): Whether to wait for the element to be present in the DOM or not


    Returns:
        str: Source code of the WebElement
    """
    driver = wdw._driver
    if in_dom:
        wdw.until(EC.presence_of_element_located(locator))
    else:
        wdw.until(EC.element_to_be_clickable(locator))
    element = driver.find_element(*locator)
    return element.get_attribute("outerHTML")


def verify_window_count_decreased(driver, expected_window_count) -> None:
    """
    ### Verifies if the number of windows has decreased


    Args:
        driver: The webdriver instance
        expected_window_count (int): The expected number of windows


    Note:
        If the number of windows is still greater than or equal to the expected count,
        it will wait until the number of windows decreases.
    """
    if len(driver.window_handles) == expected_window_count:
        while len(driver.window_handles) >= expected_window_count:
            pass
        else:
            window_ids = driver.window_handles  # ids of all windows
            driver.switch_to.window(window_ids[1])  # switch to the last window
            driver.close()
    else:
        verify_window_count_decreased(driver, expected_window_count)


def find_window_to_url_contain_and_close(driver, contain_url_to_switch: str) -> None:
    """
    ### This function switches to a window when the URL contains the parameter sent and closes it


    Args:
        driver: The webdriver instance
        contain_url_to_switch (str): The string to search for in the URL


    Note:
        The function will switch to the first window that has a URL containing the specified string and close it.
    """
    window_ids = driver.window_handles  # ids of all windows

    for window in window_ids:
        driver.switch_to.window(window)
        if contain_url_to_switch in driver.current_url:
            driver.close()
            break


def wait_for_input_clear_and_send_keys_press_esc(wdw:WebDriverWait, keys: str, locator: tuple) -> None:
    """
    ### Waits for the input or textarea to be clickable, clears it, and sends the specified keys


    Args:
        wdw (WebDriverWait): WebDriverWait instance
        keys (str): The string to send to the input or textarea
        locator (tuple): Tuple containing the form and path of the element (By.CSS_SELECTOR, '#myelementid')


    Note:
        The function will wait for the element to be clickable, clear it, send the specified keys, and press ESC twice.
        If a StaleElementReferenceException occurs, it will retry the operation.
    """
    driver = wdw._driver
    try:
        wdw.until(EC.element_to_be_clickable(locator))
        driver.find_element(*locator).click()
        driver.find_element(*locator).send_keys(Keys.ESCAPE)
        driver.find_element(*locator).clear()
        driver.find_element(*locator).send_keys(keys)
        driver.find_element(*locator).send_keys(Keys.ESCAPE)
    except StaleElementReferenceException:
        wdw.until(EC.element_to_be_clickable(locator))
        driver.find_element(*locator).click()
        driver.find_element(*locator).send_keys(Keys.ESCAPE)
        driver.find_element(*locator).clear()
        driver.find_element(*locator).send_keys(keys)
        driver.find_element(*locator).send_keys(Keys.ESCAPE)


def retrieve_text_from_website(url: str, tag_name: str = 'body', remove_escape_sequence: bool = True, sleep_request: int = 0) -> str:
    """
    ### Retrieves the text from a website based on the provided tag name


    Args:
        url (str): The URL of the website
        tag_name (str, optional): The tag name to search for. Defaults to 'body'.
        remove_escape_sequence (bool, optional): Whether to remove newline characters from the text. Defaults to True.
        sleep_request (int, optional): The number of seconds to wait before making the request. Defaults to 0.


    Returns:
        str: The text from the website or the specified element
    """
    from bs4 import BeautifulSoup
    import requests
    import time
    r = requests.get(url)
    time.sleep(sleep_request)
    soup = BeautifulSoup(r.content, 'html5lib')
    if remove_escape_sequence:
        return soup.find(tag_name).text.replace('\n', '').replace(u'\xa0', u' ')
    else:
        return soup.find(tag_name).text.replace(u'\xa0', u' ')
    

def wait_for_input_clear_and_send_keys_action_chains(wdw:WebDriverWait, keys: str, locator: tuple, in_dom: bool = False) -> None:
    """
    ### Waits for the input or textarea to be present or clickable, clears it, and sends the specified keys using ActionChains


    Args:
        wdw (WebDriverWait): WebDriverWait instance
        keys (str): The string to send to the input or textarea
        locator (tuple): Tuple containing the form and path of the element (By.CSS_SELECTOR, '#myelementid')
        in_dom (bool, optional): Whether to wait for the element to be present in the DOM or clickable. Defaults to False.


    Note:
        The function will wait for the element to be present or clickable, clear it, and send the specified keys using ActionChains.
        If a StaleElementReferenceException occurs, it will retry the operation.
    """
    from selenium.common.exceptions import StaleElementReferenceException
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys

    driver = wdw._driver
    try:
        if in_dom:
            wdw.until(EC.presence_of_element_located(locator))
        else:
            wdw.until(EC.element_to_be_clickable(locator))

        element = driver.find_element(*locator)
        ActionChains(driver).click(element).perform()
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        for char in keys:
            element.send_keys(char)
    except StaleElementReferenceException:
        if in_dom:
            wdw.until(EC.presence_of_element_located(locator))
        else:
            wdw.until(EC.element_to_be_clickable(locator))
        element = driver.find_element(*locator)
        ActionChains(driver).click(element).perform()
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        for char in keys:
            element.send_keys(char)


def verify_download_file(directory: str, keyword: str, sleep_time: int = 0, return_file: bool = False, verify_big_file: bool = False, timeout: int = 30, verify_if_element_exists: bool | dict = False) -> bool | str:
    """
    ### Verifies if a file with a keyword was downloaded to a specified directory and returns the last downloaded file.


    Args:
        directory (str): The path to the download directory.
        keyword (str): The keyword to search for in the downloaded file names (uses regex), ".pdf|.jpg".
        sleep_time (int, optional): The time to wait before checking the download directory again. Defaults to 0.
        return_file (bool, optional): Whether to return the path of the downloaded file. Defaults to False.
        verify_big_file (bool, optional): Whether to verify files with long names. Defaults to False.
        timeout (int, optional): The maximum time to wait for the file to be downloaded, in seconds. Defaults to 30.
        verify_if_element_exists (bool|dict, optional): Whether to verify if a specific element has disappeared from the DOM
            before starting the file verification. If a dictionary, it should contain:
            - 'WDW' (WebDriverWait): The explicit wait instance.
            - 'SELECTOR' (tuple): The selectors of the element to wait for in the DOM (e.g., (By.CSS_SELECTOR, '#Element')).
            Defaults to False, which means it does not verify if the element has disappeared.


    Returns:
        bool|str: Returns True if the file was downloaded successfully, False otherwise. If return_file is True,
            returns the absolute path of the last downloaded file.
    """

    if verify_if_element_exists:
        wait_for_element_to_leave_dom(verify_if_element_exists['WDW'], verify_if_element_exists['SELECTOR'])

    download_directory = os.path.abspath(directory)
    downloaded = False
    start_time = time.time()
    last_file = None
    while not downloaded:
        current_time = time.time()
        if current_time - start_time > timeout:
            return False
        files = os.listdir(download_directory)
        if verify_big_file:
            files = [support_long_paths(x).lower() for x in files]
        else:
            files = [x.lower() for x in files]

        if len(files) == 0:
            sleep(sleep_time)
            downloaded = False
        else:
            for file in files:
                if 'crdownload' in file.lower():
                    sleep(sleep_time)
                    downloaded = False
                    continue
                if re.search(keyword, file) is not None:
                    last_file = file
                    downloaded = True
                    print('Download completed!')
                    break

            if downloaded:
                if return_file:
                    return os.path.join(download_directory, last_file)
                else:
                    return True
            else:
                sleep(sleep_time)
                
                
def get_elements_independently_of_iframes(WDW: WebDriverWait, locator: tuple) -> list:
    """
    ### Returns a list of WebElements, regardless of the number of iframes in the DOM. The function searches for elements
    ### in the main context and within all iframes present on the page.


    Args:
        WDW (WebDriverWait): The WebDriverWait instance for explicit wait control.
        locator (tuple): A Selenium locator (e.g., (By.CSS_SELECTOR, '#my_element')).


    Returns:
        list: A list of WebElements found. If no elements are found, returns an empty list.


    Usage:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait


        driver = webdriver.Chrome()
        driver.get('YOUR_SITE_URL')


        wait = WebDriverWait(driver, 10)
        locator = (By.CSS_SELECTOR, 'YOUR_ELEMENT_SELECTOR')


        elements = get_elements_independently_of_iframes(wait, locator)
        for element in elements:
            print(element.text)


        driver.quit()
    """

    def find_elements_in_iframes(driver, locator):
        elements = []
        try:
            elements = driver.find_elements(*locator)
            if elements:
                return elements
        except NoSuchElementException:
            pass

        iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        for iframe in iframes:
            driver.switch_to.frame(iframe)
            elements = find_elements_in_iframes(driver, locator)
            if elements:
                return elements
            driver.switch_to.default_content()

        return elements

    driver = WDW._driver
    try:
        elements = find_elements_in_iframes(driver, locator)
        if not elements:
            WDW.until(EC.presence_of_element_located(locator))
            elements = driver.find_elements(*locator)
        return elements
    except TimeoutException:
        return []


def save_cookies(driver, cookie_file: str = 'cookies.pkl') -> str:
    """
    ### Saves the browser cookies to a file for future reuse.


    Args:
        driver (WebDriver): The WebDriver instance containing the cookies to be saved.
        cookie_file (str, optional): The name of the file where the cookies will be saved. Defaults to 'cookies.pkl'.


    Returns:
        str: Returns the name of the file where the cookies were saved.


    Usage:
        from selenium import webdriver


        driver = webdriver.Chrome()
        driver.get('https://www.yoursite.com')  # The driver must have navigated to the site before saving cookies

        # After login or navigation
        save_cookies(driver, 'my_cookies.pkl')
    """
    with open(cookie_file, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)
    return cookie_file


def load_cookies(driver, cookie_file: str = 'cookies.pkl') -> bool:
    """
    ### Loads cookies from a file and adds them to the WebDriver.


    Args:
        driver (WebDriver): The WebDriver instance to which the cookies will be loaded.
        cookie_file (str, optional): The name of the file from which the cookies will be loaded. Defaults to 'cookies.pkl'.


    Returns:
        bool: Returns True if the cookies were loaded successfully, False if the cookie file was not found.


    Usage:
        from selenium import webdriver


        driver = webdriver.Chrome()
        driver.get('https://www.yoursite.com')  # The driver must have navigated to the site before loading cookies

        if load_cookies(driver, 'my_cookies.pkl'):
            driver.refresh()  # Reloads the page with the loaded cookies
        else:
            print("Manual login required.")
    """
    try:
        with open(cookie_file, 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        print("Cookies loaded successfully.")
        return True
    except FileNotFoundError:
        print("Cookie file not found. Manual login required.")
        return False