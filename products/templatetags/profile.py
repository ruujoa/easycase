from django import template
from django.template import Library
import ConfigParser
from ConfigParser import NoSectionError

register = Library()

def get_limit(parser, token):
    try:
        tag_name, username = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly one argument" % token.contents.split()[0])
    return LimitNode(username)

def get_timeout(parser, token):
    try:
        tag_name, username = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly one argument" % token.contents.split()[0])
    return TimeoutNode(username)

class LimitNode(template.Node):
    def __init__(self, username):
        self.username = template.Variable(username)
        
    def render(self, context):
        try:
            actual_username = self.username.resolve(context)
            config = ConfigParser.ConfigParser()
            config.read(actual_username + ".profile")
            if config.has_section("system"):
                limit = config.get("system", "rows_per_page")
                return limit
            else:
                config.add_section("system")
                config.set("system", "rows_per_page", "3")
                config.set("system", "session_timeout", "1440")
                config.write(open(actual_username + ".profile", 'wb'))
                return '3'
        except template.VariableDoesNotExist:
            return ''
        
class TimeoutNode(template.Node):
    def __init__(self, username):
        self.username = template.Variable(username)
        
    def render(self, context):
        try:
            actual_username = self.username.resolve(context)
            config = ConfigParser.ConfigParser()
            config.read(actual_username + ".profile")
            if config.has_section("system"):
                timeout = config.get("system", "session_timeout")
                return timeout
            else:
                config.add_section("system")
                config.set("system", "rows_per_page", "3")
                config.set("system", "session_timeout", "1440")
                config.write(open(actual_username + ".profile", 'wb'))
                return '1440'
        except template.VariableDoesNotExist:
            return ''

register.tag('limit', get_limit)
register.tag('timeout', get_timeout)