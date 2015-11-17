# from: 
# root@eracks-production-zope:/home/sysadmin/django_eracks/zope# mkdir eracksprod

# do: (same as --bind)
# root@eracks-production-zope:/home/sysadmin/django_eracks/zope# mount -B /var/lib/zope2.10/instance/eracksprod/ eracksprod

cd /home/sysadmin/django_eracks/zope
mount -B /var/lib/zope2.10/instance/eracksprod/ eracksprod


# svn add zope/eracksprod/Extensions/ --parents
