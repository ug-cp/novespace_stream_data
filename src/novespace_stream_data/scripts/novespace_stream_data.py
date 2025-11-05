# SPDX-FileCopyrightText: 2025 Daniel Maier, Daniel Mohr, Thomas Villatte
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
This is a simple wrapper to start
stream_novespace_data.start_nove_space_datastream
from console.

`novespace_stream_data` gets the stream from Novespace during
scientific research flights.

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
import os

from novespace_stream_data.receive import NoSpaStream


def start_nove_space_datastream(
        port=3131, filepath=os.getcwd(), printing=False):
    """
    This function starts the streaming of airplanedata and
    writes them into a csv-file.
    To stop stream use the Ctrl+C keyboard interrupt

    Inputs:

    :param port (int): Number of Port for streaming (default: 3131)
    :param filepath (str): Path to file in which the csv-file is
                           created (default cwd)
    :param printig (bool): Should the recived data be printed
                           on the console? (default False)
    """
    description = "This script receives data stream of airplanedata and "
    description += "writes them into a csv-file."
    epilog = "Date: 2025-11-05\n"
    epilog += "License: GPL-3.0-or-later"
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '-port',
        nargs="?",
        default=port,
        type=int,
        required=False,
        dest='port',
        help='Number of Port for streaming (default: %(default)s)',
        metavar='i')
    args = parser.parse_args()
    datastream = NoSpaStream(filepath, args.port, printing)
    datastream.start_streaming()
    datastream.streaming_thread.join()
