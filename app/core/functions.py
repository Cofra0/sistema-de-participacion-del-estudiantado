# core/functions.py

import os

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name, default=None):
    try:
        var = os.environ[var_name]
        if var.lower() == "true":
            return True
        elif var.lower() == "false":
            return False
        return var
    except KeyError:
        if default:
            return default
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)
