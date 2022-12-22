import random
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from globals import global_params
from src.selenium.service import selenium_run_code_service, selenium_log_service
from src.sql_alchemy.db_model.action import Action
from src.sql_alchemy.db_model.macro import Macro, MacroType, MacroOperator


def run_action(driver: WebDriver, action: Action):
    global_params.action = action

    # or 일 경우 취합 후 결정
    or_macro = []

    # 매크로 실행
    for i in range(len(action.macros)):

        macro: Macro = action.macros[i]

        # or 일 경우
        if macro.macro_operator == MacroOperator.OR:
            or_macro.append(macro)

            # 다음 매크로가 없거나, or 가 아닐 경우
            if i + 1 >= len(action.macros) or action.macros[i + 1].macro_operator != MacroOperator.OR:
                # 지정
                macro = random.choice(or_macro)
                or_macro = []
            else:
                continue

        try:
            global_params.macro = macro

            # 실행
            retry_macro(driver, macro)

            # 로깅
            selenium_log_service.info(driver)
        except Exception as e:
            if macro.macro_operator == MacroOperator.TRY:
                continue
            if macro.macro_operator == MacroOperator.FAIL_END:
                break

            # 로깅
            selenium_log_service.exception(driver, e)
            raise e

    # 자식 action 재귀 실행
    for child_action_association in action.child_action_associations:
        run_action(driver, child_action_association.child_action)

    return


def retry_macro(driver: WebDriver, macro: Macro):

    for i in range(macro.retry_times - 1):
        try:
            run_macro(driver, macro)
            return
        except Exception:
            time.sleep(macro.retry_wait_sec)
            pass

    run_macro(driver, macro)


def run_macro(driver: WebDriver, macro: Macro):

    # element 조회
    element = find_available_element(driver, macro.elements)

    # RUN
    if macro.macro_type is MacroType.RUN:
        selenium_run_code_service.run_code(driver, macro, element)
    # ERROR 찾으면 오류
    elif macro.macro_type == MacroType.ERROR:
        if element is not None:
            raise Exception(f"Error element is found. element : {macro.element}")
    # 못 찾으면 오류
    elif element is None:
        raise Exception(f"Error no element found. macro : {macro.to_dict()}")
    # CLICK
    elif macro.macro_type is MacroType.CLICK:
        element.click()
    # TYPE
    elif macro.macro_type is MacroType.TYPE:
        element.send_keys(macro.variable)
    # TYPE_CLEAR
    elif macro.macro_type is MacroType.TYPE_CLEAR:
        element.clear()

    time.sleep(random.uniform(macro.min_wait_sec, macro.max_wait_sec))


def find_available_element(driver: WebDriver, elements: list):

    for element in elements:
        if element.value == '':
            continue

        found_elements = driver.find_elements(element.type.to_element_by(), element.value)

        if len(found_elements) > element.index:
            return found_elements[element.index]

    return None
