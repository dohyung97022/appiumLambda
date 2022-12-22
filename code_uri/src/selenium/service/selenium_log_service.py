from selenium.webdriver.chrome.webdriver import WebDriver

from globals import global_params
from src.automation.logger.automation_logger import AutomationLogger
from src.selenium.service import selenium_service


def info(driver: WebDriver, msg: str = ''):
    global_params.reset_img_src()
    selenium_service.upload_screenshot(driver, global_params.img_name)
    global_params.reset_html_src()
    selenium_service.upload_html(driver, global_params.html_name)
    AutomationLogger().info(msg)


def exception(driver: WebDriver, e: Exception):
    global_params.reset_img_src()
    selenium_service.upload_screenshot(driver, global_params.img_name)
    global_params.reset_html_src()
    selenium_service.upload_html(driver, global_params.html_name)
    AutomationLogger().exception(e)
