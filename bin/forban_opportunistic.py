import glob
import os.path
import sys
import string
import base64
import time
import ConfigParser
import re
config = ConfigParser.RawConfigParser()
config.read("../cfg/forban.cfg")
forbanpath = config.get('global','path')
forbanshareroot = config.get('forban','share')

sys.path.append(forbanpath+"lib/")
import index
import loot
import fetch

if not config.get("global","mode") == "opportunistic":
    print "not configured in opportunistic mode"
    exit(1)

ofilter = config.get('opportunistic','filter')
print "applied regexp filter: %s" % ofilter
refilter = re.compile(ofilter, re.I)
discoveredloot = loot.loot()
allindex = index.manage()
allindex.build()

while(1):

    for uuid in discoveredloot.listall():
        # fetch the index of all discovered and recently announced loots
        # allowing to compare local loot to announced loot
        if discoveredloot.exist(uuid) and discoveredloot.lastannounced(uuid):
            allindex.cache(uuid)

        missingfiles = allindex.howfar(uuid)
        if not missingfiles or (discoveredloot.whoami() == uuid):
            print "missing no files with %s (%s)" % (discoveredloot.getname(uuid),uuid)
        elif not discoveredloot.lastannounced(uuid):
            print "%s (%s) not seen recently" % (discoveredloot.getname(uuid),(uuid))
        else:
            for missedfile in missingfiles:
                if re.search(refilter, missedfile):
                    sourcev4 = discoveredloot.getipv4(uuid)
                    url =  """http://%s:12555/s/?g=%s&f=b64""" % (sourcev4, base64.b64encode(missedfile))
                    localfile = forbanshareroot + "/" + missedfile
                    print "from %s fetching %s to be saved in %s" % (uuid,url,localfile)
                    fetch.urlget(url,localfile)
                allindex.build()

    time.sleep(100)
