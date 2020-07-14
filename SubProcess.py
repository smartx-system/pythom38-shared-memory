
import multiprocessing
from MMapFileManager import MMapFileManager
from SharedMemoryManager import SharedMemoryManager
from multiprocessing import shared_memory
from PIL import Image

import time
import numpy as np
import Utils as utils


class SubProcess(multiprocessing.Process):

    def __init__(self):
        super().__init__()

        ini = utils.get_ini_parameters('./config.ini')
        self.mmap = MMapFileManager()
        self.mmap.init_mmap_files('./', ini['MMAP'], 'mmap')

        self.shm = SharedMemoryManager()
        self.shm.init_shm_files(ini['SHM'])

        self.shape = (int(ini['MMAP']['mmap_height']), int(ini['MMAP']['mmap_width']), 3)

    def run(self):
        while True:

            for i in range(16):
                t0 = time.time()
                data = self.mmap.read_mmap('./mmap/mmap/test.mmap_00.mmap', self.shape)
                print("[MMAP FILE] Read :", time.time() - t0)

            im = Image.fromarray(data)
            im.save('./test.png')

            for i in range(16):
                t0 = time.time()
                data = self.shm.read_shm(index=i)
                print("[SHM MODUL] Read :", time.time() - t0)

            im = Image.fromarray(data)
            im.save('./test2.png')


            return

    def unlink(self):
        self.shm.unlink()
