
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


def test_main():

    # sub process (Write process)
    sp = SubProcess()
    sp.start()
    time.sleep(1)

    # mmap
    # INFO : Do not initialize by ini. When you are only reading, just read
    mmap = MMapFileManager()

    # shm
    # INFO : Do not initialize by ini. When you are only reading, just read
    shm = SharedMemoryManager()

    # shape
    ini = utils.get_ini_parameters('./config.ini')
    shape = (int(ini['MMAP']['mmap_height']), int(ini['MMAP']['mmap_width']), 3)

    # mmap
    for i in range(4):

        mmap_name = './mmap/mmap/test.mmap_00.mmap'

        # Read
        t0 = time.time()
        data = mmap.read_mmap(mmap_name, shape)
        print('[MMAP FILE] Read :', time.time() - t0)

        # Save
        im = Image.fromarray(data)
        im.save('./test/mmap_result.png')

    # shm
    for i in range(4):

        shm_name = 'shm_avr_test0'

        # Read
        t0 = time.time()
        s = shm.read_shm(shm_name=shm_name, shape=shape)
        data = np.ndarray(shape, dtype=np.uint8, buffer=s.buf)
        print("[SHM MODUL] Read :", time.time() - t0)

        # Save
        im = Image.fromarray(data)
        im.save('./test/shm_result.png')

    time.sleep(2)
    print('=== Exit ===')
    sp.unlink()

    # Test mmap
    answer = cv2.imread('./test/mmap_answer.png')
    result = cv2.imread('./test/mmap_result.png')
    assert np.array_equal(answer, result)

    # Test shm
    answer = cv2.imread('./test/shm_answer.png')
    result = cv2.imread('./test/shm_result.png')
    assert np.array_equal(answer, result)


if __name__ == '__main__':
    test_main()

