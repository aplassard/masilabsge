#!/usr/bin/env python
import argparse
import os
import time
import tempfile

# TODO:
#  Job Hold
#  Email

def parse_args():
    t=str(int(time.time()))
    parser = argparse.ArgumentParser(description='Submit jobs to the MASI Lab Sun Grid Engine')
    parser.add_argument('--command',nargs="+",help='command to be submitted',required=True)
    parser.add_argument('--starting-dir',default=os.getcwd(),
        help='Directory to start script in. Default=`pwd`',required=False)
    parser.add_argument('--log-dir',default=os.path.join(os.getcwd(),'logs/'),
        help='Directory to write log files to. Default=`pwd`/logs/',required=False)
    parser.add_argument('--combine-output',default=False,action='store_true',
        required=False,help='Combine stdout and stderr into one file')
    parser.add_argument('--name',default="job_%s"%t,
        help='Name for script. Default=current time',required=False)
    parser.add_argument('--pbs-file',default=False,
        help='File to save PBS file to. Default=Don\'t save',required=False)
    parser.add_argument('--memory',default='4G',
        help='Memory required for the cluster. Default=4G',required=False)
    parser.add_argument('--execute-bashrc',default=False,action='store_true',
        help='Execute .bashrc file at beginning of script')
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
    " ",
    "#$ -o %s " % log_out_name,
    "#$ -e %s " % log_err_name,
    "#$ -j y" if join_log else "#$ -j n",
    "#$ -l mem_free=%s" % memory,
    "#$ -l mem_token=%s" % memory,
    "#$ -l h_vmem=%s" % memory,
    "#$ -N %s" % name,
    " ",
    ". ~/.bashrc" if args.execute_bashrc else None,
    "cd %s" % starting_dir,
    cmd,
    " ",
    ]

    lines = filter(lambda x: x, lines)
    f = open(os.path.abspath(args.pbs_file),'w',0) if args.pbs_file else tempfile.NamedTemporaryFile(delete=True,mode='w',bufsize=0)
    f.write("\n".join(lines))
    os.system('qsub %s' % f.name)
    f.close()
