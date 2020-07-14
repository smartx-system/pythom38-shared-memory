
import os
import sys
import configparser
import traceback

def file_exists(filename, print_=False, exit_=False):
    """
    Check if a file exists or not.
    :param filename:
    :param print_:
    :param exit_:
    :return True/False:
    """
    if not os.path.isfile(filename):
        if print_ or exit_:
            print("\n @ Warning: file not found, {}.\n".format(filename))
            print(traceback.print_stack())
        if exit_:
            sys.exit()
        return False
    else:
        return True


def remove_comments_in_ini(ini, cmt_delimiter='###'):
    """
    Remove comments in ini file,
    where comment is text strings rting with comment delimiter.
    :param ini:
    :param cmt_delimiter:
    :return:
    """
    for section in ini.sections():
        for key in ini[section]:
            ini[section][key] = ini[section][key].split(cmt_delimiter)[0].strip()
    return ini

def folder_exists(in_dir, exit_=False, create_=False, print_=False):
    """
    Check if a directory exists or not. If not, create it according to input argument.
    :param in_dir:
    :param exit_:
    :param create_:
    :param print_:
    :return:
    """
    if not in_dir:
        return

    if os.path.isdir(in_dir):
        if print_:
            print(" # Info: directory, {}, already existed.".format(in_dir))
        return True
    else:
        if create_:
            try:
                os.makedirs(in_dir)
            except all:
                print(" @ Error: make_dirs in check_directory_existence routine...\n")
                sys.exit()
        else:
            if print_:
                print("\n @ Warning: directory not found, {}.\n".format(in_dir))
            if exit_:
                sys.exit()
        return False

def get_ini_parameters(ini_fname, cmt_delimiter="###"):
    ini = configparser.ConfigParser()
    file_exists(ini_fname, exit_=True)
    ini.read(ini_fname, encoding='utf-8')
    return remove_comments_in_ini(ini, cmt_delimiter=cmt_delimiter)