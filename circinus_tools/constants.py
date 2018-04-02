from datetime import datetime, timedelta

UNASSIGNED = -999
# below is the datetime corresponding to UNASSIGNED (-999)
UNASSIGNED_DT = datetime.strptime('1856-02-22 00:00:00','%Y-%m-%d %H:%M:%S')

# For use as an effective infinity datetime value
UNASSIGNED_DT_INF = datetime.strptime('2100-01-01 00:00:00','%Y-%m-%d %H:%M:%S')
UNASSIGNED_DT_NEG_INF = datetime.strptime('1900-01-01 00:00:00','%Y-%m-%d %H:%M:%S')

## date formats
MODIFIED_JULIAN_DATE = 0

# todo: move the below stuff elsewhere

obs_routing_preference_Mb=1000  # prefer downlinking up to this much data from a single obs before moving on to the next one

dv_lowest_total_consider_Mb = 100 # If total data volume for a lnk goes below this, don't consider it schedulable
dv_epsilon_Mb = 1 # Aproximately zero. If this is the remaining data volume, consider it zero

min_dlnk_length = timedelta(minutes=2)     # min allowed allowed dlnk duration. Throws some fudge in for setup
exclusive_dlnk_time = timedelta(minutes=5)  # max time that a sat has exclusive control over a dlnk before another sat can steal the gs. Helps with giving everyone a chance to dlnk.
dlnk_usurpable_fraction = 0.8  # if data volume for sat 2 with gs 1 is greater than this fraction of sat 1 with gs 1, then can steal

# TODO: incorporate this back in
min_interdlnk_time = timedelta(minutes=0)  # min time allowed between downlinks for the same sat. Throws some fudge in for setup, slewing between GS


# note: we're assuming here that the satellite slews in between crosslinks
# and downlinks. For crosslinks of opposite directions, it would need to
# slew 180 degrees. For a downlink from a crosslink, 90 degrees.
# (this is, of course, because we're assuming optical crosslinks)
# To simply the code, just assume that all inter-xlnk times must need a
# transition time, even if they're actually xlnks with the same satellite.
# A low laser P_tx, it doesn't matter that much because we're swimming in
# crosslink time anyway.
min_xlnk_dlnk_transition_time_sec = 3*60
min_xlnk_xlnk_transition_time_sec = 6*60
min_xlnk_dlnk_transition_time_td = timedelta(seconds=min_xlnk_dlnk_transition_time_sec)
min_xlnk_xlnk_transition_time_td = timedelta(seconds=min_xlnk_xlnk_transition_time_sec)
# min_dlnk_xlnk_transition_time_sec = 3*60

include_commlink_transitions = True  # check if the crosslink we're trying to schedule is sufficiently far away from other links to allow for attitude slewing between
include_dlnk_transition_checking= False  # todo: note this is not implemented for now because we've already scheduled the dlnks, and it would just add pointless computations to run for now