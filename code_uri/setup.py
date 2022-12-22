import os
import importlib
from globals import global_params
from src.utils.system import system_utils


# setup 시작
def configure(context):
    # system platform 확인
    context.platform = system_utils.check_platform()
    # lambda request_id 지정
    global_params.lambda_request_id = context.aws_request_id
    # db 모델 import
    import_all_in_file("./src/sql_alchemy/db_model")


# 해당 문구로 끝나는 파일 import
def import_all_ends_with(ends_with: str):
    for root, dirs, files in os.walk("./src"):
        for file in files:
            if file.endswith(ends_with):
                controller_path = os.path.join(root, file)
                # reformat
                controller_path = controller_path.replace('./', '', 1)
                controller_path = controller_path.replace('/', '.')
                controller_path = controller_path.replace('.py', '', 1)
                # import
                importlib.import_module(controller_path)


# 해당 문구로 끝나는 파일 import
def import_all_in_file(file_name: str):
    for root, dirs, files in os.walk(file_name):
        for file in files:
            if 'pyc' in file:
                continue
            controller_path = os.path.join(root, file)
            # reformat
            controller_path = controller_path.replace('./', '', 1)
            controller_path = controller_path.replace('/', '.')
            controller_path = controller_path.replace('.py', '', 1)
            # import
            importlib.import_module(controller_path)
