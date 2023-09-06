#!./venv/bin/python
# -*- coding: utf-8 -*-
"""
Defines Logger class
"""
# Standard library
import logging
import logging.config
import os


class Logger:
    """
    Logger Class
    """

    def __init__(self):
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(self.dir_path)))

        self._config = os.path.join(self.dir_path, 'config', 'logging.ini')

        self.log_path = os.getenv('LOG_FILE_PATH')
        self.filename = 'task_manager_api.log'

        if os.path.isfile(self._config):
            self.init_config(self._config, self.log_path, self.filename, self.root_dir)

    @staticmethod
    def init_config(config, _path, filename, root=None):
        """
        Initialise logger configuration from config file
        """
        log_file = os.path.join(root, _path, filename)
        logging.config.fileConfig(
            config, disable_existing_loggers=False, defaults={'log_file': log_file}
        )
