# What is Transmission-Cleanup ?

Transmission-Cleanup is a repo with some short scripts written in Python, that removes completed torrents and read them without errors, from a running instance of *Transmission* (more info at http://www.transmissionbt.com/). 

## Why did I created this repository ?  

Well, I had two main reasons why I've created this repository:

1)	I have a server with [openmediavault](https://www.openmediavault.org/) installed and a transmission daemon running on. When the transmission finishes to download the torrents he doesn't remove those torrents from the queue. This is why I wrote the script `removedownloaded.py`. The second script `fixtransmission.py` is a fork from *nickcova/transmission-cleanup* with some bugs fixed
2)	It’s been a while since I’ve written something in Python, so I felt like practicing a little bit. 

## What do you need to use these scripts?

In order to use these scripts you need:
1)	A working *Linux* distro.
2)	*transmission-daemon* should be installed, configured and running.

## How to run these scripts?

In order to run these scripts you can choose one from the options bellow:
1) **crontab**: 
   * `echo "30 * * * * root python \`readlink -f removedownloaded.py\`" >> /etc/crontab`
   * `echo "0 * * * * root python \`readlink -f fixtransmission.py\`" >> /etc/crontab`
2) **command line**: 
   * `python removedownloaded.py`
   * `python fixtransmission.py`
