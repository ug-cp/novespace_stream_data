"""
Created on Thu Oct 23 08:47:40 2025

@author: daniel_m
"""

# necessary imports
import csv
import os
import socket
import sys
import time
from datetime import datetime
from pathlib import Path
from threading import Thread

# class definition


class NoSpaStream():
    """
    This class allows to get the stream from
    Novespace ( https://www.airzerog.com/ ),
    which is provided in scrientific research flights.

    This stream data was first provided during
    45. DLR parabolic flight campaign in October 2025.
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, csv_path, inputport=3131, printing=False):
        """
        :param csv_path: path to store the data
        :param inputport: port to listen.
        :param printing: If set to True the data is not only logged, but also
                         printed on the console (stdout).
        """
        self.streampath = csv_path
        self.streamport = inputport
        self.print_on_console = printing
        self.socket_address = ('', self.streamport)
        self.streaming_status = False
        self.csv_fieldnames = [
            'Unix - timestamp', ' Miliseconds since 00:00:00 (ms)',
            ' Time', ' Jx (g)', ' Jy (g)', ' Jz (g)',
            ' Temperature (°C)', ' Humidity (%)', ' Pressure (mbar)',
            ' Parabola', ' Announcement']
        self.socket = None
        self.csv_file = None
        self.streaming_thread = None

        if not os.path.isdir(self.streampath):
            print("ERROR! No valid folder for csv-file is given.")

    def connect_socket(self):
        """
        Connect to the UDP socket.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.socket_address)
        print(
            f"Creation of UDP-socket with port {self.streamport} sucessfull.")

    def get_status(self):
        """
        Print the current streaming status.
        """
        if self.streaming_status is True:
            print(
                "Active datastream from port "
                f"{self.streamport} to {self.csv_file}.")
        else:
            print("No active datastream!")

    def start_streaming(self):
        """
        Start the data streaming process.
        """
        if self.streaming_status is True:
            print("The stream is allready active!")
        else:
            # try:
            self.connect_socket()
            # except:
            # print("ERROR! "
            #       "Creation of UDP-socket failed. Check the portnumber.")
            # sys.exit()
            self.csv_file = Path(
                self.streampath,
                'NoveSpa_planedata_'
                f'{datetime.now().strftime("%Y%m%d-%Hh%Mm%Ss")}.csv')
            self.csv_file.touch()
            with open(self.csv_file, mode='a',
                      newline='', encoding='utf-8') as filedescriptor:
                csv_writer = csv.DictWriter(
                    filedescriptor,
                    fieldnames=self.csv_fieldnames, delimiter=';')
                csv_writer.writeheader()
            print(
                "Starting datastream from port "
                f"{self.streamport} to file: {self.csv_file}")
            print("To end streaming use: CTRL+C\n")
            self.streaming_status = True
            self.streaming_thread = Thread(
                target=self.stream_data(), daemon=True)
            self.streaming_thread.start()

    def end_streaming(self):
        """
        End the data streaming process.
        """
        if self.streaming_status is False:
            print("No active data-stream to be terminated.")
        else:
            self.streaming_status = False
            time.sleep(0.1)
            try:
                self.socket.close()
                print(f"\nEnd of streaming to {self.csv_file}")
                print(datetime.now().strftime(
                    "Streaming ended on %Y-%m-%d at %H:%M:%S"))
                sys.exit(0)
            except:  # noqa: E722 pylint: disable=W0702
                print("ERROR! Ending of Datastream was not sucessfull!")
                sys.exit(1)

    def stream_data(self):
        """
        Receive and save data from the UDP socket.
        """
        print("streaming data\n")
        try:
            while self.streaming_status is True:
                # Recive and decode datastream
                data, _ = self.socket.recvfrom(1024)
                data_str = data.decode('utf-8')
                unixtime = str(time.time())
                data_str = unixtime + ';' + data_str

                # Save the data into the csv file
                with open(self.csv_file, mode='a',
                          newline='', encoding='utf-8') as filedescriptor:
                    csv_writer = csv.writer(filedescriptor)
                    csv_writer.writerow([data_str])
                    if self.print_on_console is True:
                        print(data_str)
        except KeyboardInterrupt:
            # print(f"Error in receiving data: {e}")
            self.end_streaming()
