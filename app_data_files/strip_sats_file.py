import json

fd = open("./sats_file.czml", "r")

czml = json.load(fd)
czml_stripped = []

for pkt in czml:

    if 'id' in pkt.keys():

        if ('document' in pkt['id']) or ('Facility/' in pkt['id']) or ('Target/' in pkt['id']) or ('Rectangle/' in pkt['id']):
            pass
        elif ('Satellite' in pkt['id']) and ('billboard' in pkt.keys()):
            pass
        else:
            continue

        czml_stripped.append(pkt)


fd.close()
# fd2 = open("/Users/ktikennedy/Dropbox (MIT)/Cesium/Cesium-1.27/Apps/AutomatedConstViz/movie_rev3/app_data_files/autoconst_sats2.czml", "w")

fd = open("./sats_file.czml", "w")
json.dump(czml_stripped,fd,indent=4)