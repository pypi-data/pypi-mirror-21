from __future__ import print_function, division

# Local import
from time_base import comparison_timer

real_re = '''\
import re
real_regex = re.compile(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?$')
real_match = real_regex.match
int_regex = re.compile(r'[-+]?\d+$')
int_match = int_regex.match
def real_re(x):
    """Function to simulate safe_real but with regular expressions."""
    try:
        if int_match(x):
            return int(x)
        elif real_match(x):
            return float(x)
        else:
            return x
    except TypeError:
        if type(x) in set([float, int]):
            return x
        else:
            raise TypeError
'''

real_try = '''\
def real_try(x):
    """Function to simulate safe_real but with try/except."""
    try:
        a = float(x)
    except ValueError:
        return x
    else:
        b = int(a)
        return b if a == b else b
'''

comparison_timer(['real_re', real_re],
                 ['real_try', real_try],
                 ['fast_real', 'from fastnumbers import fast_real'])
