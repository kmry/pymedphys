# Copyright (C) 2018 CCA Health Care

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version (the "AGPL-3.0+").

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License and the additional terms for more
# details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# ADDITIONAL TERMS are also included as allowed by Section 7 of the GNU
# Affrero General Public License. These aditional terms are Sections 1, 5,
# 6, 7, 8, and 9 from the Apache License, Version 2.0 (the "Apache-2.0")
# where all references to the definition "License" are instead defined to
# mean the AGPL-3.0+.

# You should have received a copy of the Apache-2.0 along with this
# program. If not, see <http://www.apache.org/licenses/LICENSE-2.0>.


"""This is a placeholder file awaiting the required go ahead for public
release.
"""


import hashlib

import attr


@attr.s
class DeliveryData(object):
    monitor_units = attr.ib()
    gantry = attr.ib()
    collimator = attr.ib()
    mlc = attr.ib()
    jaw = attr.ib()


def hash_file(filename, dot_feedback=False):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(filename, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)

    if dot_feedback:
        print(".", end="", flush=True)

    return hasher.hexdigest()


@attr.s
class Header(object):
    machine = attr.ib()
    date = attr.ib()
    timezone = attr.ib()
    field_label = attr.ib()
    field_name = attr.ib()
