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

`novespace_stream_data` receives and logs data streams from
[Novespace](https://www.airzerog.com/), obtained during scientific research
flights.

This stream data was first provided during
45. [DLR](https://www.dlr.de/de) parabolic flight campaign in October 2025.

This software is based on Python code originally developed by
Thomas Villatte (Novespace), which featured a graphical user interface
built with tkinter. We have redesigned the software to operate without a GUI,
enabling deployment on resource-constrained embedded systems. To support data
correlation, the local computer's timestamp is included in the logged data.

## Installation

You can install `novespace_stream_data` using `pip` or `pipx`.

**Using pipx (recommended):**

Example:

```sh
pipx install https://gitlab.com/ug-cp/com/ug-cp/novespace_stream_data/-/archive/0.3.0/novespace_stream_data-0.3.0.zip
```

**Using pip:**

Example:

```sh
pip3 install https://gitlab.com/ug-cp/com/ug-cp/novespace_stream_data/-/archive/0.3.0/novespace_stream_data-0.3.0.zip
```

For development, you can install an editable version:

```sh
git clone https://gitlab.com/ug-cp/com/ug-cp/novespace_stream_data
cd novespace_stream_data
pip3 install -e .
```

## Usage

The software provides both command-line and GUI applications for
receiving and emulating data streams.

**Receiving data:**

* `novespace_stream_data_receiver`: command line receiver.
* `novespace_stream_data_gui_receiver`: GUI receiver.

The receiver applications store the streamed data in a CSV file.

**Emulating data:**

* `novespace_stream_data_emulator`: command line emulator.
* `novespace_stream_data_gui_emulator`: GUI emulator.

The emulation is only provided for testing of the receiver applications.
Normally one would use the stream from Novespace.

**Stopping the stream:**

Terminate the stream using `Ctrl+C` or by sending a TERM signal (e.g., `kill`).

**Running in the background:**

You can run the receiver in the background:

```sh
((cd /logdata && novespace_stream_data_receiver) > /dev/null 2> /dev/null) &
```

Stopping th background process:

```sh
killall novespace_stream_data_receiver
```

**Help Information:**

The command-line tools provide help output and command-line parameters:

```sh
novespace_stream_data_receiver -h
novespace_stream_data_emulator -h
```

## Citation

If you use `novespace_stream_data` in your research, please cite it.

-- tbd --

If you are using a specific version, please use the corresponding DOI.

This is good scientific practice, but does not restrict the use,
modification, and distribution of the code under the terms of the
GPL-3.0-or-later license. The code remains freely available.
