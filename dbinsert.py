import  MySQLdb
import sys
import ifcopenshell
import ifcopenshell.util
import ifcopenshell.util.element
import ifcopenshell.util.selector
import ifcopenshell.util.pset

from telegram import send_msg

ref_num = str(sys.argv[1])
type_bld = str(sys.argv[2])
year = str(sys.argv[3])
docs = str(sys.argv[4])
demol_date = str(sys.argv[5])
user = str(sys.argv[6])
phpinput = str(sys.argv[7])

ifc = ifcopenshell.open('uploads/'+str(phpinput))


site = ifc.by_type("IfcSite")
lat = site[0].RefLatitude
long = site[0].RefLongitude

def degr_to_dec(position):
    value = [i for i in position ]
    if value[3] < 0:
        value[3] = int(str(value[3])[:4])/1000
    else:
        value[3] = int(str(value[3])[:3])/1000
    value[1] = value[1]/60
    value[2] = (value[2]+value[3])/3600
    value = value[:-1]
    return(sum(value))

if lat != None and long != None:
    latitude = str(degr_to_dec(lat))
    longitude = str(degr_to_dec(long))
else:
    latitude = "0"
    longitude = "0"


#print(latitude,longitude)
db = MySQLdb.connect('localhost','root','','phpproject01')
insertrec = db.cursor()
sqlquery = 'insert into projects(usersName,modelReferenceNumber, typeOfBuilding, yearOfConstruction, availableDocumentation, demolitionStartDate, locationLatitude, locationLongitude) values ("'+user+'","'+ref_num+'", "'+type_bld+'","'+year+'","'+docs+'","'+demol_date+'","'+latitude+'","'+longitude+'") '
insertrec.execute(sqlquery)
db.commit()
db.close()




#text = "New project:\n" + 'https://maps.google.com/maps?q=' + latitude + ',' + longitude + '&hl=es;z=14&amp'
text = 'New project:\nhttps://maps.google.com/maps?q={},{}&hl=es;z=14&amp'.format(latitude, longitude)
send_msg(text)







