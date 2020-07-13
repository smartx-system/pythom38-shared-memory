
import cv2
from SubProcess import SubProcess
import MMapFileManager
import time
import numpy as np
from multiprocessing import shared_memory


if __name__ == '__main__':

    img = cv2.imread('/home/dkdk/test.jpg')
    img2 = cv2.imread('/home/dkdk/test2.jpg')
    img_size = 720 * 1280 * 3

    shm = shared_memory.SharedMemory(name='jhpark', create=True, size=img_size)
    shm_ndarray = np.ndarray((720, 1280, 3), dtype=np.uint8, buffer=shm.buf)

    print('====', shm.name, '====')
    for i in range(10):
        t0 = time.time()
        shm_ndarray[:] = img[:]
        print('[SHARED MM] Write :', time.time() - t0)
    shm_ndarray[:] = img2[:]

    sp = SubProcess(shm.name)

    for i in range(32):
        t0 = time.time()
        sp.mmap.write_mmap(img)
        print('[MMAP FILE] Write :', time.time() - t0)

    t0 = time.time()
    sp.mmap.write_mmap(img)
    print('[MMAP FILE] Write :', time.time() - t0)

    sp.run()

    time.sleep(2)
    shm.close()
    shm.unlink()
    print('close')

