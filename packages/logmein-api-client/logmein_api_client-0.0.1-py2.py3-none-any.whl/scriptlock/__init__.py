import sys
import os
import pwd
import tempfile
import json
import datetime
import logging


class Lock(object):
    """
        Class used to avoid running multiple instance of the same script
        A file is touch in /tmp, using filename of the script.
        Pid and other information are stored inside :)
    """
    def __init__(self):
        self.initialized = False

        # Get infos
        self.full_path = os.path.realpath(sys.argv[0])
        self.script_name = self.full_path.split('/')[-1]
        self.pid = os.getpid()
        self.user = pwd.getpwuid(os.getuid()).pw_name
        time_format = '%Y-%m-%d %H:%M:%S'
        self.start_time = datetime.datetime.now().strftime(time_format)

        # Remove weird caracters
        self.script_name = self.script_name.replace("/", "-")
        self.script_name = self.script_name.replace(":", "")
        self.script_name = self.script_name.replace("\\", "-")

        # Make it in a temp dir
        self.lock_file = os.path.normpath(
            tempfile.gettempdir() + '/' + self.get_lock_file())

        # If file exist warn
        if os.path.exists(self.lock_file):
            logging.warning("Another instance is already running, quitting.")
            self.read_lock_file()
            sys.exit(-1)
        else:
            # Write info to file
            self.write_lock_file()

        logging.debug("Lock acquired : %s" % (self.lock_file))
        self.initialized = True

    def get_lock_file(self):
        """Return lock file name according to script name
        """
        return '%s.lock' % self.script_name

    def write_lock_file(self):
        """Write lock with with script info
        """
        f_handler = open(self.lock_file, 'w')

        # Add extra
        f_handler.write(json.dumps({
            'script': self.script_name,
            'path': self.full_path,
            'pid': self.pid,
            'user': self.user,
            'start_time': self.start_time,
            'lock_file': self.lock_file}))

        f_handler.close()

    def read_lock_file(self):
        """Read content lock file
        """
        f_handler = open(self.lock_file, 'r')
        raw_data = f_handler.read()
        json_data = json.loads(raw_data)
        for key, value in json_data.items():
            logging.info('%-10s: %s' % (key, value))
        f_handler.close()

    def cleanup(self):
        if not self.initialized:
            return

        try:
            # Delete file
            if os.path.isfile(self.lock_file):
                os.unlink(self.lock_file)
                logging.debug("Lockfile %s released" % (self.lock_file))
            self.initialized = False

        except Exception as exception:
            logging.exception(exception)
