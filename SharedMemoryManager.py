#! /usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import shared_memory
import os
import numpy as np
import Utils as utils
import time


class SharedMemoryManager:
    def __init__(self):

        self.shm_shape = None
        self.shm_arr = None
        self.shm_file_num = None
        self.shm_idx = None
        self._shm_last_frame = None
        self.prefix = None
        self.shm_test = None

    def init_shm_files(self, shm_ini, shm_shape=None):

        self.shm_idx = 0
        self.shm_file_num = int(shm_ini['shm_file_num'])
        self.prefix = shm_ini['shm_file_prefix']

        if shm_shape:
            self.shm_shape = shm_shape
        else:
            shm_width = int(shm_ini['shm_width'])
            shm_height = int(shm_ini['shm_height'])

            self.shm_shape = (shm_height, shm_width, 3)

        self.shm_arr = []
        for i in range(self.shm_file_num):

            shm_name = self.prefix + str(i)
            shm_path = os.path.join('/dev/shm/', shm_name)

            if utils.file_exists(shm_path):
                os.remove(shm_path)

            shm_size = self.shm_shape[0] * self.shm_shape[1] * self.shm_shape[2]
            shm = shared_memory.SharedMemory(name=shm_name, create=True, size=shm_size)
            # shm = np.ndarray(self.shm_shape, dtype=np.uint8, buffer=shm.buf)
            self.shm_arr.append(shm)

    def check_init_shm(self, shm_ini, shm_shape):
        if self.shm_arr and self.shm_shape == shm_shape:
            return

        self.init_shm_files(shm_ini, shm_shape)

    def write_shm(self, frame):
        shm_mem = np.ndarray(self.shm_shape, dtype=np.uint8, buffer=self.shm_arr[self.shm_idx].buf)
        shm_mem[:] = frame[:]

        self._shm_last_frame = self.shm_arr[self.shm_idx]
        self.shm_idx = (self.shm_idx + 1) % self.shm_file_num

    def get_last_frame(self):
        return self._shm_last_frame

    @staticmethod
    def read_shm(shm_name, shape):
        existing_shm = shared_memory.SharedMemory(name=shm_name)
        ret = np.ndarray(shape, dtype=np.uint8, buffer=existing_shm.buf)
        return ret

    def read_shm(self, index=-1):

        if index == -1:
            index = self.shm_idx
        index = index % self.shm_file_num

        ret = np.ndarray(self.shm_shape, dtype=np.uint8, buffer=self.shm_arr[index].buf)

        self._shm_last_frame = self.shm_arr[index]
        self.shm_idx = (index + 1) % self.shm_file_num

        return ret

    def unlink(self):
        for shm in self.shm_arr:
            shm.close()
            shm.unlink()
