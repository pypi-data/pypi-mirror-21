# -*- coding: utf-8 -*-
#
#  bwp/contrib/devices/drivers/__init__.py
#
#  Copyright 2013 Grigoriy Kramarenko <root@rosix.ru>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
from ShtrihM import ShtrihFRK, ShtrihFRK2
from ICPDAS import ICPi7000, ICPi7000Dummy
from Zonerich import ZonerichIP, ZonerichIPDummy

DRIVER_CLASSES = {
    'Shtrih-M Fiscal Register': ShtrihFRK,
    'Shtrih-M Fiscal Register v2': ShtrihFRK2,
    'Zonerich TCP/IP Printer': ZonerichIP,
    'Zonerich TCP/IP Printer Dummy': ZonerichIPDummy,
    'ICP DAS I-7000/M-7000 DIO': ICPi7000,
    'ICP DAS I-7000/M-7000 DIO Dummy': ICPi7000Dummy,
}
