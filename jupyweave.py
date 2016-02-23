#!/usr/bin/env python3

from sys import argv, exit
from settings import Settings
from processor import Processor


DEFAULT_CONFIG_FILE_NAME = 'defconfig.json'


class JuPyWeave:

    def __init__(self, args):
        self.arguments = args
        self.config_file, self.filenames = self.parse_args()
        self.processors = []

        if len(self.filenames) == 0:
            self.usage()

        try:
            self.settings = Settings(self.config_file)
        except FileNotFoundError:
            # TODO: validation errors?
            self.exit_error('Configuration file %s not found.' % self.config_file)

    def usage(self):
        print('Usage: %s [--config=filename] file1 [file2 ...]' % self.arguments[0])
        exit()

    @staticmethod
    def exit_error(error_msg):
        print(error_msg)
        exit()

    def parse_args(self):
        args = self.arguments[1:]
        cfg_prefix = '--config='
        filenames = []
        config = DEFAULT_CONFIG_FILE_NAME

        for arg in args:
            if arg.startswith(cfg_prefix):
                config = arg[len(cfg_prefix):]
            else:
                filenames.append(arg)

        return config, filenames

    def process(self):
        self.processors = Processor.create_processors(self.filenames, self.settings)

        for processor in self.processors:
            processor.process()


def main():
    program = JuPyWeave(argv)
    program.process()

if __name__ == '__main__':
    main()