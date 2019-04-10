import Shot
import matplotlib.pyplot as plt
import tifffile as tiff
import numpy as np
from wait_for import wait_for

if __name__ == "__main__":
    # shot = Shot.Shot('Forest', 'D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\'
    #                            'Landsat 8 OLI TIRS C1 Level-1\\2018.05.29\\'
    #                            'LC08_L1TP_176025_20180529_20180605_01_T1_MTL.txt')
    #
    # shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
    #                  '2018.05.29\\LC08_L1TP_176025_20180529_20180605_01_T1_B1.TIF', 1, 'aerosol')
    # shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
    #                  '2018.05.29\\LC08_L1TP_176025_20180529_20180605_01_T1_B2.TIF', 2, 'blue')
    # shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
    #                  '2018.05.29\\LC08_L1TP_176025_20180529_20180605_01_T1_B3.TIF', 3, 'green')
    # shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
    #                  '2018.05.29\\LC08_L1TP_176025_20180529_20180605_01_T1_B4.TIF', 4, 'red')
    # shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
    #                  '2018.05.29\\LC08_L1TP_176025_20180529_20180605_01_T1_B5.TIF', 5, 'NIR')
    # shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
    #                  '2018.05.29\\LC08_L1TP_176025_20180529_20180605_01_T1_B6.TIF', 6, 'SWIR1')
    # shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
    #                  '2018.05.29\\LC08_L1TP_176025_20180529_20180605_01_T1_B7.TIF', 7, 'SWIR2')
    #
    # shot.to_make_rgb('SWIR1', 'NIR', 'red')
    #
    # digital_hypercube = shot.to_make_hypercube()
    # spectral_brightness_hypercube = digital_hypercube.to_turn_into_radiance()
    # spectrums = Shot.SpectrumsSet('Spectra samples. Valuysky rayon. 2018.05.29', spectral_brightness_hypercube)
    # spectrums.save('Spectra samples. Valuysky rayon. 2018.05.29', 'D:\\results')
    # spectrums.to_plot()

    #ref = tiff.imread('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\2018.05.29\\LC08_L1TP_176025_20180801_20180814_01_T1.TIF')

    shot = Shot.Shot('Forest. 2018.08.08', 'D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\'
                               'Landsat 8 OLI TIRS C1 Level-1\\2018.08.08\\'
                               'LC08_L1TP_177025_20180808_20180815_01_T1_MTL.txt')

    shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
                     '2018.08.08\\LC08_L1TP_177025_20180808_20180815_01_T1_B1.TIF', 1, 'aerosol')
    shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
                     '2018.08.08\\LC08_L1TP_177025_20180808_20180815_01_T1_B2.TIF', 2, 'blue')
    shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
                     '2018.08.08\\LC08_L1TP_177025_20180808_20180815_01_T1_B3.TIF', 3, 'green')
    shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
                     '2018.08.08\\LC08_L1TP_177025_20180808_20180815_01_T1_B4.TIF', 4, 'red')
    shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
                     '2018.08.08\\LC08_L1TP_177025_20180808_20180815_01_T1_B5.TIF', 5, 'NIR')
    shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
                     '2018.08.08\\LC08_L1TP_177025_20180808_20180815_01_T1_B6.TIF', 6, 'SWIR1')
    shot.to_add_band('D:\\Изображения\\Спектральные изображения\\Валуйское лесничество\\Landsat 8 OLI TIRS C1 Level-1\\'
                     '2018.08.08\\LC08_L1TP_177025_20180808_20180815_01_T1_B7.TIF', 7, 'SWIR2')

    shot.to_make_rgb('SWIR1', 'NIR', 'red')

    digital_hypercube = shot.to_make_hypercube()
    spectral_brightness_hypercube = digital_hypercube.to_turn_into_radiance()
    spectrums = Shot.SpectrumsSet('Spectra samples. Valuysky rayon. 2018.08.08', spectral_brightness_hypercube)
    spectrums.save('Spectra samples. Valuysky rayon. 2018.08.08', 'D:\\results')
    spectrums.to_plot()
