# SPDX-FileCopyrightText: 2025 Daniel Maier, Daniel Mohr, Thomas Villatte
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
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
