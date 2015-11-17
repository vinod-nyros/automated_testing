JJW 7/5/14 - OLD:
Note: as of October 2013, Apache was deprecated in favor of nginx -

SEE THE nginx CONF README

- - - - -

JJW 9/20/13

This directory contains the apache configurations for eRacks production - eracks10

To use:

 - symlink the files into /etc/apache2/sites-available
 - run a2ensite to enable


Zope is NO LONGER used or installed - its all Django.  
Be sure to set up PG DB backups and run collectstatic.



JJW 2/4/12 - OLD

This directory contains the apache configurations for eRacks production - hybrid Zope/Django


To use:

 - symlink the files into /etc/apache2/sites-available
 - run a2ensite to enable


Notes:

 - it assumes ProxyPass is enabled via mod_proxy
 - ProxyVia is required for Zope to work properly & gen reverse URLs
