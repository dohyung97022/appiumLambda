import time
from src.selenium.domain.run_code_req import RunCodeReq


def open_url(req: RunCodeReq, url: str):
    req.driver.get(url)


def switch_to_frame(req: RunCodeReq):
    req.driver.switch_to.frame(req.element)


def switch_to_default(req: RunCodeReq):
    req.driver.switch_to.default_content()


def set_attribute(req: RunCodeReq, key: str, value: str):
    req.driver.execute_script(f"arguments[0].setAttribute(arguments[1],arguments[2])", req.element, key, value)


def wait_until_element_css(req: RunCodeReq, value: str, wait_sec: int):
    for i in range(int(wait_sec)):
        try:
            element = req.driver.find_element(req.macro.element_type.to_element_by(), req.macro.element)
            if value in element.get_attribute('style'):
                return
        except:
            pass
        time.sleep(1)

    raise Exception(f"해당 css 가 변동하지 않았습니다. element: {req.macro.element}, css: {req.macro.element}, expected: {value}")


def delete_cookies(req: RunCodeReq):
    req.driver.delete_all_cookies()


def print_html(req: RunCodeReq):
    print(req.driver.page_source)
