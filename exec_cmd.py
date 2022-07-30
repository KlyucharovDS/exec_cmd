import os
import re
import subprocess
import sys


def print2log(s: str):
    sys.stdout.buffer.write(bytes(s, "utf-8"))
    sys.stdout.flush()

def exec_cmd(cmd:(str,list)):
    if isinstance(cmd, list):
        for cmd_str in cmd:
            exec_cmd(cmd_str)
    elif isinstance(cmd, str):
        print('-------------------------------------------')
        print(f"{cmd}")
        rsyncproc = subprocess.Popen(cmd,
                                     shell=True,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     )
        # read cmd output and print to console
        while True:
            next_line = rsyncproc.stdout.readline().decode("utf-8")
            if not next_line:
                break
            print2log(f"\t{next_line}")
        # wait until process is really terminated
        exitcode = rsyncproc.wait()
        # check exit code
        if exitcode == 0:
            print("done")
        else:
            print("WARNING: looks like some error occured")
    print('-------------------------------------------')
# ------------------------------------------------------
# Main program
if __name__ == '__main__':
    cmds =[
        "ls result",
        'rm  result/*',
        "ls result",
        'rsync -aP test_C result',
        'ls result',
    ]
    exec_cmd(cmds)

