# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .adapter import Adapter


class C1700_MB_1FE(Adapter):

    """
    Integrated 1 port FastEthernet adapter for c1700 platform.
    """

    def __init__(self):

        super().__init__(interfaces=1, wics=2)

    def __str__(self):

        return "C1700-MB-1FE"

    def removable(self):

        return False
