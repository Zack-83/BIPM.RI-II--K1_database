# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 08:56:11 2022

This program carries out the FAIRification of the machine-readable files of key comparison data of radionuclide metrology  

@author: romain.coulon
"""
import csv

Radionuclide = "Ce-139" # select the radionuclide


def readROR(NMI):
    with open('MNId.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            print(lines)

print(readROR("NIST"))

fileName = Radionuclide+"_database.xml"
FAIRfileName = "FAIRversions/"+Radionuclide+"_database_FAIR.xml"

file = open(fileName, 'r')
Lines = file.readlines()

FAIRfile = open(FAIRfileName, 'w')

for i, line in enumerate(Lines):

    # rewrite the 1st line
    if i == 0:
        FAIRfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        lineP = line


    # rewrite the root 
    if "<all>" in line:
        """
        FAIRfile.write("<comparison xmlns:h=\"http://www.w3.org/TR/html4/\"\n")
        FAIRfile.write("xmlns:qudt=\"http://qudt.org/2.1/schema/qudt\"\n")
        FAIRfile.write("xmlns:qudtUnit=\"http://qudt.org/schema/qudt/Unit\n")
        FAIRfile.write("  xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n")
        """
        FAIRfile.write("<Comparison>\n")
    if "</all>" in line:
        FAIRfile.write("</Comparison>")

    if "<General_information type=\"dict\">" in line:
        FAIRfile.write("\t<General_information>\n")
        FAIRfile.write("\t\t<Comparison_code>BIPM.RI(II)-K1."+Radionuclide+"</Comparison_code>\n")
        FAIRfile.write("\t\t<Pilot>\n")
        FAIRfile.write("\t\t\t<Acronym>BIPM</Acronym>\n")
        FAIRfile.write("\t\t\t<ROR_indentifier>https://ror.org/055vkyj43</ROR_indentifier>\n")
        FAIRfile.write("\t\t</Pilot>\n")
    if "</General_information>" in line:
        FAIRfile.write("\t</General_information>\n")

    if "<"+Radionuclide+" type=\"dict\">" in line:
        FAIRfile.write("\t<Comparison_data>\n")

    if "Year_of_publication" in line:
        FAIRfile.write("\t\t<Release>\n")
        line_change1 = line.replace("<Year_of_publication type=\"str\"","<Year")
        line_change2 = line_change1.replace("Year_of_publication","Year")
        FAIRfile.write(line_change2)

    if "Reference_of_the_published_comparison_report" in line:
        if "href" in line:
            i1=line.find("https")
            i2=line.find("}{")
            FAIRfile.write("\t\t\t<doi>"+line[i1:i2]+"</doi>\n")
            
    if ("</key>" in lineP and "<Data_from" in line) or ("</key>" in lineP and "<key name=\"Key comparison" in line) :
        FAIRfile.write("\t\t</Release>\n")

    if "<key name=\"Key Comparison Reference Value (KCRV)\"" in line:
        i1=line.find("\">")
        i2=line.find("</")
        line_change1=line[i1+2:i2]
        i3=line_change1.find("(")
        i4=line_change1.find(")")
        value=line_change1[:i3]
        u=line_change1[i3+1:i4]
        unit=line_change1[i4+2:]
        FAIRfile.write("\t\t\t<KCRV>\n")
        FAIRfile.write("\t\t\t\t<value>"+value+"</value>\n")
        FAIRfile.write("\t\t\t\t<unit>"+unit+"</unit>\n")
        FAIRfile.write("\t\t\t\t<standard_deviation>"+u+"</standard_deviation>\n")
        FAIRfile.write("\t\t\t</KCRV>\n")

    if "<Unit type=\"str\">" in line:
        i1=line.find(">")
        i2=line.find("</U")
        unitDoE=line[i1+1:i2]

    if "<Degrees_of_Equivalence type=\"dict\">" in line and "<Reference_of_the_linked" not in lineP2:
        FAIRfile.write("\t\t\t<Degrees_of_equivalence>\n")

    if "</Degrees_of_Equivalence>" in line:
        FAIRfile.write("\t\t\t</Degrees_of_equivalence>\n")

    if "type=\"dict\">" in lineP and "<D_i type=\"float\">" in line:
        i1=lineP.find("<")
        i2=lineP.find("type")
        Lab_acronym=lineP[i1+1:i2].replace(" ","")
        i1=line.find("\">")
        i2=line.find("</D")
        DoE=line[i1+2:i2]
        FAIRfile.write("\t\t\t\t<Degree_of_equivalence>\n")
        FAIRfile.write("\t\t\t\t\t<laboratory>\n")
        FAIRfile.write("\t\t\t\t\t\t<Acronym>"+Lab_acronym+"</Acronym>\n")
        # implement ROR
        FAIRfile.write("\t\t\t\t\t</laboratory>\n")
        FAIRfile.write("\t\t\t\t\t<value>"+DoE+"</value>\n")
        

    if "</D_i>" in lineP and "<U_i" in line:
        i1=line.find("\">")
        i2=line.find("</U_i")
        U=line[i1+2:i2]
        
        FAIRfile.write("\t\t\t\t\t<Expanded_uncertainty>"+U+"</Expanded_uncertainty>\n")
        FAIRfile.write("\t\t\t\t\t<unit>"+unitDoE+"</unit>\n")
        FAIRfile.write("\t\t\t\t</Degree_of_equivalence>\n")

    if "<Name_of_the_linked_" in line:
        i1=line.find("str\">")
        i2=line.find("</Name")
        code = line[i1+5:i2]
        i3=line.find(".RI(II)")
        rmoOrCC=line[i1+5:i3]
        FAIRfile.write("\t\t\t<Degrees_of_equivalence>\n")
        FAIRfile.write("\t\t\t\t<linked_comparison>\n")
        FAIRfile.write("\t\t\t\t\t<Comparison_code>"+code+"</Comparison_code>\n")
        if rmoOrCC == "CCRI":
            FAIRfile.write("\t\t\t\t\t<Consultative_Committee>CCRI</Consultative_Committee>\n")
        else:
            FAIRfile.write("\t\t\t\t\t<RMO>"+rmoOrCC+"</RMO>\n")

    if "<Year_of_the_link" in line:
        i1=line.find("str\">")
        i2=line.find("</Year")
        year = line[i1+5:i2]
        FAIRfile.write("\t\t\t\t\t<Year>"+year+"</Year>\n")

    if "<Reference_of_the_linked" in line:
        if "href" in line:
            i1=line.find("https")
            i2=line.find("}{")
            FAIRfile.write("\t\t\t\t\t<doi>"+line[i1:i2]+"</doi>\n")


    if "<Unit type=" in line and "<Reference_of_the_linked" in lineP:
        FAIRfile.write("\t\t\t\t</linked_comparison>\n")


    if "<Data_from" in line and "</key>" in lineP:
        FAIRfile.write("\t</Comparison_data>\n")
        FAIRfile.write("\t<Comparison_metadata>\n")
    if "</"+Radionuclide+">" in line:
        FAIRfile.write("\t</Comparison_metadata>\n")
    
    
    lineP2=lineP
    lineP=line
    




#    xmlns:bibtex "http://purl.oclc.org/NET/nknouf/ns/bibtex#"



 #   if "<key name=\"Key Comparison Reference Value (KCRV)\" type=\"str\">" in line:
 #       line_1 = "\t\t\t<QuantityKind:KCRV xmlns:QuantityKind=\"http://qudt.org/vocab/quantitykind/Activity\">\n"
 #       value = line.replace("<key name=\"Key Comparison Reference Value (KCRV)\" type=\"str\">","")
 #       for j, v in enumerate(value):
 #           if v=="(": f1=j
 #           if v==")": f2=j
 #           if v=="<": f3=j
 #       quantityValue = float(value[:f1])
 #       uncertaintyValue = int(value[f1+1:f2])
 #       unit = value[f2+2:f3]
 #       if unit == "MBq":
 #           line_2 = "\t\t\t\t<unit:MBq xmlns:unit=\"http://qudt.org/vocab/unit/MegaBQ\"> </unit:MBq xmlns:unit=\"http://qudt.org/vocab/unit/MegaBQ\">\n"
 #       else:
 #           print("unit undefined at line ", i)
 #       line_3 = "\t\t\t\t<measurmentValue type=\"float\">"+str(quantityValue)+"</YmeasurmentValue>\n"
 #       line_4 = "\t\t\t\t<stdUncertaintyUvalue type=\"float\">"+str(uncertaintyValue)+"</stdUncertaintyUvalue>\n"
 #       line_5 = "\t\t\t</QuantityKind:KCRV xmlns:QuantityKind=\"http://qudt.org/vocab/quantitykind/Activity\">\n"
 #       FAIRfile.write(line_1+line_2+line_3+line_4+line_5)
        

#    elif "<Unit type=\"str\">MBq</Unit>" in line:
#        FAIRfile.write(line.replace("<Unit type=\"str\">MBq</Unit>",   
#                                    "<unit:MBq xmlns:unit=\"http://qudt.org/vocab/unit/MegaBQ\"> </unit:MBq xmlns:unit=\"http://qudt.org/vocab/unit/MegaBQ\">"))
#    else:
#        FAIRfile.write(line)
        
    # FAIRfile.write(line)

print("END.")



# import xml.etree.ElementTree as ET


# file = "Ce-139/2022/Ce-139_database.xml"
# FAIRfile = "Ce-139/2022/Ce-139_database_FAIR.xml"


# tree = ET.parse(file)
# root = tree.getroot()

# for i in root[0]:
#     print(i.tag)
#     print(i.attrib)



# for i in root[1]:
#     print(i.tag)
#     print(i.attrib)




