# -*- coding: utf-8 -*-
#
#   Copyright 2013 Grigoriy Kramarenko <root@rosix.ru>
#
#   This file is part of BWP.
#
#   BWP is free software: you can redistribute it and/or
#   modify it under the terms of the GNU Affero General Public License
#   as published by the Free Software Foundation, either version 3 of
#   the License, or (at your option) any later version.
#
#   BWP is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public
#   License along with BWP. If not, see
#   <http://www.gnu.org/licenses/>.
#

VERSION = (0, 7, 0)


def get_version(*args, **kwargs):
    return '%d.%d.%d' % VERSION


def get_docs_version(*args, **kwargs):
    return '%d.%d' % VERSION[:2]


__version__ = get_version()

default_app_config = 'bwp.apps.BwpConfig'
