import numpy as np
import re
import tifffile as tiff
import matplotlib.pyplot as plt
from mpldatacursor import datacursor

# обазначение мультиплекативного коэффициента для перевода из цифрового значения в яркость в метаданных Landsat 8
RADIANCE_MULT_BAND_INDICATOR = 'RADIANCE_MULT_BAND'
# обазначение адитивного коэффициента для перевода из цифрового значения в яркость в метаданных Landsat 8
RADIANCE_ADD_BAND_INDICATOR = 'RADIANCE_ADD_BAND'
# обазначение высоты над горизонтом в метаданных Landsat 8
SUN_ELEVATION = 'SUN_ELEVATION'
# шаблон регулярного вырожения для числа
NUMBER_REGEX = '[+-]?[\d]+[.]?[\d]*[eE]?[-]?[\d]*'


class Shot:
    def __init__(self, metadata_file_address):
        # открытие файла с методанными по адрессу metadata_file_address для чтения
        metadata_file = open(metadata_file_address, "r")
        # чтение данных из файла методанных
        self.metadata = metadata_file.read()
        # закрытие файла с методанными
        metadata_file.close()
        self.bands_list = []
        self.rgb = None
        self.hypercube = None
        # чтение высоты Солнца над горизонтом из методанных
        regex_sun_elev = "".join([SUN_ELEVATION, ' = ', NUMBER_REGEX])
        self.solar_elevation = float(re.findall(NUMBER_REGEX, re.search(regex_sun_elev, self.metadata).group())[-1])

    def to_add_band(self, band_address, bands_number):
        """
        @Описание:
            Метод добавляет к списку спектральных каналов self.bands_list новый канал - объект Band. При создании нового
                спектрального канала в него записываются цифровые данные о спектральном канале из файла в формате tiff
                по адресу band_address. Также записывается номер канала bands_number. После для добавленного канала из
                методанных читаются мультиплекативный и адитивный коэффициенты перевода в спектральную яркость.
        :param band_address: адресс снимка цифрового спектрального канала в формате tiff, который будет записываться в
            добавляемый объект (String).
        :param bands_number: номер нового канала (номер канала Landsat 8) (int).
        :return: добавляет объект Bands к списку self.bands_list, и записывает в мультиплекативный и адитивный
            коэффициенты перевода в спектральную яркость в поля self.radiance_mult_band и self.radiance_add_band,
            соответственно, добавленного канала (объекта Band)
        """
        self.bands_list.append(Band(band_address, bands_number))
        # чтение мультиплекативного и адитивного коэффициентов перевода в спектральную яркость для добавленного канала
        self.bands_list[-1].to_parse_rad_coefs(self.metadata)

    # def to_parse_coef_for_radiance(self):
    #     """
    #     @Описание:
    #         Метод читает из self.metadata коэффициенты (мультиплекативный и адитивный) для перевода цифровых значений
    #             каждого спектрального канала из self.bands_list в спектральную яркость для спектральной полосы в этого
    #             канала (Вт / (ст * мкм)). Коэффициенты записываются в поля каждого из объектов Band из self.bands_list в
    #             поля self.radiance_mult_band и self.radiance_add_band, соответственно.
    #     :param metadata_file_address: адрес файла с методаными (String)
    #     :return: записывает коэффициенты в поля self.radiance_mult_band и self.radiance_add_band каждого из объектов
    #         Band из self.bands_list.
    #     """
    #     # поиск коэффицентов из данных metadata для каждого спектрального канала
    #     for band in self.bands_list:
    #         band.to_parse_rad_coefs(self.metadata)

    def to_make_hypercube_of_radiance(self):
        """

        :return:
        """
        # создание сиска, в который записываются канала для создания гиперкуба
        hypercube = []
        # перевод каждого цифрового канала в спектральные яркости и добавление к спику hypercube
        for band in self.bands_list:
            hypercube.append(band.to_transfer_digital_band_to_radiance())
        # перевод списка с донными о гиперкубе в массив numpy и запись его в глобальное поле self.hypercube
        self.hypercube = np.array(hypercube)

    def to_norm_hypercube(self):
        # нулевой массив, в котором будет суммироваться яркость от всех каналов для дальнейшей нормировки
        sum_hypercube = np.sum(self.hypercube, axis=0)
        sum_hypercube = np.where(sum_hypercube == 0, sum_hypercube, 1)
        self.hypercube /= sum_hypercube

    def to_make_rgb(self, red_band_num, green_band_num, blue_band_num):
        # поиск каналов для составления rgb снимка по заданным номерам
        red_band = next(band for band in self.bands_list if band.band_number == red_band_num).digital_band
        green_band = next(band for band in self.bands_list if band.band_number == green_band_num).digital_band
        blue_band = next(band for band in self.bands_list if band.band_number == blue_band_num).digital_band
        # запись rgb изображения в self.rgb
        self.rgb = np.array([red_band, green_band, blue_band])

    #def to_get_spectrum_from_hypercube(self):

class Band:
    def __init__(self, band_address, bands_number):
        self.digital_band = tiff.imread(band_address)
        self.band_number = bands_number
        self.radiance_mult_band = None
        self.radiance_add_band = None

    def to_parse_rad_coefs(self, metadata):
        """
        @Описание:
            Метод ищет в строке методанных коэффициенты (мультиплекативный и адитивный) для перевода цифровых значений
                этого спектрального канала в спектральную яркость для спектральной полосы в этого канала
                (Вт / (ст * мкм)) и записывет их в специальные поля для этих коэффициентов self.radiance_mult_band и
                self.radiance_add_band, соответственно.
        :param metadata: строка с методанными (String)
        :return: записывает в self.radiance_mult_band и self.radiance_add_band мультиплекативный и адитивный
            коэффициенты перевода, соответственно из строки metadata
        """
        # регулярное выражение для поиска мультиплекативного коэффициента для этого канала
        regex_mult = "".join([RADIANCE_MULT_BAND_INDICATOR, '_', str(self.band_number), ' = ', NUMBER_REGEX])
        # регулярное выражение для поиска адитивного коэффициента для этого канала
        regex_add = "".join([RADIANCE_ADD_BAND_INDICATOR, '_', str(self.band_number), ' = ', NUMBER_REGEX])
        # чтение мультиплекативного коэффициента из метаданных для этого канала
        self.radiance_mult_band = float(re.findall(NUMBER_REGEX, re.search(regex_mult, metadata).group())[-1])
        # чтение адитивного коэффициента из метаданных для этого канала
        self.radiance_add_band = float(re.findall(NUMBER_REGEX, re.search(regex_add, metadata).group())[-1])

    def to_transfer_digital_band_to_radiance(self):
        """

        :return:
        """
        radiance_band = self.radiance_add_band + self.radiance_mult_band * self.digital_band
        radiance_band = np.where(radiance_band >= 0, radiance_band, 0)
        return radiance_band
