
import cv2
from SubProcess import SubProcess
import MMapFileManager
import time
import numpy as np
from multiprocessing import shared_memory
import os
import Utils as utils


if __name__ == '__main__':

    img = cv2.imread('/home/dkdk/1920_1080.jpg')
    img2 = cv2.imread('/home/dkdk/1920_1080_2.jpg')
    img_size = 1080 * 1920 * 3

    sp = SubProcess()

    for i in range(16):
        t0 = time.time()
        sp.mmap.write_mmap(img)
        print('[MMAP FILE] Write :', time.time() - t0)

    for i in range(16):
        t0 = time.time()
        sp.shm.write_shm(img2)
        print("[SHM MODUL] Write :", time.time() - t0)

    sp.run()

    time.sleep(2)
    sp.unlink()
    print('close')

