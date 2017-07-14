#!/usr/bin/env python3
#
# Copyright (C) 2017 ShadowMan
#
import os
import sys
import atexit
import signal


class DaemonError(Exception):
    pass


class Daemon(object):

    def __init__(self, pid_file: str, stdin: str='/dev/null',
                 stdout: str='/dev/null', stderr: str='/dev/null'):
        self.debug = False
        self.stdin = stdin  # type: str
        self.stdout = stdout  # type: str
        self.stderr = stderr  # type: str
        if not isinstance(pid_file, str):
            raise DaemonError('pid file muse be specify')
        self.pid_file = os.path.abspath(pid_file)  # type: str

    def run_forever(self, *, debug=False):
        self.debug = debug
        if os.path.isfile(self.pid_file) and not self.debug:
            raise DaemonError('pid file already exists, server running?')
        self.start_deamon()

    def start_deamon(self):
        if os.name == 'nt' or not hasattr(os, 'fork'):
            if self.debug is False:
                raise DaemonError('Windows does not support fork')
            else:
                return

        # double fork create a deamon
        try:
            pid = os.fork()  # fork #1
            if pid > 0:  # parent exit
                exit()
        except OSError as e:
            raise DaemonError('Fork #1 error occurs, reason({})'.format(e))

        os.chdir('/')
        os.setsid()
        os.umask(0)

        try:
            pid = os.fork()  # fork #2
            if pid > 0:  # parent exit
                exit()
        except OSError as e:
            raise DaemonError('Fork #2 error occurs, reason({})'.format(e))

        # redirect all standard file descriptor
        sys.stdout.flush()
        sys.stderr.flush()
        _stdin = open(self.stdin, 'r')
        _stdout = open(self.stdout, 'a')
        # if require non-buffer, open mode muse be `b`
        _stderr = open(self.stderr, 'wb+', buffering=0)
        os.dup2(_stdin.fileno(), sys.stdin.fileno())  # close fd2 and duplicate
        os.dup2(_stdout.fileno(), sys.stdout.fileno())
        os.dup2(_stderr.fileno(), sys.stderr.fileno())

        # terminal signal
        signal.signal(signal.SIGTERM, self.signal_handler)
        # kill signal
        signal.signal(signal.SIGILL, self.signal_handler)
        # system interrupt
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        # register function at exit
        atexit.register(self.remove_pid_file)
        # write pid file
        with open(self.pid_file, 'w') as fd:
            fd.write('{pid}\n'.format(pid=os.getpid()))

    def signal_handler(self, signum, frame):
        self.remove_pid_file()
        exit()

    def remove_pid_file(self):
        if os.path.exists(self.pid_file):
            os.remove(self.pid_file)
