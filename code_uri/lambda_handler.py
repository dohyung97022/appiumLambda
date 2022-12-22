import types
import setup
from src.automation.action.service import action_service
from src.selenium.service import selenium_service, selenium_run_service


def lambda_handler(event, context):
    setup.configure(context)

    action_seq = 1
    action = action_service.select_action(action_seq)
    driver = selenium_service.get_driver(context)
    selenium_run_service.run_action(driver, action)

    selenium_page = str(selenium_service.get_page_source(driver))

    response = {
        "statusCode": 200,
        "body": {
            "page": ''
        }
    }

    return response

context = types.SimpleNamespace()
context.aws_request_id = 'local'
lambda_handler(None, context)
