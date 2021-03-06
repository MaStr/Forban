# Forban - a simple link-local opportunistic p2p free software
#
# For more information : http://www.foo.be/forban/
#
# Copyright (C) 2009-2010 Alexandre Dulaunoy - http://www.foo.be/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import ConfigParser

def guesspath():
    pp = os.path.realpath(sys.argv[0])
    lpath = os.path.split(pp)
    bis = os.path.split(lpath[0])
    return bis[0]

config = ConfigParser.RawConfigParser()
config.read(os.path.join(guesspath(),"cfg","forban.cfg"))

try: 
    disable_ipv6 =  config.get('global','disabled_ipv6')
except ConfigParser.NoOptionError:
    disable_ipv6 = 0

try:
    forbanpath = config.get('global','path')
except ConfigParser.NoSectionError:
    print "Forban config file is missing or incorrect"
    print "You should go into ../cfg/ and cp forban.cfg-sample forban.cfg"
    print "In any case, Forban should be able to work even without the config file"
    forbanpath = os.path.join(guesspath())
except ConfigParser.NoOptionError:
    forbanpath = os.path.join(guesspath())

forbanpathlib = os.path.join(forbanpath,"lib")
sys.path.append(forbanpathlib)

import discover


if __name__ == "__main__":

    while 1:
        HOST, PORT = ("", 12555)
        server = discover.UDPServer((HOST, PORT), discover.MyUDPHandler)
	if disable_ipv6 == "1":
              server.setIPv6 ( 0 )
	else:
              server.setIPv6 ( 1 )
        server.serve_forever()

