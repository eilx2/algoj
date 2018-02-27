from django import template
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


register = template.Library()

def parse_string(s):
	s=s.replace('\\r\\n','\n')
	s=s.replace('\\n','\n')
	return s
	
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def format_code(source):
	return highlight(parse_string(source),PythonLexer(),HtmlFormatter())