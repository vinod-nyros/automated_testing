#!/bin/sh

rm nohup.out
sudo -u joe nohup ssh -c blowfish -f -N -L 127.0.0.1:65432:127.0.0.1:5432 eracks.com
