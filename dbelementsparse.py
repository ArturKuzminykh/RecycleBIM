import  MySQLdb
import sys
import ifcopenshell
import ifcopenshell.util
import ifcopenshell.util.element
import ifcopenshell.util.selector
import ifcopenshell.util.pset


model = str(sys.argv[1])
model_reference = model[:-4]
ifc = ifcopenshell.open('uploads/'+str(model))



bld_elems_classes = ["IfcBeam", "IfcColumn", "IfcCovering", "IfcCurtainWall", "IfcDoor", "IfcFooting", "IfcMember", "IfcPile", "IfcPlate", "IfcRailing", "IfcRamp", "IfcRampFlight", "IfcRoof", "IfcSlab", "IfcStairFlight", "IfcWall", "IfcWindow", "IfcStair", "IfcChimney", "IfcShadingDevice"]

bld_elems = []
present_classes = []

for i in range(len(bld_elems_classes)):  # filtering present classes and populating list of present classes
    cl_elems = ifc.by_type(bld_elems_classes[i])

    if len(cl_elems) != 0:
        present_classes.append(bld_elems_classes[i])
        bld_elems.append(cl_elems)

qto_pset_name = []

def get_p_fromPset(pset, pname):
    p = pset.get(pname)
    if p!= None:
        return str(p)
    else:
        return " test "

for i in range(len(present_classes)):
    short_name = "Qto_" + present_classes[i][3:] + "BaseQuantities"
    qto_pset_name.append(short_name)

db = MySQLdb.connect('localhost', 'root', '', 'phpproject01')
insertrec = db.cursor()
counter_tot = 0
counter_passed = 0

for i in range(len(bld_elems)):
    for elem in bld_elems[i]:
        pset_recycle = ifcopenshell.util.element.get_psets(elem).get("RecycleBIM")
        if pset_recycle != None:
            counter_tot += 1

            pset_recycle = ifcopenshell.util.element.get_psets(elem).get("RecycleBIM")

            objectClass = present_classes[i]
            typeName = elem.ObjectType
            declaredUnit = get_p_fromPset(pset_recycle, "AK_DeclaredUnit")
            declaredQuantityPerUnit = get_p_fromPset(pset_recycle, "AK_DeclaredQuantityPerUnit")
            materialCompounPerDeclareUnit = get_p_fromPset(pset_recycle, "AK_MaterialCompoundPerDeclaredUnit")
            materialQuantityPerDeclaredUnit = get_p_fromPset(pset_recycle, "AK_MaterialQuantityPerDeclaredUnit")
            canBeRecycled = get_p_fromPset(pset_recycle, "AK_ItemCanBeRecycled")
            if canBeRecycled == "True":
                canBeRecycled = "1"

            canBeReused = get_p_fromPset(pset_recycle, "AK_ItemCanBeReused")
            if canBeReused == "True":
                canBeReused = "1"

            hasPotentialDanger = get_p_fromPset(pset_recycle, "AK_ItemHasPotentialDanger")
            if hasPotentialDanger == "True":
                hasPotentialDanger = "1"

            requiresIndoorStorage = get_p_fromPset(pset_recycle, "AK_RequiresIndoorStorage")
            if requiresIndoorStorage == "True":
                requiresIndoorStorage = "1"

            typeOfJoints = get_p_fromPset(pset_recycle, "AK_TypeOfJoints")
            pset_bqto = ifcopenshell.util.element.get_psets(elem).get(qto_pset_name[i])

            if pset_recycle.get("AK_ItemQuantityManual") != None and pset_recycle.get("AK_ItemQuantityManual") != 0:
                quantity = pset_recycle.get("AK_ItemQuantityManual")
            else:
                if pset_bqto != None:
                    if declaredUnit == "m":
                        if pset_bqto.get("Length") != None:
                            quantity = pset_bqto.get("Length") / 1000
                        else:
                            quantity = 0
                    elif declaredUnit == "m2":
                        if pset_bqto.get("NetSideArea") != None:
                            quantity = pset_bqto.get("NetSideArea")
                        elif pset_bqto.get("NetArea") != None:
                            quantity = pset_bqto.get("NetArea")
                        elif pset_bqto.get("Area") != None:
                            quantity = pset_bqto.get("Area")
                        else:
                            quantity = 0
                    elif declaredUnit == "m3":
                        if pset_bqto.get("NetVolume") != None:
                            quantity = pset_bqto.get("NetVolume")
                        elif pset_bqto.get("Volume") != None:
                            quantity = pset_bqto.get("Volume")
                        else:
                            quantity = 0
                    elif declaredUnit == "pcs":
                        quantity = 1
                else:
                    quantity = 0

            referenceInModel = elem.GlobalId
            documentation_image = pset_recycle.get("Image")
            if documentation_image != None:
                documentation_image = documentation_image[14:]
            else:
                documentation_image = "No image"

            if quantity != 0 and declaredQuantityPerUnit != None and materialQuantityPerDeclaredUnit != None:
                tot_qt = [str("{:.2f}".format(float(i)*quantity/float(declaredQuantityPerUnit))) for i in materialQuantityPerDeclaredUnit.split(',')]
                tot_qt_str = ",".join(tot_qt)
                
                quantity = str(quantity)


                sqlquery = 'insert into projectbuildingobjects(objectClass,typeName, declaredUnit,declaredQuantityPerUnit,materialCompounPerDeclareUnit,materialQuantityPerDeclaredUnit,canBeRecycled,canBeReused,hasPotentialDanger,requiresIndoorStorage, typeOfJoints, quantity, referenceInModel,documentation, totalQuantityOfMaterials, modelReference) values ("' + objectClass + '","' + typeName + '","' + declaredUnit + '","' + declaredQuantityPerUnit + '","' + materialCompounPerDeclareUnit + '","' + materialQuantityPerDeclaredUnit + '","' + canBeRecycled + '","' + canBeReused + '","' + hasPotentialDanger + '","' + requiresIndoorStorage + '","' + typeOfJoints + '","' + quantity + '","' + referenceInModel + '","' + documentation_image + '","' + tot_qt_str + '","' + model_reference + '") '
                insertrec.execute(sqlquery)

                counter_passed += 1
passed = str(counter_passed*100/counter_tot)[:4]
print("Elements that satisfy the quantity requirements: " + passed +" %")
db.commit()
db.close()