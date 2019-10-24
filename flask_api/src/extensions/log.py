from logging import Formatter, INFO
from logging.handlers import RotatingFileHandler


class Logger:
    def __init__(self):
        self.formatter = Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    def _get_file_handler(self, log_file):
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=10
        )
        file_handler.setFormatter(self.formatter)
        file_handler.setLevel(INFO)
        return file_handler

    def init_app(self, app):
        file_handler = self._get_file_handler('%s/server.log' % app.config['LOG_PATH'])
        if app.debug:
            app.logger.addHandler(file_handler)

