from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from src.sql_alchemy.db_model.macro import Macro


class RunCodeReq:
    driver: WebDriver
    macro: Macro
    element: WebElement

    def __init__(self, driver: WebDriver, macro: Macro, element: WebElement):
        self.driver = driver
        self.macro = macro
        self.element = element
