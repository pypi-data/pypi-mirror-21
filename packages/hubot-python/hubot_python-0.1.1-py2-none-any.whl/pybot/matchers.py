import re


class Matcher(object):
    def match(self, message):
        pass


class RegexMatcher(Matcher):
    def __init__(self, pattern):
        self.regex = re.compile(pattern)

    def match(self, message):
        if message.text:
            return self.regex.search(message.text)


class RobotNameMatcher(Matcher):
    def __init__(self, wrapped, robot):
        self.wrapped = wrapped
        self.robot = robot

    def match(self, message):
        if not message.text:
            return

        tokens = message.text.lower().split(' ')
        if not tokens:
            return

        name = self.robot.name.lower()
        first_token = tokens[0].lstrip(' @').rstrip(' :-=')

        if first_token == name:
            return self.wrapped.match(message)
