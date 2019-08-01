from .. import app
import logging

class Helpers:
    @staticmethod
    def get_logger():
        if app.config['DEBUG']:
            log_level = logging.DEBUG
        elif app.config['ENVIRONMENT'] == 'development':
            log_level = logging.INFO
        else:
            log_level = logging.WARNING

        log = logging.getLogger('werkzeug')
        log.setLevel(log_level)

        return log
