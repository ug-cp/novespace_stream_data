# SPDX-FileCopyrightText: 2025 Daniel Maier, Daniel Mohr, Thomas Villatte
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
:mod:`novespace_stream_data.receive`
====================================
   :synopsis: :mod:`novespace_stream_data.receive` is a python submodule to
              receive a stream from Novespace/AirZeroG during
              scientific research flights.

.. contents::

description
===========

`novespace_stream_data` gets the stream from Novespace/AirZeroG,
which is provided in scrientific research flights.

Available classes are:

.. autoclass:: NoSpaStream
   :members:
   :private-members:
   :special-members:

copyright + license
===================
:Author: Daniel Maier, Daniel Mohr, Thomas Villatte
:Date: 2025-11-04
:License: GPL-3.0-or-later
:Copyright: (C) 2025 Daniel Maier, Daniel Mohr, Thomas Villatte
"""

from .nove_space_stream import NoSpaStream

__all__ = ["NoSpaStream"]
