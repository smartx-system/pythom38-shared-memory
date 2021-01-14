
import multiprocessing
import time
import numpy as np
import Utils as utils
import cv2

from MMapFileManager import MMapFileManager
from SharedMemoryManager import SharedMemoryManager
from multiprocessing import shared_memory
from PIL import Image


class SubProcess(multiprocessing.Process):

    def __init__(self):
        super().__init__()

        ini = utils.get_ini_parameters('./config.ini')
        self.mmap = MMapFileManager()
        self.mmap.init_mmap_files('/dev/shm/', ini['MMAP'], 'mmap')

        self.shm = SharedMemoryManager()
        self.shm.init_shm_files(ini['SHM'])

        self.shape = (int(ini['MMAP']['mmap_height']), int(ini['MMAP']['mmap_width']), 3)
    
        self.img = cv2.imread('/home/minds/1920_1080.jpg')

    def add_text(self, image, text):
        x1, y1 = 30, 30
        ret = cv2.putText(image,
                          text=text,
                          org=(x1, y1), 
                          fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                          fontScale=1, 
                          color=(255, 255, 255), 
                          thickness=2)
        return ret

    def run(self):
        while True:

            for i in range(100):
                temp_image = self.img.copy()
                temp_image = self.add_text(temp_image, str(i))

                t0 = time.time()
                self.mmap.write_mmap(temp_image)
                print("[MMAP FILE] Write :", time.time() - t0)

            for i in range(100000):

                temp_image = self.img.copy()
                temp_image = self.add_text(temp_image, str(i))

                shm_name = "shm_avr_test0"
                print(shm_name)

                t0 = time.time()
                ret = self.shm.write_shm(temp_image)
                print("[SHM MODUL] Write :", time.time() - t0)

            return

    def unlink(self):
        print('unlink')
        self.shm.unlink()

