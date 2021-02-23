#!/usr/bin/env python3

import time
import argparse
from datetime import datetime as dt

# check if mh_z19 module is present
try:
    import mh_z19
    mh_z19.read()
    model_loaded = True
except:
    model_loaded = False
    print('\nERROR - Using mock model; module mh_z19 cannot be found!')
    print('ERROR - Make sure to run the script with sudo privledges!')


def get_sensor_data():
    if model_loaded:
        return mh_z19.read_all()
    else:
        return {'co2': 561, 'temperature': 22.1}


class co2_logger():

    def __init__(self, runtime, interval, console_out, log, logfile):
        
        self.start_time = dt.now()
        self.run_indefinate = runtime < 0
        if not self.run_indefinate:
            self.end_time = self.start_time + dt.timedelta(seconds=self.runtime)
        
        self.interval = interval
        self.to_console = console_out
        
        self.log = log
        if self.log:
            self.logfile = open(logfile, 'w+')
            self.logfile.write('\t'.join(['timestamp', 'temperature', 'co2']) + '\n')
        
        self.save_block_size = 10
        self.measurement_log = []
        
        self.run()
    
    def take_measure(self):
        # do 3 meassurements and average them
        timestamp = dt.now().strftime("%Y-%m-%d-%H:%M:%S")
        
        if self.interval < 10:
            values = get_sensor_data()
        else:
            val1 = get_sensor_data()
            time.sleep(1)
            val2 = get_sensor_data()
            time.sleep(1)
            val3 = get_sensor_data()
        
            values = dict_average([val1, val2, val3])

        log_data = (timestamp, 
                    f'{values["temperature"]:.1f}', 
                    f'{int(values["co2"])}'
                    )
        self.measurement_log.append(log_data)
        return log_data
    
    def print_header(self):
        ts = 'timestamp'
        temp = 'temperature'
        co2 = 'co2-ppm'
        print(f'\n{ts:>19} {temp:>14} {co2:>7}')
    
    def print_log_line(self, measurement):
        print(f'{measurement[0]:>19} {measurement[1]:>13}° {measurement[2]:>7}')
    
    def write_block(self):
        if self.log:
            for log_line in self.measurement_log:
                self.logfile.write('\t'.join(log_line) + '\n')
            self.logfile.flush()
        
        if self.to_console:
            self.print_header()
    
    def run(self):
        self.write_block()
        current_block_size = 1
        while self.run_indefinate or dt.now() < self.end_time:
        
            try:
                measurement = self.take_measure()
                if self.to_console:
                    self.print_log_line(measurement)
                
                if not (current_block_size % self.save_block_size): # every nth element
                    self.write_block()
                    self.measurement_log = []
            
                current_block_size = (current_block_size + 1) % self.save_block_size
            
            except Exception as e:
                print(f'Failed to log at {dt.now().strftime("%Y-%m-%d-%H:%M:%S")}')
                print(e)
            
            time.sleep(self.interval)


def dict_average(dicts):
    all_keys = set([k for d in dicts for k in d.keys()])
    
    avg_dict = {}
    for key in all_keys:
        avg_dict[key] = sum(map(lambda d: d[key], dicts)) / len(dicts)
    return avg_dict


def get_default_filename():
    return dt.now().strftime("co2_log_%Y-%m-%d-%H_%M_%S.csv")


def create_parser():
    parser = argparse.ArgumentParser()
   
    parser.add_argument('-t', '--time', action='store', default = -1, dest = 'time_seconds', type = int,
        help="set the time (nr of seconds) that she script is supposed to run for; negative values for indefinite")
        
    parser.add_argument('-i', '--interval', action='store', default = 5, dest = 'interval', type = int,
        help="set the interval (nr of seconds) for measurements")
        
    parser.add_argument('-c', '--console-out', action='store_true', dest = 'console_flag', 
        help="flag if the output should also be printed on the console")
        
    parser.add_argument('-l', '--log', action='store_true', dest = 'log_flag', 
        help="specify if data should be logged")
        
    parser.add_argument('-f', '--file', action='store', default = get_default_filename(), dest = 'log_file', 
        help="specify a file to log to; file gets deleted if alreaedy exists")
    
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    co2_logger(args.time_seconds, args.interval, args.console_flag, args.log_flag, args.log_file)


if __name__ == '__main__':
    main()
