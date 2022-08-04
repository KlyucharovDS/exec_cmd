import os
import subprocess
import sys
import time


class LogFile:
    def __init__(self, *, cmd: str, log_file: str):
        self.cmd = cmd
        self.file = None
        if log_file != '' and log_file is not None:
            time_date = time.strftime("\n\tDate: %Y-%m-%d \tTime: %H:%M:%S")
            date = time.strftime('%d_%m_%Y')
            log_file = os.path.abspath(log_file)
            # create log file if "log_file" content exist directory name
            if os.path.exists(os.path.dirname(log_file)):
                if os.path.isdir(log_file):
                    log_file = os.path.join(log_file, os.path.basename(os.path.normpath(date+'.log')))
                if os.path.isfile(log_file):
                    self.file = open(log_file, 'ab')
                else:
                    self.file = open(log_file, 'wb')
                self.print2log("\n-----------------------------------------------------------")
                self.print2log(f"\nLogging command \"{self.cmd}\"{time_date} ")
                self.print2log("\n-----------------------------------------------------------")
                self.print2log("\n")
            else:
                print('\n---------------------------------------------------------------------------')
                print(f'\tERROR!!! Path {os.path.dirname(log_file)} do not exist')
                print('----------------------------------------------------------------------------')

    def print(self,s:str):
        s = '\t' + s
        sys.stdout.buffer.write(bytes(s, "utf-8"))
        sys.stdout.flush()

    def write2log(self,s:str):
        if self.file and (s.find('\r') == -1):
            self.file.write(bytes(s, "utf-8"))

    def print2log(self, s: str):
        self.print(s)
        self.write2log(s)

    def close(self):
        if self.file:
            self.file.close()


log_file = None


def exec_cmd(cmd: (str, list), log_filename=None):
    global log_file
    if cmd is None or cmd == '':
        print('ERROR command empty!')
        return 1
    else:
        if isinstance(cmd, list):
            exit_code = 0
            for cmd_str in cmd:
                exit_code |= exec_cmd(cmd_str, log_filename)
            return exit_code
        elif isinstance(cmd, str):
            log_file = LogFile(cmd=cmd, log_file=log_filename)
            rsyncproc = subprocess.Popen(cmd,
                                         shell=True,
                                         stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE,
                                         )
            # read cmd output and print to console
            log_file.print(f'\n\t{cmd}:\n')
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
            return exitcode
        return 1

