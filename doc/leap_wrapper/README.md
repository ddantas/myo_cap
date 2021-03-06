# Leap Motion SDK 2.3.1 setup to python 3.7 #

Download the files:
- LeapDeveloperKit_2.3.1+31549_linux.tgz (at https://drive.google.com/file/d/1hoI6lLrYuk5U4TdiEWrbKYNq9NrEPoBq/view?usp=sharing)
- LeapDeveloperKit_linux-hotfix_2.3.1+33747_linux.tgz (at https://drive.google.com/file/d/1m9wo-nC4tkubOtHWYDED7r9XGPjnPyqr/view?usp=sharing)
- Leap.i.diff

## 1. Dependencies ##

- Install the packages:

```
sudo apt-get install libgl1-mesa-dri libgl1-mesa-glx
sudo apt-get install swig g++ libpython3.7-dev
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
sudo leapd
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
sudo systemctl daemon-reload or sudo service leapd restart
```

-  Create Leap Motion wrapper

```
cd ../LeapDeveloperKit*31549*/LeapSDK
mkdir python3.7_project
cp -a lib/x64/libLeap.so lib/Leap.py samples/Sample.py python3.7_project/
2to3-3.7 -nw python3.7_project/Sample.py
patch -p0 < Leap.i.diff
swig -c++ -python -o /tmp/LeapPython.cpp -interface LeapPython include/Leap.i
g++ -fPIC -I/usr/include/python3.7m -I./include /tmp/LeapPython.cpp lib/x64/libLeap.so -shared -o python3.7_project/LeapPython.so
cd python3.7_project/
LD_PRELOAD=./libLeap.so python3.7 Sample.py
```
# Leap Motion SDK 2.3.1 for Windows #

Download the file:
- Leap_Motion_SDK_Windows_2.3.1 (https://drive.google.com/file/d/1y5BmwmOZeAhrRCbbuTK28OVA80gQvlsQ/view?usp=sharing)
