from datetime import timedelta

from circinus_tools  import  constants as const

class ActivityWindow(object):
    """ specifies an activity that occurs from a start to an end time
    
    note that the hash function for this class uses the window_ID attribute. This should be globally unique across all  activity window instances and subclass instances created in the simulation
    """

    def __init__(self, start, end, window_ID):
        '''
        Creates an activity window

        :param datetime start: start time of the window
        :param datetime end: end time of the window
        :param int window_ID:  unique window ID used for hashing and comparing windows
        '''

        self.start = start
        self.end = end
        self.window_ID = window_ID
        self.data_vol = const.UNASSIGNED
        self.scheduled_data_vol = const.UNASSIGNED
        self.remaining_data_vol = const.UNASSIGNED

        self._center_cache = None
        self._ave_data_rate_cache = None

        #  keeps track of if the start and end times of this window have been updated, for use as a safeguard
        self.timing_updated = False

    def __hash__(self):
        return self.window_ID

    def __eq__(self, other):
        return self.window_ID ==  other.window_ID

    @property
    def center(self):
        #  adding this try except to deal with already pickled activity Windows
        # TODO: remove this error checking later once all code solidified?
        try:
            if not self._center_cache:
                self._center_cache = self.calc_center()
            return self._center_cache
        except AttributeError:
            self._center_cache = self.calc_center()
            return self._center_cache

    @property
    def ave_data_rate(self):
        #  adding this try except to deal with already pickled activity Windows
        # TODO: remove this error checking later once all code solidified?
        try:
            if not self._ave_data_rate_cache:
                if self.timing_updated: raise RuntimeWarning('Trying to calculate average data rate after window timing has been updated')
                self._ave_data_rate_cache =  self.data_vol / ( self.end - self.start).total_seconds ()
            return self._ave_data_rate_cache
        except AttributeError:
            if self.timing_updated: raise RuntimeWarning('Trying to calculate average data rate after window timing has been updated')
            self._ave_data_rate_cache = self.data_vol / ( self.end - self.start).total_seconds ()
            return self._ave_data_rate_cache

    def calc_center ( self):
        return self.start + ( self.end -  self.start)/2

    def update_duration_from_scheduled_dv( self,min_duration_s=10):
        """ update duration based on schedule data volume
        
        updates the schedule duration for the window based upon the assumption that the data volume scheduled for the window is able to be transferred at an average data rate. Updated window times are based off of the center time of the window.
        """
        old_duration = self.end - self.start

        if old_duration.total_seconds() < min_duration_s:
            raise RuntimeWarning('Original duration (%f) is less than minimum allowed duration (%f) for %s'%(old_duration.total_seconds(),min_duration_s,self))

        # note that accessing ave_data_rate below either uses the cached the original ave data rate, or caches it now
        scheduled_time_s = self.scheduled_data_vol/self.ave_data_rate
        scheduled_time_s = max(scheduled_time_s,min_duration_s)

        self.start = self.center - timedelta ( seconds = scheduled_time_s/2)
        self.end = self.center + timedelta ( seconds = scheduled_time_s/2)
        #  probably good to clear the cache here for consistency after a timing update, though not strictly necessary with the way the code is implemented right now (center time stays the same)
        self._center_cache = None

        # mark that timing has been updated
        self.timing_updated = True


    def print_self(self):
        print('ActivityWindow')
        print('start: ' + str(self.start))
        print('end: ' + str(self.end))
        print('......')

    def combine_with_window(self,other_act):
        '''
        Note: deprecated

        Combine this window with another one. The combined window object is stored in self. Overlap existence is assumed -compareWindows should be called first to see if there's overlap or not

        :param other_act: other window to combine into self
        :return: nothing (self stores combined window)
        '''

        if self.start < other_act.start:
            if self.end < other_act.end:
                self.end = other_act.end
            else:
                print('ActivityWindow.py: warning, combining non-overlapping windows')

        if self.start > other_act.start:
            self.start = other_act.start

            if self.start > other_act.end:
                print('ActivityWindow.py: warning, combining non-overlapping windows')

