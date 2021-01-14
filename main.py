
import numpy as np
import os
import cv2
import Utils as utils
import time

from SubProcess import SubProcess
from MMapFileManager import MMapFileManager
from multiprocessing import shared_memory
from SharedMemoryManager import SharedMemoryManager
from PIL import Image


if __name__ == '__main__':

    # sub process
    sp = SubProcess()
    sp.run()
        
    # ini
    ini = utils.get_ini_parameters('./config.ini')

    # mmap
    mmap = MMapFileManager()
    mmap.init_mmap_files('./', ini['MMAP'], 'mmap')

    # shm
    shm = SharedMemoryManager()
    shm.init_shm_files(ini['SHM'])

    # shape
    shape = (int(ini['MMAP']['mmap_height']), int(ini['MMAP']['mmap_width']), 3)

    """
    # mmap
    for i in range(1):

        t0 = time.time()

        # Read
        data = mmap.read_mmap('./mmap/mmap/test.mmap_00.mmap', shape)
        print(data)
        print('[MMAP FILE] Read :', time.time() - t0)

        # Save
        im = Image.fromarray(data)
        im.save('./mmap_{}.png'.format(i))

    # shm
    for i in range(1):

        shm_name = "shm_avr_test{}".format(i % 8)
        print(shm_name)

        t0 = time.time()

        # Read
        s = shm.read_shm(shm_name=shm_name, shape=shape)
        data = np.ndarray(shape, dtype=np.uint8, buffer=s.buf)
        print("[SHM MODUL] Read :", time.time() - t0)

        # Save
        im = Image.fromarray(data)
        im.save('./shm_{}.png'.format(i))

    """

    time.sleep(2)
    sp.unlink()
    print('close')
    exit()

