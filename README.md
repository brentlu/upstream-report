# upstream-report

Design for Chrome MM team to collect patch submission data from multiple source.

Usage:
python3 upstream_report.py -c <cfg file> -u <github user name> -t <github user token>

ex. python3 ./upstream_report.py -c chrome-mm.cfg -u brentlu -t ghp_XXXXXXXXXXXXXXXXXXXX

You may need to install gitpython and openpyxl before running the script:
$ sudo apt install python3-pip
$ pip install gitpython
$ pip install openpyxl
