import re

from exceptions.snippet_errors import BeginSnippetSyntaxError, EndSnippetSyntaxError, OutputSnippetSyntaxError, \
    SettingSnippetSyntaxError
from settings.pattern import GROUP_NAME__CODE, GROUP_NAME__CODE_SETTINGS, GROUP_NAME__OUTPUT_SETTINGS, \
    GROUP_NAME__SNIPPET_CODE, GROUP_NAME__SNIPPET_OUTPUT, \
    GROUP_NAME__LANGUAGE, GROUP_NAME__ECHO, GROUP_NAME__OUTPUT, GROUP_NAME__CONTEXT, GROUP_NAME__ID
from settings.pattern import Pattern

PATTERN_CODE_SNIPPET = str.format(R'(?P<{0}>(?:.|\s)*?)', GROUP_NAME__CODE)
PATTERN_CODE_SETTINGS = str.format(R'(?P<{0}>(?:.|\s)*?)', GROUP_NAME__CODE_SETTINGS)
PATTERN_OUTPUT_SETTINGS = str.format(R'(?P<{0}>(?:.|\s)*?)', GROUP_NAME__OUTPUT_SETTINGS)

PATTERN_SETTING = R'(?P<{0}>(?:.|\s)*?)'


class Snippet:

    def __init__(self, data):
        begin_pattern = Snippet.create_begin_pattern(data)
        end_pattern = Snippet.create_end_pattern(data)
        output_pattern = Snippet.create_output_pattern(data)

        code_snippet = str.format(R'{0}{1}{2}', begin_pattern, PATTERN_CODE_SNIPPET, end_pattern)
        code_snippet = str.format(R'(?P<{0}>{1})', GROUP_NAME__SNIPPET_CODE, code_snippet)
        output_snippet = str.format(R'(?P<{0}>{1})', GROUP_NAME__SNIPPET_OUTPUT, output_pattern)

        entry_regex = str.format(R'(?:{0})|(?:{1})', code_snippet, output_snippet)
        language_regex = self.create_setting_regex(data, 'language', GROUP_NAME__LANGUAGE)
        echo_regex = self.create_setting_regex(data, 'echo', GROUP_NAME__ECHO)
        output_regex = self.create_setting_regex(data, 'output', GROUP_NAME__OUTPUT)
        context_regex = self.create_setting_regex(data, 'context', GROUP_NAME__CONTEXT)
        id_regex = self.create_setting_regex(data, 'snippet_id', GROUP_NAME__ID)

        self.regex_patterns = Pattern(entry_regex, language_regex, echo_regex, output_regex, context_regex, id_regex)

    @staticmethod
    def create_setting_regex(data, name, group_name):
        setting_pattern = data['patterns'][name]
        setting_regex = data['settings'][name]

        if setting_pattern not in setting_regex:
            raise SettingSnippetSyntaxError(name, setting_pattern)

        setting_pattern = re.escape(re.escape(setting_pattern))
        setting_regex = re.escape(setting_regex)

        setting_group = str.format(PATTERN_SETTING, group_name)
        setting_regex = re.sub(setting_pattern, setting_group, setting_regex, 1)

        return setting_regex

    @staticmethod
    def create_begin_pattern(data):
        patterns = data['patterns']
        settings_pattern = patterns['settings']

        if settings_pattern not in data['begin']:
            raise BeginSnippetSyntaxError(settings_pattern)

        settings_pattern = re.escape(re.escape(settings_pattern))

        snippet_pattern = re.escape(data['begin'])
        snippet_pattern = re.sub(settings_pattern, PATTERN_CODE_SETTINGS, snippet_pattern, 1)

        return snippet_pattern

    @staticmethod
    def create_end_pattern(data):
        patterns = data['patterns']

        if patterns['settings'] in data['end']:
            raise EndSnippetSyntaxError(patterns['settings'])

        return re.escape(data['end'])

    @staticmethod
    def create_output_pattern(data):
        patterns = data['patterns']
        settings_pattern = patterns['settings']

        if settings_pattern not in data['output']:
            raise OutputSnippetSyntaxError(settings_pattern)

        settings_pattern = re.escape(re.escape(settings_pattern))

        snippet_pattern = re.escape(data['output'])
        snippet_pattern = re.sub(settings_pattern, PATTERN_OUTPUT_SETTINGS, snippet_pattern, 1)

        return snippet_pattern

    def pattern(self):
        return self.regex_patterns