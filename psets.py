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

# find if there are parent elements that hold properties

        if len(elem.Decomposes) != 0:
            parent_element = elem.Decomposes[0].RelatingObject
            num_of_elem_with_parents += 1
            if parent_element not in parent_elements:
                parent_elements.append(parent_element)
                parent_pset_recycle = ifcopenshell.util.element.get_psets(parent_element).get("RecycleBIM")
                if parent_pset_recycle == None or parent_pset_recycle == 0:
                    parent_donthave_pset += 1
                else:
                    parent_have_pset += 1
    #print(parent_have_pset,parent_donthave_pset)
    #print(len(parent_elements))
    print(present_classes[i], "-", len(bld_elems[i]),"element(s). Circularity properties are filled:",ratio, "%")
    if len(parent_elements) != 0:
        ratio_parents = math.ceil(100*parent_have_pset/(parent_have_pset+parent_donthave_pset))
        print( "NOTE: For the class",present_classes[i], num_of_elem_with_parents,"elements (",math.ceil(100*num_of_elem_with_parents/len(bld_elems[i])),"%) have parent elements,", ratio_parents,"% of them have Circularity properties")
    print()

print (json.dumps([elems_wo_pset,[item for item in present_elems_ids if item not in elems_wo_pset]]))






