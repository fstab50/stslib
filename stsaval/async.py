"""
Summary:
    Non-blocking event caller

Module Attributes:
    cycle (int): duration of timer cycle which calls event 1 time
    delta (int): number of seconds prior to end of cycle
    delay_seconds (int): duration of cycle when event call occurs
    debug (Boolean): flag, enable verbose log output

Returns:
    TYPE: Bool, False when cycle completes

Example Use:

    thread = TimeKeeper(
        roles=['DynamoDBReadOnlyRole', 'EC2FullAccessRole'],
        event=<self.method of calling class>,
        RefreshCount=<num of cycles to call event>
    )
    thread.start()
"""

import threading
from threading import current_thread
import time
import datetime
from stsaval import logd
from stsaval.statics import __version__


logger = logd.getLogger(__version__)


# module attributes
thread_exception = {}




class TimeKeeper(threading.Thread):
    """ class def async process trigger """
    def __init__(self, roles, event, RefreshCount, debug=False):
        threading.Thread.__init__(self)
        self._halt_event = threading.Event()
        self.role_list = roles
        self.event = event
        self.count = RefreshCount
        self.event_result = {}
        self.status = False         # thread alive status
        if debug:
            self.cycle = 30                           # seconds
            delta = 5                                 # seconds
        else:
            self.cycle = 60 * 60                      # seconds (1 hr)
            delta = 30                                # seconds
        self.delay_seconds = self.cycle - delta
        try:
            # session length in seconds
            self.cycle_length = int(self.cycle * int(self.count)) - (int(self.count) * delta)
        except ValueError as e:
            logger.critical('refresh count must be an integer')
            raise e
        self.session_remaining = int(self.cycle_length)    # seconds

    def run(self):
        """
        Summary:
            non-blocking event trigger cycle

        RETURNS:
            thread status information | TYPE: dict
        """
        try:
            remaining = self.cycle_length
            executions = 1
            max_executions = self.count

            # thread status reporting and update
            self.status = self.is_alive()
            self.thread_status(
                exec=executions, max=max_executions, residual=remaining
            )

            while not self._halt_event.wait(timeout=self.delay_seconds):
                if not self._halt_event.is_set():
                    #
                    logger.info('executing event: %s' % str(self.event))
                    # call event
                    self.event_result = self.event(accounts=self.role_list)
                    remaining = remaining - self.cycle
                    executions += 1
                    # log new status
                    self.thread_status(
                        exec=executions, max=max_executions, residual=remaining
                    )
                    # halt when completed
                    if (max_executions == executions):
                        self.halt()
                else:
                    self.halt()

            return {'thread_name': str(self.name), 'STATUS': 'COMPLETE'}

        except Exception as e:
            thread_exception['thread_identifier'] = str(self.name)
            thread_exception['STATUS']= 'INCOMPLETE'
            thread_exception['Error'] = str(e)
            logger.exception('Exception: %s' % str(thread_exception))
            return thread_exception

    def halt(self):
        self._halt_event.set()
        self.status = False

    def dead(self):
        return self._halt_event.is_set()

    def thread_status(self, **kwargs):
        """ log thread and event status """
        completed = kwargs.get('exec', 'NA')
        commit = kwargs.get('max', 'NA')
        residual = kwargs.get('residual', 'NA')
        #
        logger.info('thread identifier: %s' % str(self.name))
        logger.info('thread Alive status is: %s' %  self.status)
        if 'NA' not in (completed, commit, residual):
            logger.info('completed %d out of %d total executions' %
                (kwargs['exec'], kwargs['max']))
            td = datetime.timedelta(seconds=int(kwargs['residual']))
            logger.info('remaining in cycle: %s \n ' % convert_time(td))
        return

#
# --- module functions ------------------------------------------------------###
#

def convert_to_seconds(days, hours, minutes, seconds):
    """
    Summary:
        convert time to seconds
    Args:
        time delinations in days, hours, minutes, seconds | TYPE: integer
    Returns:
        timedata in seconds | TYPE: integer
    """
    return (((days * 24) + hours) * 60 + minutes) * 60 + seconds


def convert_time(timedelta_object, return_iter=False):
    """
    Summary:
        convert timedelta objects to human readable output
    Args:
        time duration as object | TYPE: datetime.timedelta
    Returns:
        days, hours, minutes, seconds | TYPE: tuple (integers)
        or
        human readable, notated units | TYPE: string
    """
    seconds = timedelta_object.seconds
    days = seconds // (3600 * 24)
    hours = (seconds // 3600) % 24
    minutes = (seconds // 60) % 60
    seconds = seconds % 60
    if return_iter:
        return days, hours, minutes, seconds
    # string format conversions
    if days > 0:
        format_string = ('{} days, {} hours'.format(minutes, hours))
    elif hours < 1:
        format_string = ('{} min, {} sec'.format(minutes, seconds))
    else:
        format_string = ('{} hours, {} min'.format(hours, minutes))
    return format_string
