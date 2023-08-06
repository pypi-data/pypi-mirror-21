# This file is part of boatd, the Robotic Sailing Boat Daemon.
#
# Copyright (C) 2013-2016 Louis Taylor <louis@kragniz.eu>
#
# boatd is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# boatd is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
import subprocess
import threading

from .color import color


log = logging.getLogger(__name__)


class LogPipe(threading.Thread):
    def __init__(self, level, name):
        threading.Thread.__init__(self)
        self.name = name
        self.daemon = True
        self.level = level
        self.fd_read, self.fd_write = os.pipe()
        self.pipe_reader = os.fdopen(self.fd_read)
        self.start()

    def fileno(self):
        return self.fd_write

    def run(self):
        for line in iter(self.pipe_reader.readline, ''):
            logging.log(self.level, self.name + ': ' + line.strip('\n'))

        self.pipe_reader.close()

    def close(self):
        os.close(self.fd_write)


class Behaviour(object):
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename
        self.running = False
        self.process = None
        self.logpipe = None

    def start(self):
        log.info('starting behaviour {} from {}'.format(
            color(self.name, 34),
            color(self.filename, 37)))

        self.logpipe = LogPipe(logging.INFO, self.name)
        self.process = subprocess.Popen([self.filename],
                                        stdout=self.logpipe,
                                        stderr=self.logpipe)
        self.running = True

    def end(self):
        '''
        Send a SIGTERM signal (15) to the behaviour script to nicely ask it to
        stop.
        '''

        log.info('stopping behaviour {}'.format(self.name))

        if self.running:
            self.process.terminate()
            self.process.wait()
            self.running = False
            self.logpipe.close()


class BehaviourManager(object):
    def __init__(self):
        self.behaviours = []
        self.active_behaviour = None

    def add(self, behaviour):
        self.behaviours.append(behaviour)

    def list(self):
        return [b.name for b in self.behaviours]

    def start_behaviour_by_name(self, name):
        for behaviour in self.behaviours:
            if behaviour.name == name:
                behaviour.start()
                self.active_behaviour = behaviour.name

    def stop(self):
        for behaviour in self.behaviours:
            if behaviour.running:
                behaviour.end()
                self.active_behaviour = None
