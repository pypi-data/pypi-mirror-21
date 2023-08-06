import matplotlib.pyplot as plt
import netCDF4 as nc
import os
import pandas as pd
try:
    import oceanobs.observatory as observatory
except ImportError:
    import observatory as observatory


class EMODnet(observatory.Observatory):

    def __init__(self, path=None):
        """
        Constructor of class
        :param path: Path where data is
        :type path: str
        """

        self.data = None
        self.metadata = None

        if path is not None:
            self.open(path)

    def open(self, path):
        """
        Open the nc or csv file
        :param path: Path where data is
        :type path: str
        :return: True i todo va bien, o str con el error cometido.
        """

        def open_nc(path_nc):
            """
            Open a nc file and extract metadata and data
            :param path_nc: Path of the nc file
            :type path_nc: str
            """
            def where_is_the_value(val_qc):
                """
                Where is the value.
                :param val_qc:
                :return:
                """
                # Search number of sensors
                n_sensors = len(val_qc[:][:][0])
                for i in range(n_sensors):
                    for j in range(len(val_qc[:][:, i])):
                        if val_qc[:][:, i][j] != '--':
                            return i
            try:
                # Open nc file
                df_nc = nc.Dataset(path_nc)
            except OSError as error:
                self.dialog = error
                return

            # Creation of the metadata dataframe
            self.metadata = pd.DataFrame({'platform_code': df_nc.platform_code,
                                          'wmo_platform_code': df_nc.wmo_platform_code,
                                          'institution': df_nc.institution,
                                          'id': df_nc.id,
                                          'type': [df_nc.data_type],
                                          'lat': df_nc.geospatial_lat_min,
                                          'lon': df_nc.geospatial_lon_min})
            # Creation of the data dataframe
            # The time is the index
            times = df_nc.variables['TIME']
            jd = nc.num2date(times[:], times.units)

            keys_nc = df_nc.variables.keys()
            # print(keys_nc)
            df_dict = {}
            if 'TIME_QC' in keys_nc:
                df_dict['time_qc'] = df_nc['TIME_QC'][:]
            if 'VTDH' in keys_nc:
                df_dict['wahe'] = df_nc['VTDH'][:][:, 0]
                df_dict['wahe_qc'] = df_nc['VTDH_QC'][:][:, 0]
            if 'VTZA' in keys_nc:
                df_dict['wape'] = df_nc['VTZA'][:][:, 0]
                df_dict['wape_qc'] = df_nc['VTZA_QC'][:][:, 0]
            if 'VDIR' in keys_nc:
                df_dict['wadi'] = df_nc['VDIR'][:][:, 0]
                df_dict['wadi_qc'] = df_nc['VDIR_QC'][:][:, 0]
            if 'ATMS' in keys_nc:
                df_dict['atm'] = df_nc['ATMS'][:][:, 0]
                df_dict['atm_qc'] = df_nc['ATMS_QC'][:][:, 0]
            if 'DRYT' in keys_nc:
                sensor = where_is_the_value(df_nc['DRYT'])
                if sensor is not None:
                    df_dict['atemp'] = df_nc['DRYT'][:][:, sensor]
                    df_dict['atemp_qc'] = df_nc['DRYT_QC'][:][:, sensor]
            if 'WSPD' in keys_nc:
                sensor = where_is_the_value(df_nc['WSPD_QC'])
                if sensor is not None:
                    df_dict['wisp'] = df_nc['WSPD'][:][:, sensor]
                    df_dict['wisp_qc'] = df_nc['WSPD_QC'][:][:, sensor]
            if 'WDIR' in keys_nc:
                sensor = where_is_the_value(df_nc['WDIR_QC'])
                if sensor is not None:
                    df_dict['widi'] = df_nc['WDIR'][:][:, sensor]
                    df_dict['widi_qc'] = df_nc['WDIR_QC'][:][:, sensor]
            if 'TEMP' in keys_nc:
                sensor = where_is_the_value(df_nc['TEMP_QC'])
                if sensor is not None:
                    df_dict['temp'] = df_nc['TEMP'][:][:, sensor]
                    df_dict['temp_qc'] = df_nc['TEMP_QC'][:][:, sensor]
            if 'ATMP' in keys_nc:
                sensor = where_is_the_value(df_nc['ATMP_QC'])
                if sensor is not None:
                    df_dict['atm'] = df_nc['ATMP'][:][:, sensor]
                    df_dict['atm_qc'] = df_nc['ATMP_QC'][:][:, sensor]
            if 'PRES' in keys_nc:
                sensor = where_is_the_value(df_nc['PRES_QC'])
                if sensor is not None:
                    df_dict['atmpres'] = df_nc['PRES'][:][:, sensor]
                    df_dict['atmpres_qc'] = df_nc['PRES_QC'][:][:, sensor]
            if 'SLEV' in keys_nc:
                sensor = where_is_the_value(df_nc['SLEV_QC'])
                if sensor is not None:
                    df_dict['sele'] = df_nc['SLEV'][:][:, sensor]
                    df_dict['sele_qc'] = df_nc['SLEV_QC'][:][:, sensor]
            if 'PRHT' in keys_nc:
                sensor = where_is_the_value(df_nc['PRHT_QC'])
                if sensor is not None:
                    df_dict['prec'] = df_nc['PRHT'][:][:, sensor]
                    df_dict['prec_qc'] = df_nc['PRHT_QC'][:][:, sensor]
            if 'RELH' in keys_nc:
                sensor = where_is_the_value(df_nc['RELH_QC'])
                if sensor is not None:
                    df_dict['relhu'] = df_nc['RELH'][:][:, sensor]
                    df_dict['relhu_qc'] = df_nc['RELH_QC'][:][:, sensor]
            if 'GSPD' in keys_nc:
                sensor = where_is_the_value(df_nc['GSPD_QC'])
                if sensor is not None:
                    df_dict['gusp'] = df_nc['GSPD'][:][:, sensor]
                    df_dict['gusp_qc'] = df_nc['GSPD_QC'][:][:, sensor]
            if 'HCSP' in keys_nc:
                sensor = where_is_the_value(df_nc['HCSP_QC'])
                if sensor is not None:
                    df_dict['cusp'] = df_nc['HCSP'][:][:, sensor]
                    df_dict['cusp_qc'] = df_nc['HCSP_QC'][:][:, sensor]
            if 'HCDT' in keys_nc:
                sensor = where_is_the_value(df_nc['HCDT_QC'])
                if sensor is not None:
                    df_dict['cudi'] = df_nc['HCDT'][:][:, sensor]
                    df_dict['cudi_qc'] = df_nc['HCDT_QC'][:][:, sensor]
            if 'DEWT' in keys_nc:
                sensor = where_is_the_value(df_nc['DEWT_QC'])
                if sensor is not None:
                    df_dict['dewt'] = df_nc['DEWT'][:][:, sensor]
                    df_dict['dewt_qc'] = df_nc['DEWT_QC'][:][:, sensor]
            if 'EWCT' in keys_nc:
                sensor = where_is_the_value(df_nc['EWCT_QC'])
                if sensor is not None:
                    df_dict['ecus'] = df_nc['EWCT'][:][:, sensor]
                    df_dict['ecus_qc'] = df_nc['EWCT_QC'][:][:, sensor]
            if 'NSCT' in keys_nc:
                sensor = where_is_the_value(df_nc['NSCT_QC'])
                if sensor is not None:
                    df_dict['ncus'] = df_nc['NSCT'][:][:, sensor]
                    df_dict['ncus_qc'] = df_nc['NSCT_QC'][:][:, sensor]
            if 'VAVH' in keys_nc:
                sensor = where_is_the_value(df_nc['VAVH_QC'])
                if sensor is not None:
                    df_dict['wasi'] = df_nc['VAVH'][:][:, sensor]
                    df_dict['wasi_qc'] = df_nc['VAVH_QC'][:][:, sensor]
            if 'VEMH' in keys_nc:
                sensor = where_is_the_value(df_nc['VEMH_QC'])
                if sensor is not None:
                    df_dict['mawa'] = df_nc['VEMH'][:][:, sensor]
                    df_dict['mawa_qc'] = df_nc['VEMH_QC'][:][:, sensor]
            if 'VCSP' in keys_nc:
                sensor = where_is_the_value(df_nc['VCSP_QC'])
                if sensor is not None:
                    df_dict['btcus'] = df_nc['VCSP'][:][:, sensor]
                    df_dict['btcus_qc'] = df_nc['VCSP_QC'][:][:, sensor]
            if 'VGTA' in keys_nc:
                sensor = where_is_the_value(df_nc['VGTA_QC'])
                if sensor is not None:
                    df_dict['wagape'] = df_nc['VGTA'][:][:, sensor]
                    df_dict['wagape_qc'] = df_nc['VGTA_QC'][:][:, sensor]
            if 'VHZA' in keys_nc:
                sensor = where_is_the_value(df_nc['VGTA_QC'])
                if sensor is not None:
                    df_dict['waahe'] = df_nc['VHZA'][:][:, sensor]
                    df_dict['waahe_qc'] = df_nc['VHZA_QC'][:][:, sensor]
            if 'VMDR' in keys_nc:
                sensor = where_is_the_value(df_nc['VGTA_QC'])
                if sensor is not None:
                    df_dict['wamdi'] = df_nc['VMDR'][:][:, sensor]
                    df_dict['wamdi_qc'] = df_nc['VMDR_QC'][:][:, sensor]
            if 'VTZM' in keys_nc:
                sensor = where_is_the_value(df_nc['VTZM_QC'])
                if sensor is not None:
                    df_dict['wahipe'] = df_nc['VTZM'][:][:, sensor]
                    df_dict['wahipe_qc'] = df_nc['VTZM_QC'][:][:, sensor]
            if 'NRAD' in keys_nc:
                sensor = where_is_the_value(df_nc['NRAD_QC'])
                if sensor is not None:
                    df_dict['tur'] = df_nc['NRAD'][:][:, sensor]
                    df_dict['tur_qc'] = df_nc['NRAD_QC'][:][:, sensor]

            self.data = pd.DataFrame(df_dict, index=jd)

        def listdir_fullpath(d):
            return [os.path.join(d, f) for f in os.listdir(d)]

        def open_list(path_list):
            big_data = pd.DataFrame()
            for one_path in path_list:
                if os.path.isfile(one_path):
                    _one_filename, one_file_extension = os.path.splitext(one_path)
                    if one_file_extension == ".nc":
                        open_nc(one_path)
                    else:
                        self.dialog = "Error: {} is no EMODnet data.".format(path)
                        continue
                    big_data = pd.concat([big_data, self.data])
            self.data = big_data
            # Copy of the data for future resets
            self.data_original = self.data.copy()

        self.dialog = False
        if isinstance(path, str):
            # Know if path is a file or a directory
            if os.path.isfile(path):
                # Path is a file
                # Know if it is a csv or a nc
                _filename, file_extension = os.path.splitext(path)
                if file_extension == ".nc":
                    open_nc(path)
            elif os.path.isdir(path):
                # Path is a directory
                path_lst = listdir_fullpath(path)
                open_list(path_lst)
            else:
                self.dialog = "Error: {} is not exists.".format(path)
        elif isinstance(path, list):
            open_list(path)

    @staticmethod
    def how_to_download_data(lenguage='CAT'):
        """
        Returns a string text explaining how to download EMODnet data with the selected language.
        :param lenguage: Idioma con el que quieres la explicacion
        :type lenguage: str
        :return: Explicacion
        :rtype: str
        """
        tutorial = ""
        if lenguage == 'CAT':
            tutorial = "Descarrega les dades de ..."
        return tutorial

if __name__ == '__main__':
    import sys
    from matplotlib import style
    style.use('ggplot')

    print("Example of class EMODnet")

    # Path de datos
    path_data = r""
    print("Data path: {}".format(path_data))

    print("Loading data, please wait.")
    ob = EMODnet(path_data)
    if ob.dialog:
        print(ob.dialog)
        sys.exit()
    else:
        print("Done.")

    print("METADATA INFORMATION")
    print(ob.info_metadata())
    print("DATA INFORMATION")
    print(ob.info_data())
    print("DATA MEANING")
    print(ob.info_parameters())

    # print("Resampling weekly frequency.")
    ob.resample_data('W')
    if ob.dialog:
        print(ob.dialog)
        sys.exit()
    else:
        print("Done.")

    # Slicing
    print("Slicing.")
    start = ""
    stop = ""
    print("Start: {}/{}/{} {}:{}:{}, Stop: {}/{}/{} {}:{}:{}".format(start[:4], start[4:6], start[6:8], start[8:10],
                                                                     start[10:12],  start[12:], stop[:4], stop[4:6],
                                                                     stop[6:8], stop[8:10], stop[10:12],  stop[12:]))
    ob.slicing(start, stop)
    print("Done.")

    # Plots
    print("Making plots.")
    ob.plt_all()
    plt.show()
    print("Done.")
