import json
from collections import OrderedDict
import datetime
import sys

def update_epochs(sats_file = ".../sats_file.czml",start_epoch = datetime.datetime(2017, 3, 15, 10, 0, 0),end_epoch = datetime.datetime(2017, 3, 16, 10, 0, 0)):
    fd = open(sats_file, "r")

    czml = json.load(fd,object_pairs_hook=OrderedDict)

    full_interval = start_epoch.strftime('%Y-%m-%dT%H:%M:%SZ')+'/'+end_epoch.strftime('%Y-%m-%dT%H:%M:%SZ')

    for pkt in czml:

        if 'id' in pkt.keys():

            if ('document' in pkt['id']):
                pkt['clock']['interval'] = full_interval
                pkt['clock']['currentTime'] = start_epoch.strftime('%Y-%m-%dT%H:%M:%SZ')

            elif ('Facility/' in pkt['id']) and ('billboard' in pkt.keys()):
                pkt['availability'] = full_interval

            elif ('Target/' in pkt['id']) and ('billboard' in pkt.keys()):
                pkt['availability'] = full_interval

            elif ('Satellite' in pkt['id']) and ('billboard' in pkt.keys()):
                pkt['availability'] = full_interval
                pkt['position']['epoch'] = start_epoch.strftime('%Y-%m-%dT%H:%M:%SZ')

                if len(pkt['path']['show']) == 1:
                    pkt['path']['show']= {'interval':full_interval,'boolean':True}

    fd.close()

    fd = open(sats_file, "w")
    json.dump(czml,fd,indent=4)
    fd.close()


if __name__ == '__main__':

    if len(sys.argv) != 4:
        # print len(sys.argv)
        print "Usage: CZMLEpochUpdater.py <path to file> <start epoch string> <end epoch string>"
        print str(len(sys.argv)) + ' args given: '+str(sys.argv)

        sys.exit(-1)

    sats_file,start_epoch_str,end_epoch_str = sys.argv[1:4]
    start_epoch = datetime.datetime.strptime(start_epoch_str,'%d %b %Y %H:%M:%S.%f')
    end_epoch = datetime.datetime.strptime(end_epoch_str,'%d %b %Y %H:%M:%S.%f')
    update_epochs(sats_file,start_epoch,end_epoch)