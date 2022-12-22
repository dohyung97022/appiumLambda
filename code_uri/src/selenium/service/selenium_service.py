import io

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from src.aws.aws_s3.service import s3_service
from fake_useragent import UserAgent

from src.utils.system import system_utils
from src.utils.system.enum.system_platform import SystemPlatform


def get_driver(context) -> WebDriver:
    options = Options()

    if context.platform is SystemPlatform.LINUX:
        options.binary_location = '/opt/headless-chromium'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'user-agent={UserAgent().random}')

    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}

    chrome_location = '/opt/chromedriver'
    if context.platform is SystemPlatform.MAC:
        chrome_location = '../chromedriver'

    return webdriver.Chrome(chrome_location, chrome_options=options, desired_capabilities=caps)


def goto_url(driver: WebDriver, url: str):
    driver.get(url)


def get_page_source(driver: WebDriver):
    return driver.page_source


def upload_screenshot(driver: WebDriver, file_name: str):
    screenshot_location = f'/tmp/{file_name}'
    if system_utils.check_platform().MAC:
        screenshot_location = f'../{file_name}'
    save_location = f'lambda_images/{file_name}'

    driver.save_screenshot(screenshot_location)
    s3_service.upload_file(screenshot_location, save_location, is_public=True)


def upload_html(driver: WebDriver, file_name: str):
    html_location = f'/tmp/{file_name}'
    if system_utils.check_platform().MAC:
        html_location = f'../{file_name}'
    save_location = f'lambda_html/{file_name}'

    with io.open(html_location, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
        f.close()
    s3_service.upload_file(html_location, save_location, is_public=True)


def exit_driver(driver: WebDriver):
    driver.close()
    driver.quit()
