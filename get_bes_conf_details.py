import configparser
import os

# got this piece of code from besapi code from @JGStew
def get_bes_conn_using_config_file(conf_file=None):
    """
    read connection values from config file
    return besapi connection
    """
    config_paths = [
        "/etc/besapi.conf",
        os.path.expanduser("~/besapi.conf"),
        os.path.expanduser("~/.besapi.conf"),
        "besapi.conf",
    ]
    # if conf_file specified, then only use that:
    if conf_file:
        config_paths = [conf_file]

    configparser_instance = configparser.ConfigParser()

    found_config_files = configparser_instance.read(config_paths)

    if found_config_files and configparser_instance:
        print("Attempting BESAPI Connection using config file:", found_config_files)
        try:
            BES_ROOT_SERVER = configparser_instance.get("besapi", "BES_ROOT_SERVER")
        except BaseException:  # pylint: disable=broad-except
            BES_ROOT_SERVER = None

        try:
            BES_USER_NAME = configparser_instance.get("besapi", "BES_USER_NAME")
        except BaseException:  # pylint: disable=broad-except
            BES_USER_NAME = None

        try:
            BES_PASSWORD = configparser_instance.get("besapi", "BES_PASSWORD")
        except BaseException:  # pylint: disable=broad-except
            BES_PASSWORD = None
        if BES_ROOT_SERVER and BES_USER_NAME and BES_PASSWORD:
            return(BES_USER_NAME, BES_PASSWORD, BES_ROOT_SERVER)
        