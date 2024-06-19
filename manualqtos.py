
import sys
import ifcopenshell
import ifcopenshell.util
import ifcopenshell.util.element
import ifcopenshell.util.selector
import ifcopenshell.geom
import json

import ifcopenshell.util.pset


phpinput = str(sys.argv[1])



bld_elems_classes = ["IfcBeam","IfcColumn","IfcCovering","IfcCurtainWall","IfcDoor","IfcFooting","IfcMember","IfcPile","IfcPlate","IfcRailing","IfcRamp", "IfcRampFlight","IfcRoof","IfcSlab","IfcStairFlight","IfcWall","IfcWindow","IfcStair", "IfcChimney" , "IfcShadingDevice"]

ifc = ifcopenshell.open('uploads/'+str(phpinput))

bld_elems = []
present_classes = []
present_elems_ids = []
lst_text =[]
for i in range(len(bld_elems_classes)):  #filtering present classes and populating list of present classes
    cl_elems = ifc.by_type(bld_elems_classes[i])

    if len(cl_elems) != 0:
        present_classes.append(bld_elems_classes[i])
        bld_elems.append(cl_elems)
        #(bld_elems_classes[i], len(cl_elems))

manqto_elems = []
for i in range(len(bld_elems)):
    lst_text_cl =[]
    for elem in bld_elems[i]:
        present_elems_ids.append(elem.GlobalId)
        pset_recycle = ifcopenshell.util.element.get_psets(elem).get("RecycleBIM")
        if pset_recycle != None:

            pr_qto = pset_recycle.get("AK_ItemQuantityManual")
            pr_qto_du = pset_recycle.get("AK_DeclaredUnit")
            if pr_qto != None:
                lst_text_cl.append(str(present_classes[i]) + ". GUID: " + str(elem.GlobalId) + ". The quantity will be taken according to the manually identified numeric value: " + str(pr_qto)+ str(pr_qto_du))
                manqto_elems.append(elem.GlobalId)
            
                
    if len(lst_text_cl) != 0:
        lst_text.append(lst_text_cl)

print(json.dumps([manqto_elems, [item for item in present_elems_ids if item not in manqto_elems],lst_text]))