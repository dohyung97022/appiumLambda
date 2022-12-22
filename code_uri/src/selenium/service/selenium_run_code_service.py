import datetime
import json

from selenium.webdriver.chrome.webdriver import WebDriver
from src.selenium.domain.run_code_req import RunCodeReq
from src.selenium.exception.device_store_key_exception import DeviceStoreKeyException
from src.selenium.exception.invalid_macro_variable_exception import InvalidMacroVariableException
from src.selenium.service import selenium_run_code_functions
from globals import global_params
from src.sql_alchemy.db_model.macro import Macro
from src.utils.object import object_utils
from src.utils.operator import operator_utils
from src.utils.string import string_utils


def run_code(driver: WebDriver, macro: Macro, element):

    # 변수 가져오기
    kwarg_variables = json.loads(f'{macro.variable}') if macro.variable != '' else {}

    # 내부 저장 변수 ex: {{key.value}}
    global_store = global_params.global_store

    for key, value in kwarg_variables.items():

        if not isinstance(value, str):
            kwarg_variables[key] = value
            continue

        # 앞의 비교 연산자 추가
        operator = None
        success, result = operator_utils.parse_comparison_operator(value)
        if success:
            if result.before is not None:
                raise InvalidMacroVariableException(f'{macro.variable}의 {result.before} 가 비교 연산자 이전 위치에 있으면 안됩니다.')
            operator = result.operator
            value = result.after

        # {{ }} 지정 방식
        success, command = string_utils.get_between(value, '{{', '}}')
        if success:

            # command 확인
            command_value = parse_custom_command(command)
            if command_value is not None:
                # command 일 경우
                value = command_value
            else:
                # 변수 일 경우
                attr_locators = command.split('.')
                attr_key = attr_locators[0]
                attr_locators = attr_locators[1:]

                # device_store 내에 없을 경우
                if attr_key not in global_store.keys():
                    raise DeviceStoreKeyException(f'{macro.variable}의 {attr_key} key 가 device_store 내에 존재하지 않습니다.')

                # 값 조회 반환
                value = global_store[attr_key]
                success, value = object_utils.get_leaf_attr(value, attr_locators)
                if not success:
                    raise InvalidMacroVariableException(f'{macro.variable}의 {attr_locators} 를 device_store 내에서 조회할 수 없습니다.')

        if operator is not None:
            value = (operator, value)

        kwarg_variables[key] = value

    # function 가져오기
    code_function = getattr(selenium_run_code_functions, macro.function_name)

    # function 실행
    code_function(RunCodeReq(driver, macro, element), **kwarg_variables)


def parse_custom_command(command: str) -> object:
    if command == 'now()':
        return datetime.datetime.now()

    return None
