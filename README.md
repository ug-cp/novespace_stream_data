---
author: Daniel Maier, Daniel Mohr, Thomas Villatte
license: GPL-3.0-or-later
home: https://gitlab.com/ug-cp/novespace_stream_data
latest_release: https://gitlab.com/ug-cp/com/ug-cp/novespace_stream_data/-/releases/permalink/latest
doi:
---
<!--
SPDX-FileCopyrightText: 2025 Daniel Maier, Daniel Mohr, Thomas Villatte

SPDX-License-Identifier: GPL-3.0-or-later
-->

# novespace_stream_data

`novespace_stream_data` gets the stream from
[Novespace](https://www.airzerog.com/),
which is provided in scrientific research flights.

This stream data was first provided during
45. [DLR](https://www.dlr.de/de) parabolic flight campaign in October 2025.

This software utilizes Python code originally developed by
Thomas Villatte (Novespace) as its foundation. The original application
featured a graphical user interface built with tkinter. Our derived software
has been redesigned to operate without a GUI, enabling deployment on
resource-constrained embedded systems. To facilitate data correlation,
the local computer's timestamp is included in the logged data.

## install

To install use `pip` or `pipx`.

For example to install with `pipx` (similar with `pip`):

```sh
pipx install https://gitlab.com/ug-cp/com/ug-cp/novespace_stream_data/-/archive/0.3.0/novespace_stream_data-0.3.0.zip
```

For development you could install an editable version, e. g.:

```sh
git clone https://gitlab.com/ug-cp/com/ug-cp/novespace_stream_data
cd novespace_stream_data
pip3 install -e .
```

## usage

To start the stream of data, use the command `novespace_stream_data_receiver`
for command line and `novespace_stream_data_gui_receiver` as a GUI.

This will start the datastream and will store it in a csv-file
that is created in the path, the program was started from.

To stop streaming use "Ctrl+C" or TERM signal (kill).

To emulate a data stream use as command line tool
`novespace_stream_data_emulator` and `novespace_stream_data_gui_emulator` as a
GUI.

It is possible to start `novespace_stream_data_receiver` in the background,
e. g.:

```sh
((cd /logdata && novespace_stream_data_receiver) > /dev/null 2> /dev/null)&
```

Stopping is possible using `killall`, e. g.:

```sh
killall novespace_stream_data_receiver
```

The command line tools have some help output and command line parameters,
e. g.:

```sh
novespace_stream_data_receiver -h
novespace_stream_data_emulator -h
```

## Citation

If you are using `novespace_stream_data`, please make it clear by citing:

-- tbd --

If you are using a specific version, please use the corresponding DOI.

This is good practice in science, but does not constitute a restriction in the
sense of the GPL license. The code remains freely available for use,
modification, and distribution under the terms of the GPL-3.0-or-later.
