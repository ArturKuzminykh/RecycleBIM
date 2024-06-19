import math
import sys
import ifcopenshell
import ifcopenshell.util
import ifcopenshell.util.element
import ifcopenshell.util.selector
import json
import ifcopenshell.util.pset
from ifcopenshell import util

phpinput = str(sys.argv[1])


bld_elems_classes = ["IfcBeam","IfcColumn","IfcCovering","IfcCurtainWall","IfcDoor","IfcFooting","IfcMember","IfcPile","IfcPlate","IfcRailing","IfcRamp", "IfcRampFlight","IfcRoof","IfcSlab","IfcStairFlight","IfcWall","IfcWindow","IfcStair", "IfcChimney" , "IfcShadingDevice"]

ifc = ifcopenshell.open('uploads/'+str(phpinput))
#ifc = ifcopenshell.open('D:/OneDrive/03_Study/BIMA+Dissertation/05_CaseStudy/02_IFC/v03_IFC4_SampleModel/AK_TestProject_sample.ifc')


#print(ifc.by_type("IfcProject")[0].UnitsInContext.Units)
bld_elems = []
present_classes = []
elems_wo_pset = []
present_elems_ids = []


for i in range(len(bld_elems_classes)):  #filtering present classes and populating list of present classes
    cl_elems = ifc.by_type(bld_elems_classes[i])

    if len(cl_elems) != 0:
        present_classes.append(bld_elems_classes[i])
        bld_elems.append(cl_elems)
        #(bld_elems_classes[i], len(cl_elems))


# Retrieving GUIDs of elements that can be reused

for i in range(len(bld_elems)):
    have_pset = 0
    donthave_pset = 0
    num_of_elem_with_parents = 0
    parent_donthave_pset = 0
    parent_have_pset = 0
    parent_elements = []
    
    for elem in bld_elems[i]:
        pset_recycle = ifcopenshell.util.element.get_psets(elem).get("RecycleBIM")
        present_elems_ids.append(elem.GlobalId)
        if pset_recycle == None or pset_recycle == 0:
            donthave_pset += 1

            if len(elem.Decomposes) != 0:
                pel = elem.Decomposes[0].RelatingObject
                pel_prop = ifcopenshell.util.element.get_psets(pel).get("RecycleBIM")
                if  pel_prop== None or pel_prop == 0:
                    elems_wo_pset.append(elem.GlobalId)
        else:
            have_pset += 1
        ratio = math.ceil(have_pset*100/(have_pset+donthave_pset))


#print([item for item in present_elems_ids if item not in elems_wo_pset])

#print (json.dumps([["sgsg",4,'sgsg'],elems_wo_pset]))

print (json.dumps([elems_wo_pset,[item for item in present_elems_ids if item not in elems_wo_pset]]))


