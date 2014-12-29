import re
from pylint.interfaces import IRawChecker
from pylint.checkers import BaseChecker

class DisallowedFunctionChecker(BaseChecker):
    """cheap check for gc.collect() and other functions that should BBF interfaces instead."""
    __implements__ = IRawChecker

    name = 'disallowed_func'
    msgs = {'W9910': ('gc.collect() replaced by base.gc_collect().',
                      'base-gc-collect',
                      'please use base.gc_collect() instead of gc.collect().'),
            'W9911': ('datetime.strptime replaced by base.strptime().',
                      'base-strptime',
                      'please use base.strptime instead for dates'),
            'W9912': ('Order.all() replaced by order.get_order_history().', 
                      'get-order-history',
                      'please use order.get_order_history() for order stats'),
            'W9913': ('if not ... disallowed', 
                      'if-not-foo',
                      'please use "if foo is None" instead.')
            }
    options = ()

    def process_module(self, node):
        stream = node.file_stream
        stream.seek(0)
        for (lineno, line) in enumerate(stream):
            if line.find("gc.collect(") >= 0:
                self.add_message('W9910', line=lineno+1)

            # BBF specific rule to force people to use our new/improved strptime
            #if line.find("datetime.datetime.strptime(") >= 0:
            #    self.add_message('W9911', line=lineno+1)

            # BBF specific rule to stop people from scanning the Orders
            # table directly - instead go through an API
            #if line.find("Order.all()") >= 0 and line.find('W9912') == -1:
            #    self.add_message('W9912', line=lineno+1)

            # awesome pylint rule to thwart bugs created by
            #   if not <varname>:
            # which triggers if varname is (e.g.) the empty string!!!
            #if re.search(r'^\s*if +not +[a-zA-Z0-9_]+[: ]+', line) and line.find('W9913') == -1:
            #    self.add_message('W9913', line=lineno+1)

def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(DisallowedFunctionChecker(linter))
