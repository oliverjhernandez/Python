#!/usr/local/bin/python2

import os
import re
import jinja2

def get_template():
  THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def print_final():
  templateLoader = jinja2.FileSystemLoader( searchpath="." )
  templateEnv = jinja2.Environment( loader=templateLoader )
  
  TEMPLATE_FILE = "export.json"
  template = templateEnv.get_template( TEMPLATE_FILE )
  
  COUNTRIES = ["Bahamas","Trinidad","Panama","Jamaica","BVI","ST.Kitts","Cayman","Curacao","TCI","Barbados","St.Lucia","Jamaica-Carlton","Jamaica-MoBay","Anguilla"]
  COUNTRY_CODE = ["bs","tt","pa","jm","vg","kn","ky","an","tci","bb","slu","jm-cl","jm-mb","ai"]
  
  for i in range(len(COUNTRIES)):
    output = open("export_" + COUNTRY_CODE[i] + ".json", "w")
    templateVars = { "country" : COUNTRIES[i],
                     "country_code" : COUNTRY_CODE[i] }
    final = template.render( templateVars )
    output.write(final)
    output.close()


if __name__ == '__main__':
  print_final()


