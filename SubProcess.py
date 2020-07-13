
import multiprocessing
from MMapFileManager import MMapFileManager
from multiprocessing import shared_memory
from PIL import Image

import configparser
import sys
import os
import time
import numpy as np


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


def get_ini_parameters(ini_fname, cmt_delimiter="###"):
    ini = configparser.ConfigParser()
    file_exists(ini_fname, exit_=True)
    ini.read(ini_fname, encoding='utf-8')
    return remove_comments_in_ini(ini, cmt_delimiter=cmt_delimiter)

class SubProcess(multiprocessing.Process):

    def __init__(self, shm_name):
        self.shm_name = shm_name

        ini = get_ini_parameters('./config.ini')
        self.mmap = MMapFileManager()
        self.mmap.init_mmap_files('./', ini['MMAP'], 'mmap', (720, 1280, 3))


    def run(self):

        while True:
            existing_shm = shared_memory.SharedMemory(name=self.shm_name)

            for i in range(10):
                t0 = time.time()
                c = np.ndarray((720, 1280, 3), dtype=np.uint8, buffer=existing_shm.buf)
                print("[SHARED MM] Read :", time.time() - t0)

            for i in range(10):
                t0 = time.time()
                data = self.mmap.read_mmap('./mmap/mmap/test.mmap_00.mmap', (720, 1280, 3))
                print("[MMAP FILE] Read :", time.time() - t0)

            im = Image.fromarray(c)
            im.save('./test.png')

            return

