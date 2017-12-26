#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Transmission Error Fix
#  (fixtransmission.py)
#  
#  Copyright 2017 Ruslan Rotaru <rotarur.social.apps@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
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

import time
import subprocess

def listTorrents():
    try:
        commandResult = subprocess.check_output(["transmission-remote","--auth", "transmission:transmission", "-l"])
    except CalledProcessError:
        dateAndTime = time.strftime("%H:%M:%S") + " " + time.strftime("%d/%m/%Y")
        print(dateAndTime + " ERROR: something went wrong checking the torrents listing.") 
        return -1
    return commandResult

def getTorrentInfo(item):
    try:
        commandResult = subprocess.check_output(["transmission-remote","--auth", "transmission:transmission", "-t", item, "-i"])
    except CalledProcessError:
        dateAndTime = time.strftime("%H:%M:%S") + " " + time.strftime("%d/%m/%Y")
        print(dateAndTime + " ERROR: something went wrong checking the torrent info.") 
        return -1
    return commandResult

def removeTorrent(item):
    try:
        commandResult = subprocess.check_output(["transmission-remote","--auth", "transmission:transmission", "-t", item, "--remove"])
    except CalledProcessError:
        dateAndTime = time.strftime("%H:%M:%S") + " " + time.strftime("%d/%m/%Y")
        print(dateAndTime + " ERROR: something went wrong removing torrent.") 
        return -1
    return commandResult

def addTorrent(magnet):
    try:
        commandResult = subprocess.check_output(["transmission-remote","--auth", "transmission:transmission", "--add", magnet])
    except CalledProcessError:
        dateAndTime = time.strftime("%H:%M:%S") + " " + time.strftime("%d/%m/%Y")
        print(dateAndTime + " ERROR: something went wrong adding torrent.") 
        return -1
    return commandResult


def sendEmail(msg):
    try:
        ps = subprocess.Popen(('echo', msg), stdout=subprocess.PIPE)
        output = subprocess.check_output(('mail', '-s', 'Torrents Fixed', "rotarur.adverts@gmail.com"), stdin=ps.stdout)
        ps.wait()
    except OSError:
        dateAndTime = time.strftime("%H:%M:%S") + " " + time.strftime("%d/%m/%Y")
        print(dateAndTime + " ERROR: something went wrong with 'mail'. " + output)
        return -1
     
def main():

    splitResult = listTorrents().split("\n")

    # Remove items which are just empty strings
    while True:
        try:
            splitResult.remove("")
        except ValueError:
            # Insert error message here
            break

    # Remove first and last items so the list only contains torrent info.
    # If the length of the list is smaller than 2, just exit.
    if len(splitResult) > 2:
        splitResult.pop(0)
        splitResult.pop()
    else:
        return 0

    # For the remaining items, check if any of them does not contain '100%',
    # if there is an error string add them to a error torrents list.
    errorTorrents = []
    for item in splitResult:
        if not "100%" in item:
            torrentId = item.split()[0].rstrip("*")
            torrent = getTorrentInfo(torrentId)
            if "Error" in torrent:
                torrent = torrent.split()
                for item in torrent:
                    if "magnet" in item:
                        errorTorrents.append((torrentId, item))

    # For each torrentId in the Torrents list, save the magnet link
    # remove the torrent and readd it from magnet link
    emailMessage = "The following torrents were readded: \n"
    torrentsFixed = False
    
    for item in errorTorrents:
        commandResultRemove = removeTorrent(item[0])
        commandAdd = addTorrent(item[1])
        emailMessage += commandResultRemove.rstrip() + ", Id = "  + item[0] + ", Torrent Name = " + item[1] + "\n"    
        if "success" in commandResultRemove:
            torrentsFixed = True

    if torrentsFixed == True:
        sendEmail(emailMessage)
        
    return 0

if __name__ == '__main__':
    main()

