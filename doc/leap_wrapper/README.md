# Leap Motion setup to python 3.7#

Download the files:
- LeapDeveloperKit_2.3.1+31549_linux.tgz
- LeapDeveloperKit_linux-hotfix_2.3.1+33747_linux.tgz
- Leap.i.diff

## 1. Dependencies ##

- Install the packages:

```
sudo apt-get install libgl1-mesa-dri libgl1-mesa-glx
```

- If you don't have the file /etc/init.d/leapd, create it:

```
sudo nano /lib/systemd/system/leapd.service
```

- Put the following code in the file leapd.service:

```
[Unit]
Description=LeapMotion Daemon
After=syslog.target

[Service]
Type=simple
ExecStart=/usr/sbin/leapd

[Install]
WantedBy=multi-user.target
```

- Then:
```
sudo ln -s /lib/systemd/system/leapd.service /etc/systemd/system/leapd.service
sudo systemctl daemon-reload
sudo dpkg --install Leap-2.3.1+31549-x64.deb
```

## 2. Installation ##

- Extract files:

```
tar -xaf LeapDeveloperKit*31549*.tgz
tar -xaf LeapDeveloperKit*33747*.tgz
```

- Install client software:

``` 
cd LeapDeveloperKit*33747*
sudo dpkg -i Leap*x64.deb
```

-  Create Leap Motion SDK

```
cd ../LeapDeveloperKit*31549*/LeapSDK
mkdir python3.7_project
cp -a lib/x64/libLeap.so lib/Leap.py samples/Sample.py python3.7_project/
sudo apt-get install swig g++ libpython3.7-dev
2to3-3.7 -nw python3.7_project/Sample.py
patch -p0 < Leap.i.diff
swig -c++ -python -o /tmp/LeapPython.cpp -interface LeapPython include/Leap.i
g++ -fPIC -I/usr/include/python3.7m -I./include /tmp/LeapPython.cpp lib/x64/libLeap.so -shared -o python3.7_project/LeapPython.so
cd python3.7_project/
LD_PRELOAD=./libLeap.so python3.7 Sample.py
```
