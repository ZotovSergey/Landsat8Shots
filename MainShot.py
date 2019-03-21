from Shot import Shot
import matplotlib.pyplot as plt
import tifffile as tiff
import numpy as np
from wait_for import wait_for
#from mpldatacursor import datacursor

if __name__ == "__main__":
    shot = Shot('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\'
                                    'Landsat 8 OLI TIRS C1 Level-1\\2018.05.29\\'
                                    'LC08_L1TP_176025_20180529_20180605_01_T1_MTL.txt')

    shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
                     '2018.05.29\\LC08_L1TP_176025_20180529_20180605_01_T1_B1.TIF', 1)
    shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
                     '2018.05.29\\LC08_L1TP_176025_20180529_20180605_01_T1_B2.TIF', 2)
    shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
                     '2018.05.29\\LC08_L1TP_176025_20180529_20180605_01_T1_B3.TIF', 3)
    shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
                     '2018.05.29\\LC08_L1TP_176025_20180529_20180605_01_T1_B4.TIF', 4)
    shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
                     '2018.05.29\\LC08_L1TP_176025_20180529_20180605_01_T1_B5.TIF', 5)
    shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
                     '2018.05.29\\LC08_L1TP_176025_20180529_20180605_01_T1_B6.TIF', 6)
    shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
                     '2018.05.29\\LC08_L1TP_176025_20180529_20180605_01_T1_B7.TIF', 7)



    # def onButton(event):
    #     x, y = int(event.xdata), int(event.ydata)
    #     print(x, y)

    #def A():
    #    return False
    # shot.to_make_rgb(4, 5, 2)
    # tiff.imshow(shot.rgb)
    # plt.connect('key_press_event', onButton)
    # plt.show()
    # shot.to_make_hypercube_of_radiance()
    # shot.to_norm_hypercube()