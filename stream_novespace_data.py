"""
Created on Thu Oct 23 11:04:46 2025

@author: daniel_m

"""

import os
import nove_space_stream


def start_nove_space_datastream(
        port=3131, filepath=os.getcwd(), printing=False):
    """
    This functions starts the streaming of airplanedata and
    writes them into a csv-file.
    To stop stream use the Ctrl+C keyboard interrupt

    Inputs:

    :param port (int): Number of Port for streaming (default: 3131)
    :param filepath (str): Path to file in which the csv-file is
                           created (default cwd)
    :param printig (bool): Should the recived data be printed
                           on the console? (default False)
    """
    datastream = nove_space_stream.NoSpaStream(filepath, port, printing)
    datastream.start_streaming()
