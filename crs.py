#!/usr/bin/env python
# encoding: utf-8
"""
crs.py

Script to work with CRS.
Contains code to download CRS list from the nationalrail website too.

Author: Prabhu Subramanian
"""

import sys, os
import urllib2, pickle
from BeautifulSoup import BeautifulSoup
from settings import *
import sqlite3

# Headers for spoofing Firefox
HEADERS = {
    "User-Agent" : "Mozilla/5.0 (Windows; U; Windows NT 6.1; pl; rv:1.9.1) Gecko/20090624 Firefox/3.5 (.NET CLR 3.5.30729)",
    "Accept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.5",
    "Accept-Language" : "en-us,en;q=0.5",
    "Accept-Charset" : "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
    "Keep-Alive" : "300",
    "Connection" : "keep-alive"
}

def recreateDB():
    """
    Method to recreate SQLite DB. 
    SQLite DB File is specified through the setting CRS_SQLITE_DB.
    """
    if os.path.exists(CRS_SQLITE_DB):
        os.remove(CRS_SQLITE_DB)
    conn = sqlite3.connect(CRS_SQLITE_DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE crs(station_name text, crs text UNIQUE)''')
    conn.commit()
    c.close()
    
def fetchFromUrl():
    """
    Method to fetch the CRS codes fresh from the CRS_URL specified in settings.
    """
    print "Retrieving CRS from %s" %CRS_URL
    req = urllib2.Request(CRS_URL, None, HEADERS)
    f = urllib2.urlopen(req)
    data = f.read()
    f.close()
    soup = BeautifulSoup(data)
    soup = soup.find("table", {"class" : "aztable sct"}).find("tbody").findAll('tr')
    if not soup:
        return
    recreateDB()
    conn = sqlite3.connect(CRS_SQLITE_DB)
    c = conn.cursor()
    cnt = 0
    for row in soup:
        sn = crs = None
        td1 = row.findNext('td')
        if td1:
            sn = td1.a.contents
            td2 = td1.findNext('td')
            if td2:
                crs = td2.contents
        if sn and crs:
            c.execute('INSERT INTO crs VALUES("%s", "%s")' %(sn, crs))
            cnt = cnt + 1
    conn.commit()
    c.close()
    print "Stored %d CRS codes in %s" %(cnt, CRS_SQLITE_DB)
            
def main():
    fetchFromUrl()

if __name__ == '__main__':
    main()
