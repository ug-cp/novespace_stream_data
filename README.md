---
author: Daniel Maier, Daniel Mohr, Thomas Villatte
license: GPL-3.0-or-later
home: https://gitlab.com/ug-cp/ovespace_stream_data
latest_release: https://gitlab.com/ug-cp/com/ug-cp/ovespace_stream_data/-/releases/permalink/latest
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

To start the stream of data, use the command `do_logging.py`.

This will start the datastream and will store it in a csv-file
that is created in the path, the program was started from.

To stop streaming use "Ctrl+C".

## Citation

If you are using `novespace_stream_data`, please make it clear by citing:

-- tbd --

If you are using a specific version, please use the corresponding DOI.

This is good practice in science, but does not constitute a restriction in the
sense of the GPL license. The code remains freely available for use,
modification, and distribution under the terms of the GPL-3.0-or-later.
