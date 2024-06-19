import sys

import math
import sys
import ifcopenshell
import ifcopenshell.util
import ifcopenshell.util.element
import ifcopenshell.util.selector

import ifcopenshell.util.pset
from ifcopenshell import util

phpinput = str(sys.argv[1])


bld_elems_classes = ["IfcBeam","IfcColumn","IfcCovering","IfcCurtainWall","IfcDoor","IfcFooting","IfcMember","IfcPile","IfcPlate","IfcRailing","IfcRamp", "IfcRampFlight","IfcRoof","IfcSlab","IfcStairFlight","IfcWall","IfcWindow","IfcStair", "IfcChimney" , "IfcShadingDevice"]

ifc = ifcopenshell.open('uploads/'+str(phpinput))

#print(ifc.by_type("IfcProject")[0].UnitsInContext.Units)
bld_elems = []
present_classes = []

print(('uploads/'+str(phpinput)))