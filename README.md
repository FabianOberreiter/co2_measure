# CO2_measure
Python script to monitor and log co2-concentration; run with 

`sudo python3 co2_detect.py [-h] [-t TIME_SECONDS] [-i INTERVAL] [-c] [-l] [-f LOG_FILE]`



optional arguments:



| option                               | help - text
|:------------------------------------ | :----------|
| -h, --help                           | show this help message and exit
| -t TIME_SECONDS, --time TIME_SECONDS | set the time (nr of seconds) that she script is supposed to run for; negative values for indefinite
| -i INTERVAL, --interval INTERVAL     | set the interval (nr of seconds) for measurements
| -c, --console-out                    | if set, the output should be printed on the console
| -l, --log                            | specify if data should be logged
| -f LOG_FILE, --file LOG_FILE         | specify a file to log to; file gets overwritten if already exists

