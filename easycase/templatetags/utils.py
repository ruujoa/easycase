from django.template import Library
import ConfigParser

register = Library()

def get_limit(user):
    config = ConfigParser.ConfigParser()
    config.read(user.get_username() + ".profile")
    limit = config.get("system", "rows_per_page")
    return limit

limit = register.simple_tag(get_limit)