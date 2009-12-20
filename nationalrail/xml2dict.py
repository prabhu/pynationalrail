#!/usr/bin/env python
# Thunder Chen<nkchenz@gmail.com> 2007.9.1
# 
#

import xml.etree.ElementTree as ET
from object_dict import object_dict 

def __parse_node(node):
    tmp = object_dict()
    # save attrs and text, hope there will not be a child with same name
    if node.text:
        # Uncomment the below line to get value attribute for each tag
        #tmp['value'] = node.text
        tmp = node.text
    for (k,v) in node.attrib.items():
        tmp[k] = v

    for ch in node.getchildren():
        cht = ch.tag
        chp = __parse_node(ch)

        if cht not in tmp: # the first time, so store it in dict
            tmp[cht] = chp
            continue

        old = tmp[cht]
        if not isinstance(old, list):
            tmp.pop(cht)   
            tmp[cht] = [old] # multi times, so change old dict to a list       
        tmp[cht].append(chp) # add the new one      

    return  tmp

def parse(file):
    """parse a xml file to a dict"""
    f = open(file, 'r')
    t = ET.parse(f).getroot()
    return object_dict({t.tag: __parse_node(t)})

def fromstring(s):
    """parse a string"""
    t = ET.fromstring(s)
    return object_dict({t.tag: __parse_node(t)})
