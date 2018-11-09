import functools
import logging
import time
import threading


class ThreadHandler:
    def __init__(self, target, name=None,
                 parent_logger=logging, interval=3, suppress_out=False, auto_restart=True):
        """
        Initialize a ThreadHandler.

        :param target: the child function to run, should be either a functools.partial or lambda
        :param name: the name of the thread; default is name of function or pointer location
        :param parent_logger: a logging object (ex. GPS); default 'root'
        :param interval: amount of time between checking the status of the child function; default 3s
        :param suppress_out: suppresses the logging of messages; default False
        :param auto_restart: whether or not to automatically restart the thread
        """

        self.target = target

        if name is None:
            if type(target) == functools.partial:
                self.name = target.func.__name__
            else:
                self.name = "thread_" + str(id(self))
        else:
            self.name = name

        self.parent_logger = parent_logger
        self.interval = interval
        self.suppress_out = suppress_out
        self.auto_restart = auto_restart
        self.is_active = True
        self.is_alive = False

    def start(self):
        """
        Start the ThreadHandler. This function actually starts a threading.Thread, with the run() method as the target.
        """
        threading.Thread(target=self.run, name=self.name, daemon=True).start()

    def run(self):
        def start():
            while True:
                if self.is_active:
                    if not self.suppress_out: self.parent_logger.info("'%s' thread started" % self.name)
                    try:
                        self.target()
                    except BaseException as e:
                        if not self.suppress_out: self.parent_logger.exception(str(e) + ", restarting '%s'" % self.name)
                        if not self.auto_restart:
                            self.is_active = False
                    else:
                        if not self.suppress_out: self.parent_logger.info("Bad thread, restarting '%s'" % self.name)
                        if not self.auto_restart:
                            self.is_active = False
                time.sleep(self.interval)

        return start()

    def resume(self):
        """
        Resume the ThreadHandler.
        """
        if not self.suppress_out: self.parent_logger.info("'%s' thread resumed" % self.name)
        if not self.auto_restart:
            self.is_active = True

    def pause(self):
        """
        Pause the ThreadHandler.
        """
        if not self.suppress_out: self.parent_logger.info("'%s' thread paused" % self.name)
        if not self.auto_restart:
            self.is_active = False