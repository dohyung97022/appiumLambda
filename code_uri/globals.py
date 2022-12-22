from src.sql_alchemy.db_model.action import Action
from src.sql_alchemy.db_model.macro import Macro


class GlobalParams:
    action: Action = None
    macro: Macro = None
    lambda_request_id: str

    img_index: int = 0
    img_name: str = None
    img_src: str = None

    html_index: int = 0
    html_name: str = None
    html_src: str = None

    global_store: dict = {}

    def reset_img_src(self):
        self.img_name = f'{self.lambda_request_id}_{self.img_index}.png'
        self.img_src = f'https://appiumapi.s3.amazonaws.com/lambda_images/{self.img_name}'
        self.img_index = self.img_index + 1

    def reset_html_src(self):
        self.html_name = f'{self.lambda_request_id}_{self.html_index}.html'
        self.html_src = f'https://appiumapi.s3.amazonaws.com/lambda_html/{self.html_name}'
        self.html_index = self.html_index + 1


global_params = GlobalParams()
