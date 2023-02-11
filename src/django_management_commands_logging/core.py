from logging import Formatter, StreamHandler, getLogger

from django.core.management.base import BaseCommand


class LoggingBaseCommand(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = getLogger(self.__module__)

    def add_arguments(self, parser):
        parser.add_argument(
            '--log-level',
            dest='log_level',
            default='info',
            choices={'debug', 'info', 'warning', 'error', 'critical'}
        )
        
    def handle(self, *args, **options):
        self.logger.setLevel(options['log_level'].upper())
        handler = StreamHandler()
        handler.setFormatter(
            Formatter(
                '%(asctime)s:%(levelname)s:%(name)s:%(message)s',
                datefmt='%Y-%m-%dT%H:%M:%S%z')
        )
        self.logger.addHandler(handler)
        return self.logger

def enable_logging(function):
    def wrapper(self, *args, **kwargs):
        mapper = {
            'handle': LoggingBaseCommand().handle,
            'add_arguments': LoggingBaseCommand().add_arguments
        }
        
        self.logger = mapper[function.__name__](*args, **kwargs)
    
        return function(self, *args, **kwargs)
    return wrapper
