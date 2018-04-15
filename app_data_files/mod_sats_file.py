import json
from collections import OrderedDict

def mod_file(sats_file = "./sats_file_test.czml"):
    fd = open(sats_file, "r")

    czml = json.load(fd,object_pairs_hook=OrderedDict)
    fd.close()

    for pkt in czml:

        if 'id' in pkt.keys():

            if ('document' in pkt['id']):
                pass
            elif ('Satellite' in pkt['id']) and ('billboard' in pkt.keys()):
                pass
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
            elif ('Target/' in pkt['id']):
                pkt['label']['show']=False
                pkt['billboard']['show']=  True
            else:
                continue


    fd = open(sats_file, "w")
    json.dump(czml,fd,indent=4)


if __name__ == '__main__':
    mod_file(sats_file = "./sats_file.czml")
