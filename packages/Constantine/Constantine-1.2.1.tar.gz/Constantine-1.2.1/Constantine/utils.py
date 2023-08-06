import os, sys
import datetime
import string, random
import json
import re

def get_project_full_path():
    """ Return the full path of the project for navigation."""

    projectDirectory = os.path.dirname(os.path.realpath(__file__))

    return projectDirectory


def check_date_string(date):
    """ Return True if the input string is a valid YYYY-MM-DD date, False
        otherwise. """

    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return False

    return True


def read_config(config_file_path):
    """ Return the configuration value of requestedKey. """

    full_path = get_project_full_path()
    default_config_file = os.path.join(full_path, "settings.json")

    if config_file_path is None or not os.path.isfile(config_file_path):
        print("Warning: I cannot find the configuration file.")
        print("Using the default configuration file at " + str(default_config_file))
        print("Please find an example config file at Docs/settings-example.json, and use --config= to specify your config file.")
        config_file = default_config_file
    else:
        config_file = config_file_path

    try:
        with open(config_file) as SettingsFile:
            SettingsData = json.load(SettingsFile)
            if SettingsData['logo'].startswith('/'): # Absolute path.
                logo_path = SettingsData['logo']
            else:
                logo_path = full_path + "/" + SettingsData['logo']

            if not os.path.isfile(logo_path):
                raise ValueError("The logo file does not exist! If you are using Constantine installed from pip (or otherwise as a package), use absolute path like /home/user/logo.png for 'logo' in settings.json .")
            if not any([check_date_string(i) for i in SettingsData['term_start_dates']]):
                raise ValueError("Invalid date(s) found in 'term_start_dates' of settings.json!")
            return SettingsData
    except:
        print("Error reading settings.json, JSON probably not valid.")
        raise

    return False


def get_closest_date_time(current_date, date_list):
    """ Given a datetime, find the closest previous datetime in list. Adapted from:
        http://stackoverflow.com/a/17249470/846892
    """

    def func(x):
       d = datetime.datetime.strptime(x, "%Y-%m-%d")
       d = d - datetime.timedelta(days=d.weekday()) # Make sure it's a Monday.
       delta = current_date - d if d < current_date else datetime.timedelta.max
       return delta

    closest_date = min(date_list, key = func)
    closest_date = datetime.datetime.strptime(closest_date, "%Y-%m-%d")
    closest_date = closest_date - datetime.timedelta(days=closest_date.weekday())
    return datetime.datetime.strftime(closest_date, "%Y-%m-%d")


def tex_escape(text):
    """
        Adapted from http://stackoverflow.com/a/25875504
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless',
        '>': r'\textgreater',
    }
    regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key = lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], str(text))


def settings_to_formatting(settings):
    """ Given a settings dictionary, return a dictionary for formatting the
        LaTeX template except week_number, events and special text.
        Certain items needs to be split to different keys due to LaTeX
        formatting.
    """

    formatting = {}
    for key, val in settings.items():

        if key == "logo":
            if val.startswith('tex/'):
                formatting["logo_file"] = val[4:]
            else:
                formatting["logo_file"] = val
        elif key == "url":
            formatting["domain_main"] = val.rsplit('.', 1)[0]
            formatting["domain_tld"] = "." + val.rsplit('.', 1)[1]
        elif key == "email":
            formatting["email_user"] = val.rsplit('@', 1)[0]
            formatting["email_domain"] = "@" + val.rsplit('@', 1)[1]
        else:
            formatting[key] = val

    # Escape TeX special characters.
    formatting = {i:tex_escape(formatting[i]) for i in formatting}

    return formatting
