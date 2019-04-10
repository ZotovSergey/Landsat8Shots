import Shot

if __name__ == "__main__":
    spectrums_set = Shot.to_load_spectrums_set('D:\\results\\Spectra samples. Valuysky rayon. 2018.08.08.file')
    spectrums_set.to_plot(list(spectrums_set.spectrums_dict.keys()), ['blue', 'lime', 'green', 'gold', 'black'])