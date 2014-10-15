#!/usr/bin/env python
import argparse
import os
import time

def parse_args():
    parser = argparse.ArgumentParser(description='Submit jobs to the MASI Lab Sun Grid Engine')
    parser.add_argument('--command',nargs="+",help='command to be submitted',required=True)
    parser.add_argument('--starting-dir',nargs=1,default=os.getcwd(),
        help='Directory to start script in. Default=`pwd`',required=False)
    parser.add_argument('--log-dir',nargs=1,default=os.path.join(os.getcwd(),'logs/'),
        help='Directory to write log files to. Default=`pwd`/logs/',required=False)
    parser.add_argument('--combine-output',default=False,action='store_true',
        required=False,help='Combine stdout and stderr into one file')
    parser.add_argument('--name',nargs=1,default=str(time.time()),
        help='Name for script. Default=current time',required=False)
    parser.add_argument('--pbs-file',nargs=1,default=False,
        help='File to save PBS file to. Default=Don\'t save',required=False)
    parser.add_argument('--memory',nargs=1,default='4G',
        help='Memory required for the cluster. Default=4G',required=False)
    args = parser.parse_args()

if __name__=='__main__':
    args = parse_args()
