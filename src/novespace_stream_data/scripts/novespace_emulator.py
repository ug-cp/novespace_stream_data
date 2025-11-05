# SPDX-FileCopyrightText: 2025 Daniel Maier, Daniel Mohr, Thomas Villatte
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
This emulates a data stream.

Copyright (C) 2025 Daniel Maier (University of Greifswald),
                   Daniel Mohr (University of Greifswald),
                   Thomas Villatte (Novespace)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import csv
import signal
import socket
import time
from importlib.resources import files
from threading import Event


class NovespaceStreamEmulator():
    """
    This program emulates the UDP broadcast of the Data-unit,
    sending data from a csv file (row by row) to a UDP port on a
    specific IP address, every 0.1s
    """

    def __init__(self, filepath=None, ip_address='localhost', port=3131,
                 sleeptime=0.1):
        """
        This emulates a data stream.

        Inputs:

        :param filepath (str): Path to file to stream
        :param ip_address (str): ip address to send data
        :param port (int): Number of Port for streaming (default: 3131)
        :param sleeptime: number of seconds to sleep between datagrams
        """
        self.filepath = filepath
        self.ip_address = ip_address
        self.port = port
        self.sleeptime = sleeptime
        self.stop_event = Event()
        self.streaming_not_running = Event()
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def __call__(self):
        """
        stream data to socket
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        print(f'stream "{self.filepath}"')
        print("to stop streaming use: CTRL+C or send a TERM signal\n")
        self.stop_event.clear()
        self.streaming_not_running.clear()
        with open(self.filepath, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if self.stop_event.is_set():
                    print("transmission stopped")
                    break
                message = ",".join(row)
                sock.sendto(message.encode(), (self.ip_address, self.port))
                time.sleep(self.sleeptime)
        if not self.stop_event.is_set():
            print("full file sent")
        sock.close()
        self.streaming_not_running.set()

    def signal_handler(self, signum, _):
        """
        signal handler to catch TERM signal
        """
        if signum == signal.SIGTERM:
            print("got TERM signal")
        elif signum == signal.SIGINT:
            print("got SIGINT signal (Ctrl+C)")
        self.stop_event.set()
        self.streaming_not_running.wait(max(3*self.sleeptime, 0.1))


def start_novespace_emulator(
        filepath=None, ip_address='localhost', port=3131, sleeptime=0.1):
    """
    This emulates a data stream.

    Inputs:

    :param filepath (str): Path to file to stream
    :param ip_address (str): ip address to send data
    :param port (int): Number of Port for streaming (default: 3131)
    :param sleeptime: number of seconds to sleep between datagrams
    """
    if filepath is None:
        filepath = files("novespace_stream_data").joinpath(
            "data/example_data.csv")
    description = "This script emulates data stream of airplanedata"
    epilog = "Date: 2025-11-05\n"
    epilog += "License: GPL-3.0-or-later"
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '-filepath',
        nargs="?",
        default=filepath,
        type=str,
        required=False,
        dest='filepath',
        help='path to file to stream (example data as default: %(default)s)',
        metavar='f')
    parser.add_argument(
        '-ip_address',
        nargs="?",
        default=ip_address,
        type=str,
        required=False,
        dest='ip_address',
        help='ip address to send data (default: %(default)s)',
        metavar='dst')
    parser.add_argument(
        '-port',
        nargs="?",
        default=port,
        type=int,
        required=False,
        dest='port',
        help='Number of Port for streaming (default: %(default)s)',
        metavar='i')
    parser.add_argument(
        '-sleeptime',
        nargs="?",
        default=sleeptime,
        type=float,
        required=False,
        dest='sleeptime',
        help='number of seconds to sleep between datagrams '
        '(default: %(default)s)',
        metavar='i')
    args = parser.parse_args()
    stream_emulator = NovespaceStreamEmulator(
        args.filepath, args.ip_address, args.port, args.sleeptime)
    stream_emulator()
