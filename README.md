## FingerprintSecurityTest

# Hardware
The following hardware was used through the development of this project:
Raspberry pi

ZhianTec ZFM-20 Fingerprinting Sensor
  Specs: http://microcontrollershop.com/product_info.php?products_id=7224
  
  
MAXREFDES117#: HEART-RATE AND PULSE-OXIMETRY MONITOR
  Specs and SetUp: https://www.maximintegrated.com/en/design/reference-design-center/system-board/6300.html

 
# Fingerprinter
The original scripts to execute operations on the fingerprinter can be found at:
https://sicherheitskritisch.de/2015/03/fingerprint-sensor-fuer-den-raspberry-pi-und-debian-linux-en/

# Master

To execute the security test, run the following command in the directory of the master_run.py file:

$ python2 master_run.py

# Troubleshooting
If you get errors, make sure:

1) You have the appropriate ports set in the master_run.py file. The ports for the fingerprinter and the LED can be found using the $ dmesg command
2) python2 compiler is downloaded onto your system
3) All of the connection are intact