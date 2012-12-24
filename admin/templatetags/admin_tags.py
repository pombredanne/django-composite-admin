import re

from django.template import Library
from django.conf import settings
from django.core.urlresolvers import reverse


register = Library()


@register.simple_tag
def url(*args):
    name = ':'.join(args)
    return reverse(name)


numeric_test = re.compile("^\d+$")


def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""

    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value in arg:
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return settings.TEMPLATE_STRING_IF_INVALID

register.filter('getattribute', getattribute)
