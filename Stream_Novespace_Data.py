#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 11:04:46 2025

@author: daniel_m

This functions starts the streaming of airplanedata and writes them into a csv-file.
To stop stream use the Ctrl+C keyboard interrupt

Inputs:
port (int): Number of Port for streaming (default: 3131)
filepath (str): Path to file in which the csv-file is created (default cwd)
printig (bool): Should the recived data be printed on the console? (default False)
"""
import os

def start_NoveSpace_Datastream(port=3131,filepath=os.getcwd(),printing=False):
    import NoSpa_stream
    Datastream=NoSpa_stream.NoSpaStream(filepath,port,printing)
    Datastream.start_streaming()