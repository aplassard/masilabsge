#!/usr/bin/env python
import argparse
import os
import time

# TODO:
#  Job Hold
#  Email

def parse_args():
    parser = argparse.ArgumentParser(description='Submit jobs to the MASI Lab Sun Grid Engine')
    parser.add_argument('--command',nargs="+",help='command to be submitted',required=True)
    parser.add_argument('--starting-dir',nargs=1,default=os.getcwd(),
        help='Directory to start script in. Default=`pwd`',required=False)
    parser.add_argument('--log-dir',nargs=1,default=os.path.join(os.getcwd(),'logs/'),
        help='Directory to write log files to. Default=`pwd`/logs/',required=False)
    parser.add_argument('--combine-output',default=False,action='store_true',
        required=False,help='Combine stdout and stderr into one file')
    parser.add_argument('--name',nargs=1,default=str(int(time.time())),
        help='Name for script. Default=current time',required=False)
    parser.add_argument('--pbs-file',nargs=1,default=False,
        help='File to save PBS file to. Default=Don\'t save',required=False)
    parser.add_argument('--memory',nargs=1,default='4G',
        help='Memory required for the cluster. Default=4G',required=False)
    args = parser.parse_args()
    return args

if __name__=='__main__':
    args = parse_args()
    memory = args.memory
    starting_dir = args.starting_dir
    name = args.name
    log_out_name = os.path.join(os.path.abspath(args.log_dir),"%s.out" % name)
    log_err_name = os.path.join(os.path.abspath(args.log_dir),"%s.err" % name)
    join_log = args.combine_output
    cmd = " ".join(args.command)

    lines = [
    "#!/bin/bash",
    "",
    "#$ -o %s " % log_out_name,
    "#$ -e %s " % log_err_name,
    "#$ -j y" if join_log else "#$ -j n",
    "#$ -l mem_free=%s" % memory,
    "#$ -l mem_token=%s" % memory,
    "#$ -l h_vmem=%s" % memory,
    "#$ -N %s" % name,
    "",
    "cd %s" % starting_dir,
    cmd,
    ]
    print "\n".join(lines)
