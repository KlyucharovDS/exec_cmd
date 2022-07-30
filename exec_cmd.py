import os
import subprocess
import sys
import time

class LogFile:
    def __init__(self,*, cmd: str, log_file:str):
        self.file =None
        if log_file != '' and log_file is not None:
            t = time.strftime("%Y-%m-%dT%H:%M:%S")
            log_file = os.path.abspath(log_file)
            #create log file
            if os.path.isdir(log_file):
                log_file = os.path.join(log_file, os.path.basename(os.path.normpath(cmd)), t + '.log')
            #test exist file
            if not os.path.isfile(log_file):
                print("---------------------------------------")
                print(f"\tERROR log file name! {log_file}")
                print("---------------------------------------")
                return
            self.file = open(log_file, 'wb')
            self.print2log("\n-----------------------------------------------------------")
            self.print2log(f"\nLogging command \"{cmd}\" time: {t} ")
            self.print2log("-----------------------------------------------------------")
            self.print2log("\n")

    def print2log(self, s:str):
        sys.stdout.buffer.write(bytes(s, "utf-8"))
        sys.stdout.flush()
        # '\r' has no effect for file write
        if self.write_logfile and (s.find('\r') == -1):
            self.write_logfile.write(bytes(s, "utf-8"))

    def close(self):
        if self.file: self.file.close()

log_file = None
def exec_cmd(cmd:(str,list), filename=None):
    global log_file
    if isinstance(cmd, list):
        for cmd_str in cmd:
            log_file = LogFile(cmd=cmd_str, log_file=filename)
            exec_cmd(cmd_str,filename)
    elif isinstance(cmd, str):
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
            log_file.print2log(f"\t{next_line}")
        # wait until process is really terminated
        exitcode = rsyncproc.wait()
        # check exit code
        if exitcode == 0:
            log_file.print2log("done")
        else:
            log_file.print2log("WARNING: looks like some error occured")
        log_file.print2log("\n")
        log_file.close()
# ------------------------------------------------------
# Main program
# @todo create test!
if __name__ == '__main__':
    cmds =[
        "ls result",
        'rm  result/*',
        "ls result",
        'rsync -aP test_C result',
        'ls result',
    ]
    exec_cmd(cmds)

