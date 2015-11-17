This directory contains an "instance home" for the Zope application
server.  It contains the following directories:

  bin/         Scripts used to control the Zope instance
  etc/         Configuration files
  Extensions/  Python sources for External Methods
  log/         Log files
  lib/python/  Installed Python packages specific to the instance
  Products/    Installed Zope Products specific to the instance
  var/         Run-time data files, including the object database

NOTES JJW 2/4/12:

- Only the Extensions/ dir is in the repo.

- Dependencies: Products requuires FSSession, ZPsycopgDA, LocalFS
  - look for more recent versions when reinstalling

- /etc is a symlink, some reconf mayt be required when reinstalling

