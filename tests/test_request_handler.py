import os
import sys
import types
import importlib.util

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Provide a minimal bs4 module if not installed
if 'bs4' not in sys.modules:
    bs4_stub = types.ModuleType('bs4')
    class BeautifulSoup:  # type: ignore
        pass
    bs4_stub.BeautifulSoup = BeautifulSoup
    sys.modules['bs4'] = bs4_stub

if 'cleo' not in sys.modules:
    cleo = types.ModuleType('cleo')
    sys.modules['cleo'] = cleo
if 'cleo.exceptions' not in sys.modules:
    cleo_exceptions = types.ModuleType('cleo.exceptions')
    class CleoValueError(Exception):
        pass
    cleo_exceptions.CleoValueError = CleoValueError
    sys.modules['cleo.exceptions'] = cleo_exceptions
if 'cleo.formatters.style' not in sys.modules:
    cleo_formatters_style = types.ModuleType('cleo.formatters.style')
    class Style:
        def __init__(self, *args, **kwargs):
            pass
    cleo_formatters_style.Style = Style
    sys.modules['cleo.formatters.style'] = cleo_formatters_style
if 'cleo.formatters.style_stack' not in sys.modules:
    cleo_formatters_style_stack = types.ModuleType('cleo.formatters.style_stack')
    class StyleStack:
        def __init__(self):
            self.stack = []
        def push(self, style):
            self.stack.append(style)
        def pop(self):
            if self.stack:
                self.stack.pop()
    cleo_formatters_style_stack.StyleStack = StyleStack
    sys.modules['cleo.formatters.style_stack'] = cleo_formatters_style_stack

streamseeker_pkg = types.ModuleType('streamseeker')
api_pkg = types.ModuleType('streamseeker.api')
core_pkg = types.ModuleType('streamseeker.api.core')
sys.modules.setdefault('streamseeker', streamseeker_pkg)
sys.modules.setdefault('streamseeker.api', api_pkg)
sys.modules.setdefault('streamseeker.api.core', core_pkg)

logger_mod = types.ModuleType('streamseeker.api.core.logger')
class Logger:
    def instance(self):
        class _Logger:
            def error(self, *args, **kwargs):
                pass
            def debug(self, *args, **kwargs):
                pass
        return _Logger()
logger_mod.Logger = Logger
sys.modules['streamseeker.api.core.logger'] = logger_mod

spec = importlib.util.spec_from_file_location(
    'streamseeker.api.core.request_handler',
    os.path.join(os.path.dirname(__file__), '..', 'src', 'streamseeker', 'api', 'core', 'request_handler.py')
)
request_handler = importlib.util.module_from_spec(spec)
sys.modules['streamseeker.api.core.request_handler'] = request_handler
spec.loader.exec_module(request_handler)
RequestHandler = request_handler.RequestHandler


def test_get_header_contains_referer_and_user_agent():
    handler = RequestHandler()
    headers = handler.get_header("https://example.com/page")
    assert headers.get("Referer") == "https://example.com"
    assert "User-Agent" in headers
    assert headers["User-Agent"]
