import json
from collections import OrderedDict

keep_target_indcs= [1,3,5,9,11,16,21,26,13,18,23,27,15,29,39,34,54,41,36,43,52,48,58,46,61,66,69,65,75,89,77,81,91,78,83,88,80,95,94,98]

def mod_file(sats_file = "./sats_file_test.czml"):
    fd = open(sats_file, "r")

    czml = json.load(fd,object_pairs_hook=OrderedDict)
    fd.close()

    czml_out = []

    for pkt in czml:

        if 'id' in pkt.keys():

            if ('document' in pkt['id']):
                czml_out.append(pkt)
            elif ('Satellite' in pkt['id']) and ('billboard' in pkt.keys()):
                czml_out.append(pkt)
                # name = pkt['name']
                # num = int(name.split('CubeSat')[1])

                # # if num <= 10:
                # #     pkt['availability']="2017-03-15T10:10:00Z/2017-03-16T10:00:00Z"
                # #     pkt['path']['show']['interval'] = "2017-03-15T10:10:00Z/2017-03-16T10:00:00Z"
                # # elif num <= 20:
                # #     pkt['availability']="2017-03-15T10:15:00Z/2017-03-16T10:00:00Z"
                # #     pkt['path']['show']['interval'] = "2017-03-15T10:15:00Z/2017-03-16T10:00:00Z"
                # # else:
                # #     pkt['availability']="2017-03-15T10:20:00Z/2017-03-16T10:00:00Z"
                # #     pkt['path']['show']['interval'] = "2017-03-15T10:20:00Z/2017-03-16T10:00:00Z"

                # # if num>1:
                # pkt['path']['show']['boolean']=True
                # pkt['path']['leadTime']=43200
                # pkt['path']['trailTime']=43200

                # if num==1:
                #     pkt['path']['material']['solidColor']['color']['rgba']=[255,0,0,255]
                # elif num==2:
                #     pkt['path']['material']['solidColor']['color']['rgba']=[0,255,0,255]
                # elif num==3:
                #     pkt['path']['material']['solidColor']['color']['rgba']=[16,200,175,255]
                # elif num==4:
                #     pkt['path']['material']['solidColor']['color']['rgba']=[189,111,122,255]
                # elif num==5:
                #     pkt['path']['material']['solidColor']['color']['rgba']=[32,150,89,255]
                # elif num==6:
                #     pkt['path']['material']['solidColor']['color']['rgba']=[230,230,118,255]
                # elif num==7:
                #     pkt['path']['material']['solidColor']['color']['rgba']=[240,89,5,255]
                # elif num==8:
                #     pkt['path']['material']['solidColor']['color']['rgba']=[150,130,110,255]
                # elif num==9:
                #     pkt['path']['material']['solidColor']['color']['rgba']=[69,96,69,255]
                # elif num==10:
                #     pkt['path']['material']['solidColor']['color']['rgba']=[0,100,200,255]
                # elif num>10:
                #     pkt['path']['show']['boolean']=False

            elif ('Facility/' in pkt['id']) and ('billboard' in pkt.keys()):
                pkt['label']['show']=False
                pkt['billboard']['show']=  True

                czml_out.append(pkt)

            elif ('Target/' in pkt['id']):
                target_indx = int(pkt['id'].split('/')[1])

                # pkt['label']['show']=False
                # pkt['billboard']['show']=  True

                if target_indx in keep_target_indcs:
                    czml_out.append(pkt)
            else:
                czml_out.append(pkt)


    fd = open(sats_file, "w")
    json.dump(czml_out,fd,indent=4)


if __name__ == '__main__':
    mod_file(sats_file = "./sats_file.czml")
