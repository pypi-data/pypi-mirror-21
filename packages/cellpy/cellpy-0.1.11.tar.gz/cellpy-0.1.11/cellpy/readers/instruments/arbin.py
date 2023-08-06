"""arbin res-type data files"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import os
import tempfile
import shutil
import logging
import warnings
from six.moves import range  # 'lazy' range (i.e. xrange in Py27)
import numpy as np

import pandas as pd

from cellpy.readers.cellreader import dataset
from cellpy.readers.cellreader import fileID
from cellpy.readers.cellreader import humanize_bytes
from cellpy.readers.cellreader import check64bit
from cellpy.readers.cellreader import USE_ADO
from cellpy.readers.cellreader import get_headers_normal


if USE_ADO:
    try:
        import adodbapi as dbloader  # http://adodbapi.sourceforge.net/
    except ImportError:
        USE_ADO = False

else:
    try:
        import pyodbc as dbloader
    except ImportError:
        warnings.warn("COULD NOT LOAD DBLOADER!",  ImportWarning)
        dbloader = None




# The columns to choose if minimum selection is selected
MINIMUM_SELECTION = ["Data_Point", "Test_Time", "Step_Time", "DateTime", "Step_Index", "Cycle_Index",
                     "Current", "Voltage", "Charge_Capacity","Discharge_Capacity", "Internal_Resistance"]

# Names of the tables in the .res db that is used by cellpy
TABLE_NAMES = {
    "normal": "Channel_Normal_Table",
    "global": "Global_Table",
    "statistic": "Channel_Statistic_Table",
}


# def get_raw_limits():
#     """Include the settings for how to decide what kind of step you are examining here.
#
#     The raw limits are 'epsilons' used to check if the current and/or voltage is stable (for example
#     for galvanostatic steps, one would expect that the current is stable (constant) and non-zero).
#     It is expected that different instruments (with different resolution etc.) have different
#     'epsilons'.
#
#     Returns: the raw limits (dict)
#
#     """
#     raw_limits = dict()
#     raw_limits["current_hard"] = 0.0000000000001
#     raw_limits["current_soft"] = 0.00001
#     raw_limits["stable_current_hard"] = 2.0
#     raw_limits["stable_current_soft"] = 4.0
#     raw_limits["stable_voltage_hard"] = 2.0
#     raw_limits["stable_voltage_soft"] = 4.0
#     raw_limits["stable_charge_hard"] = 2.0
#     raw_limits["stable_charge_soft"] = 5.0
#     raw_limits["ir_change"] = 0.00001
#     return raw_limits


# def get_raw_units():
#     """Include the settings for the units used by the instrument.
#
#     The units are defined w.r.t. the SI units ('unit-fractions'; currently only units that are multiples of
#     Si units can be used). For example, for current defined in mA, the value for the
#     current unit-fraction will be 0.001.
#
#     Returns: dictionary containing the unit-fractions for current, charge, and mass
#
#     """
#     raw_units = dict()
#     raw_units["current"] = 1.0  # A
#     raw_units["charge"] = 1.0  # Ah
#     raw_units["mass"] = 0.001  # g
#     return raw_units


# def get_headers_global():
#     """Defines the so-called global column headings for Arbin .res-files"""
#     headers = dict()
#     # - global column headings (specific for Arbin)
#     headers["applications_path_txt"] = 'Applications_Path'
#     headers["channel_index_txt"] = 'Channel_Index'
#     headers["channel_number_txt"] = 'Channel_Number'
#     headers["channel_type_txt"] = 'Channel_Type'
#     headers["comments_txt"] = 'Comments'
#     headers["creator_txt"] = 'Creator'
#     headers["daq_index_txt"] = 'DAQ_Index'
#     headers["item_id_txt"] = 'Item_ID'
#     headers["log_aux_data_flag_txt"] = 'Log_Aux_Data_Flag'
#     headers["log_chanstat_data_flag_txt"] = 'Log_ChanStat_Data_Flag'
#     headers["log_event_data_flag_txt"] = 'Log_Event_Data_Flag'
#     headers["log_smart_battery_data_flag_txt"] = 'Log_Smart_Battery_Data_Flag'
#     headers["mapped_aux_conc_cnumber_txt"] = 'Mapped_Aux_Conc_CNumber'
#     headers["mapped_aux_di_cnumber_txt"] = 'Mapped_Aux_DI_CNumber'
#     headers["mapped_aux_do_cnumber_txt"] = 'Mapped_Aux_DO_CNumber'
#     headers["mapped_aux_flow_rate_cnumber_txt"] = 'Mapped_Aux_Flow_Rate_CNumber'
#     headers["mapped_aux_ph_number_txt"] = 'Mapped_Aux_PH_Number'
#     headers["mapped_aux_pressure_number_txt"] = 'Mapped_Aux_Pressure_Number'
#     headers["mapped_aux_temperature_number_txt"] = 'Mapped_Aux_Temperature_Number'
#     headers["mapped_aux_voltage_number_txt"] = 'Mapped_Aux_Voltage_Number'
#     headers["schedule_file_name_txt"] = 'Schedule_File_Name'  # KEEP FOR CELLPY FILE FORMAT
#     headers["start_datetime_txt"] = 'Start_DateTime'
#     headers["test_id_txt"] = 'Test_ID'  # KEEP FOR CELLPY FILE FORMAT
#     headers["test_name_txt"] = 'Test_Name'  # KEEP FOR CELLPY FILE FORMAT
#     return headers


class ArbinLoader(object):
    """ Class for loading arbin-data from res-files."""

    def __init__(self):
        """initiates the ArbinLoader class"""
        # could use __init__(self, cellpydata_object) and set self.logger = cellpydata_object.logger etc.
        # then remember to include that as prm in "out of class" functions
        self.logger = logging.getLogger()
        self.load_only_summary = False
        self.select_minimal = False
        self.max_res_filesize = 150000000

        self.chunk_size = None  # 100000
        self.max_chunks = None
        self.last_chunk = None
        self.limit_loaded_cycles = None
        self.load_until_error = False

        self.headers_normal = get_headers_normal()
        self.headers_global = self.get_headers_global()

    @staticmethod
    def get_raw_units():
        """Include the settings for the units used by the instrument.

        The units are defined w.r.t. the SI units ('unit-fractions'; currently only units that are multiples of
        Si units can be used). For example, for current defined in mA, the value for the
        current unit-fraction will be 0.001.

        Returns: dictionary containing the unit-fractions for current, charge, and mass

        """
        raw_units = dict()
        raw_units["current"] = 1.0  # A
        raw_units["charge"] = 1.0  # Ah
        raw_units["mass"] = 0.001  # g
        return raw_units

    @staticmethod
    def get_headers_global():
        """Defines the so-called global column headings for Arbin .res-files"""
        headers = dict()
        # - global column headings (specific for Arbin)
        headers["applications_path_txt"] = 'Applications_Path'
        headers["channel_index_txt"] = 'Channel_Index'
        headers["channel_number_txt"] = 'Channel_Number'
        headers["channel_type_txt"] = 'Channel_Type'
        headers["comments_txt"] = 'Comments'
        headers["creator_txt"] = 'Creator'
        headers["daq_index_txt"] = 'DAQ_Index'
        headers["item_id_txt"] = 'Item_ID'
        headers["log_aux_data_flag_txt"] = 'Log_Aux_Data_Flag'
        headers["log_chanstat_data_flag_txt"] = 'Log_ChanStat_Data_Flag'
        headers["log_event_data_flag_txt"] = 'Log_Event_Data_Flag'
        headers["log_smart_battery_data_flag_txt"] = 'Log_Smart_Battery_Data_Flag'
        headers["mapped_aux_conc_cnumber_txt"] = 'Mapped_Aux_Conc_CNumber'
        headers["mapped_aux_di_cnumber_txt"] = 'Mapped_Aux_DI_CNumber'
        headers["mapped_aux_do_cnumber_txt"] = 'Mapped_Aux_DO_CNumber'
        headers["mapped_aux_flow_rate_cnumber_txt"] = 'Mapped_Aux_Flow_Rate_CNumber'
        headers["mapped_aux_ph_number_txt"] = 'Mapped_Aux_PH_Number'
        headers["mapped_aux_pressure_number_txt"] = 'Mapped_Aux_Pressure_Number'
        headers["mapped_aux_temperature_number_txt"] = 'Mapped_Aux_Temperature_Number'
        headers["mapped_aux_voltage_number_txt"] = 'Mapped_Aux_Voltage_Number'
        headers["schedule_file_name_txt"] = 'Schedule_File_Name'  # KEEP FOR CELLPY FILE FORMAT
        headers["start_datetime_txt"] = 'Start_DateTime'
        headers["test_id_txt"] = 'Test_ID'  # KEEP FOR CELLPY FILE FORMAT
        headers["test_name_txt"] = 'Test_Name'  # KEEP FOR CELLPY FILE FORMAT
        return headers

    @staticmethod
    def get_raw_limits():
        """Include the settings for how to decide what kind of step you are examining here.

        The raw limits are 'epsilons' used to check if the current and/or voltage is stable (for example
        for galvanostatic steps, one would expect that the current is stable (constant) and non-zero).
        It is expected that different instruments (with different resolution etc.) have different
        'epsilons'.

        Returns: the raw limits (dict)

        """
        raw_limits = dict()
        raw_limits["current_hard"] = 0.0000000000001
        raw_limits["current_soft"] = 0.00001
        raw_limits["stable_current_hard"] = 2.0
        raw_limits["stable_current_soft"] = 4.0
        raw_limits["stable_voltage_hard"] = 2.0
        raw_limits["stable_voltage_soft"] = 4.0
        raw_limits["stable_charge_hard"] = 2.0
        raw_limits["stable_charge_soft"] = 5.0
        raw_limits["ir_change"] = 0.00001
        return raw_limits


    def loader(self, file_name=None):
        """Loads data from arbin .res files.

        Args:
            file_name (str): path to .res file.

        Returns:
            new_tests (list of data objects), FileError

        """

        new_tests = []
        if not os.path.isfile(file_name):
            print("Missing file_\n   %s" % file_name)

        filesize = os.path.getsize(file_name)
        hfilesize = humanize_bytes(filesize)
        txt = "Filesize: %i (%s)" % (filesize, hfilesize)
        self.logger.debug(txt)
        if filesize > self.max_res_filesize and not self.load_only_summary:
            error_message = "\nERROR (loader):\n"
            error_message += "%s > %s - File is too big!\n" % (hfilesize, humanize_bytes(self.max_res_filesize))
            error_message += "(edit self.max_res_filesize)\n"
            print(error_message)
            return None
            # sys.exit(FileError)

        table_name_global = TABLE_NAMES["global"]
        table_name_stats = TABLE_NAMES["statistic"]

        temp_dir = tempfile.gettempdir()
        temp_filename = os.path.join(temp_dir, os.path.basename(file_name))
        shutil.copy2(file_name, temp_dir)
        print(".", end=' ')

        constr = self.__get_res_connector(temp_filename)
        if USE_ADO:
            conn = dbloader.connect(constr)  # adodbapi
        else:
            conn = dbloader.connect(constr, autocommit=True)
        print(".", end=' ')

        sql = "select * from %s" % table_name_global
        global_data_df = pd.read_sql_query(sql, conn)
        # col_names = list(global_data_df.columns.values)

        tests = global_data_df[self.headers_normal['test_id_txt']]  # OBS
        number_of_sets = len(tests)
        print(".", end=' ')

        for test_no in range(number_of_sets):
            data = dataset()
            data.test_no = test_no
            data.loaded_from = file_name
            fid = fileID(file_name)
            # data.parent_filename = os.path.basename(file_name)# name of the .res file it is loaded from
            data.channel_index = int(global_data_df[self.headers_global['channel_index_txt']][test_no])
            data.channel_number = int(global_data_df[self.headers_global['channel_number_txt']][test_no])
            data.creator = global_data_df[self.headers_global['creator_txt']][test_no]
            data.item_ID = global_data_df[self.headers_global['item_id_txt']][test_no]
            data.schedule_file_name = global_data_df[self.headers_global['schedule_file_name_txt']][test_no]
            data.start_datetime = global_data_df[self.headers_global['start_datetime_txt']][test_no]
            data.test_ID = int(global_data_df[self.headers_normal['test_id_txt']][test_no])  # OBS
            data.test_name = global_data_df[self.headers_global['test_name_txt']][test_no]
            data.raw_data_files.append(fid)

            # --------- read raw-data (normal-data) -------------------------
            length_of_test, normal_df = self._load_res_normal_table(conn, data.test_ID)

            # --------- read stats-data (summary-data) ----------------------
            sql = "select * from %s where %s=%s order by %s" % (table_name_stats,
                                                                self.headers_normal['test_id_txt'],
                                                                data.test_ID,
                                                                self.headers_normal['data_point_txt'])
            summary_df = pd.read_sql_query(sql, conn)
            data.dfsummary = summary_df
            data.dfdata = normal_df
            data.raw_data_files_length.append(length_of_test)
            new_tests.append(data)
            self._clean_up_loadres(None, conn, temp_filename)
            print(". <-")
        return new_tests




    def _load_res_normal_table(self, conn, test_ID):
        table_name_normal = TABLE_NAMES["normal"]
        if self.load_only_summary:  # SETTING
            return 0

        if self.select_minimal:  # SETTING
            columns = MINIMUM_SELECTION
            columns_txt = ", ".join(["%s"] * len(columns)) % tuple(columns)
        else:
            columns_txt = "*"

        sql_1 = "select %s " % columns_txt
        sql_2 = "from %s " % table_name_normal
        sql_3 = "where %s=%s " % (self.headers_normal['test_id_txt'], test_ID)
        sql_4 = ""

        if self.limit_loaded_cycles:
            if len(self.limit_loaded_cycles) > 1:
                sql_4 = "AND %s>%i " % (self.headers_normal['cycle_index_txt'], self.limit_loaded_cycles[0])
                sql_4 += "AND %s<%i " % (self.headers_normal['cycle_index_txt'], self.limit_loaded_cycles[-1])
            else:
                sql_4 = "AND %s=%i " % (self.headers_normal['cycle_index_txt'], self.limit_loaded_cycles[0])

        sql_5 = "order by %s" % self.headers_normal['data_point_txt']
        sql = sql_1 + sql_2 + sql_3 + sql_4 + sql_5

        if not self.chunk_size:
            normal_df = pd.read_sql_query(sql, conn)
            length_of_test = normal_df.shape[0]
        else:
            normal_df_reader = pd.read_sql_query(sql, conn, chunksize=self.chunk_size)
            if not self.last_chunk:
                normal_df = next(normal_df_reader)
                chunk_number = 1
            else:
                chunk_number = 0
                for j in range(self.last_chunk):
                    normal_df = next(normal_df_reader)  # TODO: This is SLOW - should use itertools.islice
                    chunk_number += 1

            for chunk in normal_df_reader:

                if self.load_until_error:
                    try:
                        normal_df = pd.concat([normal_df, chunk], ignore_index=True)
                        print("*", end=' ')
                    except MemoryError:
                        print(" - Could not read complete file (MemoryError).")
                        print("Last successfully loaded chunk number:", chunk_number)
                        print("Chunk size:", self.chunk_size)
                        break
                elif self.max_chunks:
                    if chunk_number < self.max_chunks:
                        normal_df = pd.concat([normal_df, chunk], ignore_index=True)
                        print("*", end=' ')
                    else:
                        break
                else:
                    normal_df = pd.concat([normal_df, chunk], ignore_index=True)
                chunk_number += 1
            length_of_test = normal_df.shape[0]

        return length_of_test, normal_df

    @staticmethod
    def __get_res_connector( temp_filename):
        is64bit_python = check64bit(System="python")
        # TODO: should be made to a function
        # is64bit_os = check64bit(System = "os")
        if USE_ADO:
            if is64bit_python:
                print("using 64 bit python")
                constr = 'Provider=Microsoft.ACE.OLEDB.12.0; Data Source=%s' % temp_filename
            else:
                constr = 'Provider=Microsoft.Jet.OLEDB.4.0; Data Source=%s' % temp_filename

        else:
            constr = 'Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=' + temp_filename
        return constr


    def _clean_up_loadres(self, cur, conn, filename):
        if cur is not None:
            cur.close()  # adodbapi
        if conn is not None:
            conn.close()  # adodbapi
        if os.path.isfile(filename):
            try:
                os.remove(filename)
            except WindowsError as e:
                self.logger.warning("could not remove tmp-file\n%s %s" % (filename, e))


    def load(self, file_name):
        """Load a raw data-file

        Args:
            file_name (path)

        Returns:
            loaded test
        """

        raw_file_loader = self.loader
        new_rundata = raw_file_loader(file_name)
        new_rundata = self.inspect(new_rundata)
        return new_rundata

    def inspect(self, run_data):
        """inspect the file.
        
        -adds missing columns (with np.nan)
        """

        checked_rundata = []
        for data in run_data:
            new_cols = data.dfdata.columns
            for col in self.headers_normal:
                if not col in new_cols:
                    data.dfdata[col] = np.nan
            checked_rundata.append(data)
        return checked_rundata

    def repair(self):
        """try to repair a broken/corrupted file"""
        pass


def lp_resf(filename):
    """Load a raw data file """
    print("1")
    a = ArbinLoader()
    a.load(filename)
    print("2")




if __name__ == '__main__':
    # TODO: 1) rewrite load_raw - could possibly move it outside of class --OK
    # TODO: 2) make a test --OK
    # TODO: 3) make it work --OK
    # TODO: 4) include changes in load_raw etc in cellreader.py

    import logging
    from cellpy import log

    log.setup_logging(default_level=logging.DEBUG)
    testfile = "../../indata/20160805_test001_45_cc_01.res"
    lp_resf(testfile)
