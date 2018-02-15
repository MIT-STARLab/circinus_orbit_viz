##############################
# Values for window comparisons

# The more negative a value below is, the more it suggests window1 should be put in front of window2.

# If absolute value is 20 or greater, then we should keep 2 windows. If abs is less than 20 (a total overlap), that suggests maybe it would be better to split the larger window in 2 pieces. If value is 0, then it's only one window should be chosen because the activities are totally in conflict

WIND1_TOTS_BEFORE = -60                 # end of wind 1 is less than start of wind 2. Easy.
WIND1_END_TOUCH_BEG_WIND2 = -50         # end of wind 1 is equal to start of wind 2.
WIND1_END_OVLP_WIND2 = -40              # start of wind 1 before start of wind 2. End of wind 1 before end of end of wind 2.
WIND1_END_OVLP_WIND2_EQ = -30           # start of wind 1 before start of wind 2. Ends equal

WIND1_TOT_OVLP_WIND2_MORE_BEFORE = -11  # wind 2 completely covered by wind 1, endtimes not equal. More of wind 1 hanging out before wind 2 starts
WIND1_TOT_OVLP_WIND2_EQ = -10           # wind 2 completely covered by wind 1, endtimes not equal. Equal amounts of wind 1 hanging on either side
WIND1_TOT_OVLP_WIND2_MORE_AFTER = -9    # wind 2 completely covered by wind 1, endtimes not equal. More of wind 1 hanging out after wind 2 ends

WIND2_BEG_OVLP_WIND1 = -0.5             # start is equal, wind 1 smaller than wind2
TOTS_EQ = 0                             # exactly equal end times
WIND1_BEG_OVLP_WIND2 = 0.5              # start is equal, wind 2 smaller than wind1

WIND2_TOT_OVLP_WIND1_MORE_BEFORE = 9
WIND2_TOT_OVLP_WIND1_EQ  = 10           # window 2 is bigger than window 1, and the distance from start of window 2 to start wind 1 is same as end of wind 1 to end of wind 2
WIND2_TOT_OVLP_WIND1_MORE_AFTER  = 11

WIND2_END_OVLP_WIND1_EQ = 30
WIND2_END_OVLP_WIND1 = 40
WIND2_END_TOUCH_BEG_WIND1 = 50
WIND1_TOTS_AFTER = 60

UNASSIGNED = -999
####################


class ActivityWindow(object):
    def __init__(self, start, end):
        '''
        Creates an activity window

        :param datetime start: start time of the window
        :param datetime end: end time of the window
        '''

        self.start = start
        self.end = end

        # create a timedelta object from by subtracting two datetimes
        self.duration = end - start

    def printSelf(self):
        print('ActivityWindow')
        print('start: ' + str(self.start))
        print('end: ' + str(self.end))
        print('duration: ' + str(self.duration))
        print('......')

    def refreshDuration(self):
        self.duration = self.end - self.start

    def compareWithWindow(self, wind2):
        '''
        A seemingly very complicated function that in reality just returns an integer that describes the degree of overlap in two time windows.

        :param wind2: other window to compare timing with. wind2 start time should come AFTER self's start time.
        :return: a number that specifies the degree of overlap between the windows
        '''

        comparison = UNASSIGNED

        if self.start < wind2.start:
            if self.end < wind2.start:
                comparison = WIND1_TOTS_BEFORE

            elif self.end == wind2.start:
                comparison = WIND1_END_TOUCH_BEG_WIND2

            elif self.end > wind2.start:

                if self.end < wind2.end:
                    comparison = WIND1_END_OVLP_WIND2

                elif self.end == wind2.end:
                    comparison = WIND1_END_OVLP_WIND2_EQ

                elif self.end > wind2.end:
                    before_delta_t = wind2.start - self.start
                    after_delta_t = self.end - wind2.end

                    if before_delta_t > after_delta_t:
                        comparison = WIND1_TOT_OVLP_WIND2_MORE_BEFORE
                    elif before_delta_t == after_delta_t:
                        comparison = WIND1_TOT_OVLP_WIND2_EQ
                    else:  # before_delta_t < after_delta_t
                        comparison = WIND1_TOT_OVLP_WIND2_MORE_AFTER
                else:
                    print('should not be reachable 1')
                    hi = 1 / 0
            else:
                print('should not be reachable 2')
                hi = 1 / 0

        elif self.start == wind2.start:
            if self.end < wind2.end:
                comparison = WIND2_BEG_OVLP_WIND1

            if self.end == wind2.end:
                comparison = TOTS_EQ

            if self.end > wind2.end:
                comparison = WIND1_BEG_OVLP_WIND2

        elif self.start > wind2.start:
            if self.start == wind2.end:
                comparison = WIND2_END_TOUCH_BEG_WIND1

            elif self.start > wind2.end:
                comparison = WIND1_TOTS_AFTER

            elif self.start < wind2.end:

                if self.end < wind2.end:
                    before_delta_t = self.start - wind2.start
                    after_delta_t = wind2.end - self.end

                    if before_delta_t > after_delta_t:
                        comparison = WIND2_TOT_OVLP_WIND1_MORE_BEFORE
                    elif before_delta_t == after_delta_t:
                        comparison = WIND2_TOT_OVLP_WIND1_EQ
                    else:  # before_delta_t < after_delta_t
                        comparison = WIND2_TOT_OVLP_WIND1_MORE_AFTER

                elif self.end == wind2.end:
                    comparison = WIND2_END_OVLP_WIND1_EQ

                elif self.end > wind2.end:
                    comparison = WIND2_END_OVLP_WIND1

                else:
                    print('should not be reachable 3')
                    hi = 1 / 0

            else:
                print('should not be reachable 4')
                hi = 1 / 0
        else:
            print('should not be reachable 5')
            hi = 1 / 0

        return comparison

    def combineWithWindow(self,other_act):
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

        self.duration = self.end - self.start