import logging
import traceback
import json

from globals import global_params


class CustomLogger:
    logger = logging.Logger
    kwargs = {}

    def __init__(self):
        self.logger = logging.getLogger()

    def exception(self, exception: Exception, *args, **kwargs):
        self.add_empty_extra()
        self.add_lambda_request_id_extra()
        self.add_exception_extra(exception)
        self.kwargs.update(**kwargs)
        self.logger.setLevel(logging.ERROR)
        self.logger.error(f'{self.extra_as_json()}', *args, **self.kwargs)

    def warn_exception(self, exception: Exception, *args, **kwargs):
        self.add_empty_extra()
        self.add_lambda_request_id_extra()
        self.add_exception_extra(exception)
        self.kwargs.update(**kwargs)
        self.logger.setLevel(logging.WARN)
        self.logger.warn(f'{self.extra_as_json()}', *args, **self.kwargs)

    def info(self, message: str = '', *args, **kwargs):
        self.add_empty_extra()
        self.add_lambda_request_id_extra()
        self.kwargs.update(**kwargs)
        self.logger.setLevel(logging.INFO)
        self.logger.info(f'{message} {self.extra_as_json()}', *args, **self.kwargs)

    def add_empty_extra(self):
        if 'extra' not in self.kwargs.keys():
            self.kwargs['extra'] = {}

    def add_exception_extra(self, exception: Exception):
        self.kwargs['extra']['exceptionName'] = exception.__class__.__name__
        self.kwargs['extra']['exceptionMessage'] = str(exception)
        self.kwargs['extra']['exceptionStackTrace'] = "".join(traceback.TracebackException.from_exception(exception).format())

    def add_lambda_request_id_extra(self):
        self.kwargs['extra']['lambda'] = {'request_id': global_params.lambda_request_id}

    def extra_as_json(self) -> str:
        return json.dumps({'extra': self.kwargs['extra']})

