# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""

from minghu6.etc.version import iswin
__all__ = ['get_env_var_sep']
def get_env_var_sep():

    if iswin():
        return ';'
    else:
        return ':' # Linux, Unix, OS X
