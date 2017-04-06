import json
from collections import OrderedDict

def strip_file(strip_file = "./sats_file.czml"):
    fd = open(strip_file, "r")

    czml = json.load(fd,object_pairs_hook=OrderedDict)
    czml_stripped = []

    for pkt in czml:

        if 'id' in pkt.keys():

            if ('document' in pkt['id']) or ('Target/' in pkt['id']) or ('Rectangle/' in pkt['id']):
                pass
            elif ('Satellite' in pkt['id']) and ('billboard' in pkt.keys()):
                pass
            elif ('Facility/' in pkt['id']) and ('billboard' in pkt.keys()):
                pass
            else:
                continue

            czml_stripped.append(pkt)


    fd.close()
    # fd2 = open("/Users/ktikennedy/Dropbox (MIT)/Cesium/Cesium-1.27/Apps/AutomatedConstViz/movie_rev3/app_data_files/autoconst_sats2.czml", "w")

    fd = open(strip_file, "w")
    json.dump(czml_stripped,fd,indent=4)


if __name__ == '__main__':
    strip_file()
