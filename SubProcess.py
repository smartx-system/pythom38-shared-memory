
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

        # Init ini
        ini = utils.get_ini_parameters('./config.ini')

        # mmap
        self.mmap = MMapFileManager()
        self.mmap.init_mmap_files('./', ini['MMAP'], 'mmap')

        # shm
        self.shm = SharedMemoryManager()
        self.shm.init_shm_files(ini['SHM'])

        # etc
        self.shape = (int(ini['MMAP']['mmap_height']), int(ini['MMAP']['mmap_width']), 3)
        self.img = cv2.imread('./test/input_1920_1080.jpg')

    def add_text(self, image, text: str):
        """
        Add text for debug...
        """
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
            for i in range(4):
                temp_image = self.img.copy()
                temp_image = self.add_text(temp_image, str(i))
                cv2.imwrite('./test/mmap_answer.png', temp_image)

                # Write
                t0 = time.time()
                self.mmap.write_mmap(temp_image[:,:,::-1])
                print("[MMAP FILE] Write :", time.time() - t0)

            for i in range(4):

                temp_image = self.img.copy()
                temp_image = self.add_text(temp_image, str(i))
                cv2.imwrite('./test/shm_answer.png', temp_image)

                shm_name = "shm_avr_test0"

                # Write
                t0 = time.time()
                ret = self.shm.write_shm(temp_image[:,:,::-1])
                print("[SHM MODUL] Write :", time.time() - t0)

            return

    def unlink(self):
        print('unlink')
        self.shm.unlink()

