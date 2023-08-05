#!/usr/bin/env python
#
# LoggingModules.py
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA  02111-1307  USA

from .modules import MITRE
from .modules import JSON
from .modules import MongoDB
from .modules import ElasticSearch
from .modules import HPFeeds

LoggingModules = {
    'maec11'        : MITRE.MAEC11,
    'json'          : JSON.JSON,
    'mongodb'       : MongoDB.MongoDB,
    'elasticsearch' : ElasticSearch.ElasticSearch,
    'hpfeeds'       : HPFeeds.HPFeeds
}
