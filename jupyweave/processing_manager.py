from importlib import import_module


class ProcessingManager:
    """Responsible for loading processors and passing control to them"""

    def __init__(self, document_language, snippet_language, snippet_settings, user_processor_name, output_manager,
                 executor, image_settings):
        """Initialization"""
        package_name = str.format('jupyweave.processors.{0}_processor', document_language.lower())

        if user_processor_name is not None:
            package_name = str.format('jupyweave.processors.{0}_{1}_processor', user_processor_name, document_language.lower())
            module = import_module(package_name)
            self.__processor = getattr(module, 'Processor')(output_manager, executor, snippet_language, snippet_settings,
                                                            image_settings)
        else:
            try:
                module = import_module(package_name)
                self.__processor = getattr(module, 'Processor')(output_manager, executor, snippet_language,
                                                                snippet_settings, image_settings)
            except (ImportError, AttributeError):
                module = import_module('jupyweave.processors.processor')
                self.__processor = getattr(module, 'Processor')(output_manager, executor, snippet_language,
                                                                snippet_settings, image_settings)

    def code(self, code):
        """Processing source code"""
        return self.__processor.source(code)

    def text(self, text):
        """Processing text results"""
        return self.__processor.text(text)

    def image(self, data, mime_type):
        """Processing images"""
        return self.__processor.image(data, mime_type)

    def result(self, text):
        """Processing whole result"""
        return self.__processor.result(text)

    def execute_before(self):
        """Executing user-defined code before snippet code"""
        return self.__processor.begin()

    def execute_after(self):
        """Executing user-defined code after snippet code"""
        return self.__processor.end()