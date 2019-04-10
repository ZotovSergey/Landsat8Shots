import numpy as np
import re
import pickle
import tifffile as tiff
import matplotlib.pyplot as plt

# верхние границы длин волн каждого канала Landsat 8 в нм. Позиция в списке соответствуют номеру канала в Landsat 8 - 1
UPPER_BAND_WAVELENGTH = [0.451, 0.512, 0.590, 0.673, 0.879, 1.651, 2.294]
# нижние границы длин волн каждого канала Landsat 8 в нм. Позиция в списке соответствуют номеру канала в Landsat 8 - 1
LOWER_BAND_WAVELENGTH = [0.435, 0.452, 0.533, 0.636, 0.851, 1.566, 2.107]
# обазначение мультиплекативного коэффициента для перевода из цифрового значения в яркость в метаданных Landsat 8
RADIANCE_MULT_BAND_INDICATOR = 'RADIANCE_MULT_BAND'
# обазначение адитивного коэффициента для перевода из цифрового значения в яркость в метаданных Landsat 8
RADIANCE_ADD_BAND_INDICATOR = 'RADIANCE_ADD_BAND'
# обазначение высоты над горизонтом в метаданных Landsat 8
SUN_ELEVATION = 'SUN_ELEVATION'
# шаблон регулярного вырожения для числа
NUMBER_REGEX = '[+-]?[\d]+[.]?[\d]*[eE]?[-]?[\d]*'
# обозначение единиц измерения данных:
# цифровые данные
DIGITAL_UNIT = 'unit16'
# спектральныя яркость
SPECTRAL_BRIGHTNESS_UNIT = '\\frac{W}{m ^ 2 * sr * µm}' # В TeX
# относительная величина
RELATIVE_UNIT = '1'


class Shot:
    def __init__(self, name, metadata_file_address):
        self.name = name
        # открытие файла с методанными по адрессу metadata_file_address для чтения
        metadata_file = open(metadata_file_address, "r")
        # чтение данных из файла методанных
        self.metadata = metadata_file.read()
        # закрытие файла с методанными
        metadata_file.close()
        self.bands_dict = {}
        self.rgb = None
        #self.hypercube = None
        # чтение высоты Солнца над горизонтом из методанных
        regex_sun_elev = "".join([SUN_ELEVATION, ' = ', NUMBER_REGEX])
        self.solar_elevation = float(re.findall(NUMBER_REGEX, re.search(regex_sun_elev, self.metadata).group())[-1])

    def to_add_band(self, band_address, band_number, bands_key):
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
        band = Band(band_address, band_number)
        # чтение мультиплекативного и адитивного коэффициентов перевода в спектральную яркость для добавленного канала
        band.to_parse_rad_coefs(self.metadata)
        self.bands_dict.update({bands_key : band})

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

    def to_make_hypercube(self, bands_keys=None):
        """

        :return:
        """
        # если список ключей не задан, то гиперкуб создается из всех имеющихся каналов в том порядке, в котором они
        #   добавлялись
        if bands_keys is None:
            bands_keys = list(self.bands_dict.keys())
        # создание списка, в который записываются канала для создания гиперкуба
        hypercube_value = []
        # добавление к гиперкубу цифровые данные из каналов по ключам из band_keys в том порядке, в котором расположены
        #   ключи
        for band_key in bands_keys:
            hypercube_value.append(self.bands_dict.setdefault(band_key).digital_band)
        return Hypercube(np.array(hypercube_value), bands_keys, DIGITAL_UNIT, self)

    # def to_turn_hypercube_into_radiance(self, hypercube):
    #     """
    #
    #     :param hypercube:
    #     :return:
    #     """
    #     # создание пустого списка для мултиплекативных коэффициентов перевода цифровых значений в спектральные яркости
    #     mult_coef = []
    #     # создание пустого списка для адитивных коэффициентов перевода цифровых значений в спектральные яркости
    #     add_coef = []
    #     # заполнение списков mult_coef и add_coef в соответствии списку ключей для гиперкуба
    #     for band_key in hypercube.bands_keys:
    #         mult_coef.append(self.bands_dict.setdefault(band_key).radiance_mult_band)
    #         add_coef.append(self.bands_dict.setdefault(band_key).radiance_add_band)
    #     # перевод цифровых значений гиперкуба в спектральную яркость
    #     radiance_hypercube = np.array([mult_coef[i] * hypercube.values[i] +
    #                                    add_coef[i] for i in range(0, len(hypercube.bands_keys))])
    #     return Hypercube(radiance_hypercube, hypercube.bands_keys, SPECTRAL_BRIGHTNESS_UNIT)

    def to_make_rgb(self, red_band_key, green_band_key, blue_band_key):
        # поиск каналов для составления rgb снимка по заданным ключам
        red_band = self.bands_dict.setdefault(red_band_key).digital_band
        green_band = self.bands_dict.setdefault(green_band_key).digital_band
        blue_band = self.bands_dict.setdefault(blue_band_key).digital_band
        # запись rgb изображения в self.rgb
        self.rgb = np.array([red_band, green_band, blue_band])

    # def to_get_spectrums_from_hypercube(self, spectrums_sets_name, hypercube):
    #     # словарь, в который будут записываться спектры
    #     spectrum_dict = {}
    #     x_coord_list = []
    #     y_coord_list = []
    #
    #     # метод, вызываемый при нажатии кнопки
    #     def key_press_event(event):
    #         if event.key == 'escape':
    #             plt.close()
    #
    #         elif event.key == 'enter':
    #             x, y = int(event.xdata), int(event.ydata)
    #             spectrums_name = input("Print spectrums name: ")
    #             spectrum_dict.update({spectrums_name: hypercube.values[:, y, x]})
    #             x_coord_list.append(x)
    #             y_coord_list.append(y)
    #             print("".join(["Spectrum /'", spectrums_name, "/' captured"]))
    #
    #     tiff.imshow(self.rgb)
    #     plt.connect('key_press_event', key_press_event)
    #     plt.show()
    #
    #     # передача данный о длинах волны
    #     upper_wavelength_list = []
    #     lower_wavelength_list = []
    #     for key in hypercube.bands_keys:
    #         band = self.bands_dict.setdefault(key)
    #         upper_wavelength_list.append(band.upper_wavelength)
    #         lower_wavelength_list.append(band.lower_wavelength)
    #     return SpectrumsSet(spectrums_sets_name, spectrum_dict, x_coord_list, y_coord_list, upper_wavelength_list,
    #                         lower_wavelength_list, hypercube.data_unit)


class Band:
    def __init__(self, band_address, band_number):
        self.digital_band = tiff.imread(band_address)
        self.band_number = band_number
        self.upper_wavelength = UPPER_BAND_WAVELENGTH[band_number - 1]
        self.lower_wavelength = LOWER_BAND_WAVELENGTH[band_number - 1]
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


class Hypercube:
    def __init__(self, hypercube_values, bands_keys, data_unit, source):
        self.values = hypercube_values
        self.bands_keys = bands_keys
        self.data_unit = data_unit
        self.source = source

    def to_turn_into_radiance(self):
        """

        :param hypercube:
        :return:
        """
        # создание пустого списка для мултиплекативных коэффициентов перевода цифровых значений в спектральные яркости
        mult_coef = []
        # создание пустого списка для адитивных коэффициентов перевода цифровых значений в спектральные яркости
        add_coef = []
        # заполнение списков mult_coef и add_coef в соответствии списку ключей для гиперкуба
        for band_key in self.bands_keys:
            mult_coef.append(self.source.bands_dict.setdefault(band_key).radiance_mult_band)
            add_coef.append(self.source.bands_dict.setdefault(band_key).radiance_add_band)
        # перевод цифровых значений гиперкуба в спектральную яркость
        radiance_hypercube = np.array([mult_coef[i] * self.values[i] +
                                       add_coef[i] for i in range(0, len(self.bands_keys))])
        return Hypercube(radiance_hypercube, self.bands_keys, SPECTRAL_BRIGHTNESS_UNIT, self.source)

    def to_norm_hypercube(self):
        # массив суммы всех каналов
        sum_hypercube = np.sum(self.values, axis=0)
        # замена нулевых значений на единицу
        sum_hypercube = np.where(sum_hypercube == 0, sum_hypercube, 1)
        norm_hypercube = self.values / sum_hypercube
        return Hypercube(norm_hypercube, self.bands_keys, RELATIVE_UNIT, self.source)


def to_load_spectrums_set(save_address):
    with open(save_address, "rb") as file:
        loaded_spectrums_set = pickle.load(file)
    return loaded_spectrums_set


class SpectrumsSet:
    def __init__(self, name, first_hypercube):
        self.name = name
        self.unit_str = first_hypercube.data_unit
        self.spectrums_dict = {}
        self.to_add_spectrum(first_hypercube)

    def to_plot(self, spectrums_keys_list=None, colors_list=None):
        if spectrums_keys_list is None:
            spectrums_keys_list = list(self.spectrums_dict.keys())

        if colors_list is None:
            colors_list = len(spectrums_keys_list) * ['']

        graph = plt.figure()

        for i in range(0, len(spectrums_keys_list)):
            spectrum = self.spectrums_dict.setdefault(spectrums_keys_list[i])
            y = spectrum.bands_list
            x = (spectrum.upper_wavelength_list + spectrum.lower_wavelength_list) / 2
            plt.plot(x, y, marker='o', color=colors_list[i])

        plt.legend(spectrums_keys_list)
        plt.grid()
        plt.title(self.name)
        plt.xlabel('Wavelength (µm)')
        plt.ylabel("".join(['Spectral radiance $\\left(', SPECTRAL_BRIGHTNESS_UNIT, '\\right)$'])) # Следует добавить возможность писать другие велиины
        plt.show()
        graph.savefig('D:\\results\\Landsat8_samples')

    def to_add_spectrum(self, hypercube):
        # словарь, в который будут записываться спектры
        spectrums_dict = {}
        # данные о длинах волны
        upper_wavelength_list = []
        lower_wavelength_list = []
        for key in hypercube.bands_keys:
            band = hypercube.source.bands_dict.setdefault(key)
            upper_wavelength_list.append(band.upper_wavelength)
            lower_wavelength_list.append(band.lower_wavelength)
        upper_wavelength_list = np.array(upper_wavelength_list)
        lower_wavelength_list = np.array(lower_wavelength_list)
        # метод, вызываемый при нажатии кнопки
        def key_press_event(event):
            if event.key == 'escape':
                plt.close()

            elif event.key == 'enter':
                x, y = int(event.xdata), int(event.ydata)
                spectrums_name = input("Print spectrums name: ")
                spectrums_dict.update({spectrums_name: Spectrum(hypercube.values[:, y, x], hypercube.source.name, x, y,
                                                                upper_wavelength_list, lower_wavelength_list)})

                print("".join(["Spectrum '", spectrums_name, "' captured"]))

        tiff.imshow(hypercube.source.rgb)
        plt.connect('key_press_event', key_press_event)
        plt.show()

        self.spectrums_dict.update(spectrums_dict)

    def delete_spectrum(self, spectrums_key):
        self.spectrums_dict.pop(spectrums_key)

    def save(self, file_name, address):
        with open("".join([address, '\\', file_name, '.file']), "wb") as file:
            pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)


class Spectrum:
    def __init__(self, bands_list, sources_name, x_coord, y_coord, upper_wavelength_list, lower_wavelength_list):
        self.bands_list = bands_list
        self.sources_name = sources_name
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.upper_wavelength_list = upper_wavelength_list
        self.lower_wavelength_list = lower_wavelength_list
