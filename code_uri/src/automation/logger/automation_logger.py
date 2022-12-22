from globals import global_params
from src.sql_alchemy.db_model.action import Action
from src.sql_alchemy.db_model.macro import Macro
from src.utils.log import log_utils


class AutomationLogger(log_utils.CustomLogger):

    def __init__(self):
        self.kwargs = {'extra': {'automation': {}}}
        if global_params.macro is not None:
            self.add_macro_extra(global_params.macro)
        if global_params.action is not None:
            self.add_action_extra(global_params.action)
        if global_params.img_src is not None:
            self.add_img_src_extra(global_params.img_src)
        if global_params.img_src is not None:
            self.add_html_src_extra(global_params.html_src)

        super(AutomationLogger, self).__init__()

    def add_macro_extra(self, macro: Macro):
        self.kwargs['extra']['automation']['macro'] = {
            'macro_seq': macro.macro_seq,
            'name': macro.name,
            'macro_type': macro.macro_type.name,
            'driver_type': macro.driver_type.name,
            'element': macro.element,
            'element_type': macro.element_type.name,
            'operator': macro.macro_operator.name,
            'macro_index': macro.macro_index,
            'variable': macro.variable,
            'retry_times': macro.retry_times
        }

    def add_action_extra(self, action: Action):
        self.kwargs['extra']['automation']['action'] = {
            'action_seq': action.action_seq,
            'name': action.name,
            'is_root': action.is_root
        }

    def add_img_src_extra(self, img_src):
        self.kwargs['extra']['automation']['img_src'] = img_src

    def add_html_src_extra(self, html_src):
        self.kwargs['extra']['automation']['html_src'] = html_src
