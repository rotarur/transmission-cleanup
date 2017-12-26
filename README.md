# What is Transmission-Cleanup?

Transmission-Cleanup is a repo with some short scripts written in Python, that removes completed torrents and readd those ones with some error, from a running instance of *Transmission* (more info at http://www.transmissionbt.com/). 

###Why did I write these scripts?  

Well, I had two main reasons why I wrote this script:

1)	I have a server with openmediavault installed and a transmission daemon running on. When the transmission finishes to download the torrents he is not removing those torrents from queue. This is why i wrote the script `removedownloadedd.py`. The second script `fixtransmission.py` is a fork from *nickcova/transmission-cleanup* with some bugs fixed
2)	It’s been a while since I’ve written something in Python, so I felt like practicing a little bit. 

### What do you need to use these scripts?

In order to use these scripts you need:
1)	You need to be working on a *Linux* distro.
2)	*transmission-daemon* should be installed, configured and running.

###How to run these scripts?

In order to run these scripts you can choose one option:
1) crontab: `echo "*/30 * * * * root python `readlink -f removedownloadedd.py`" >> /etc/crontab`
2) command line: python removedownloadedd.py
