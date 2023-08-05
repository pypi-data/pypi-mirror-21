import logging as log
import yaml
from conf import Config
from test import Test


class Parser:
    """
    Parser parses the file, url and stores tests.
    """
    def __init__(self, file, url_prefix):
        # Load the file and read the config
        try:
            with open(file, 'r') as fl:
                self.yam = yaml.load(fl.read())
                self.tests = None
                self.config = None
            if not (url_prefix.startswith("http://")
                    or url_prefix.startswith("https://")):
                url_prefix = "http://"+url_prefix
            self.url_prefix = url_prefix
        except BaseException as ex:
            log.error(ex.message)
            log.exception(ex)
            raise Exception("Error Parsing YAML File")

    def get_config(self):
        if self.config is None:
            for prop in self.yam:
                if 'config' in prop:
                    self.config = Config(prop['config'])
        return self.config

    def get_tests(self):
        if self.tests is None:
            tests = []
            try:
                for prop in self.yam:
                    if 'test' in prop:
                        tests.append(Test(prop['test'], self.url_prefix))
                return tests
            except BaseException as ex:
                log.error(ex.message)
                log.exception(ex)
                raise Exception("Error getting list of test cases")
        return self.tests
