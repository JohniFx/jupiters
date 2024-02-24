import xml.etree.cElementTree as ET
from datetime import datetime
import polars as pl
import pandas as pd
import numpy as np
import okos_solar_production as osp

params= dict(
    pods= 50000,
    days = 1)

obis = '1.29.99.128'
# dates = pl.datetime_range(datetime(2023,10,1, 0,15), datetime(2023,10,31, 0,15), interval="1D", eager=True)
dates = pd.date_range(datetime(2024,1,1,0,15), periods=params['days'], freq = 'D')

om_piac=[{"eloszto": 110, "pod_szam":110000, "batch_size":10000, "indent":False},
         {"eloszto": 120, "pod_szam":120000, "batch_size":10000, "indent":False},
         {"eloszto": 130, "pod_szam":130000, "batch_size":10000, "indent":True},
         {"eloszto": 210, "pod_szam":200000, "batch_size":10000, "indent":True},
         {"eloszto": 220, "pod_szam":100000, "batch_size":10000, "indent":True},
         {"eloszto": 310, "pod_szam":35000,  "batch_size":10000, "indent":True}]

def create_pods(elo, count):
    pods = []
    for i in range(0,count):
        pod = f'HU000{elo}-A00-v-TESTPOD-{i:06}'
        pods.append(pod)
    return pods

def generate1():
    root = ET.Element("EDW_XML")
    # header
    header = ET.SubElement(root, "HEADER")
    ET.SubElement(header, "VERSION").text = "1.0"
    ET.SubElement(header, "GENERATOR").text = "xml_by_jano"
    ET.SubElement(header, "GENERATED-DATETIME").text = datetime.now().isoformat()
    # ET.indent(header)
    header.tail='\n'
    # data
    for e in elos:
        for p in create_pods(e[0],e[1]):
            for d in dates.to_list():
                data = ET.SubElement(root, "DATA")
                ET.SubElement(data, "LOC-KEY").text = p
                ET.SubElement(data, "CHANNEL-NAME").text = "TESZT_CHANNEL_NAME"
                ET.SubElement(data, "VALUE-NAME").text = obis
                ET.SubElement(data, "VALUE-UNIT").text = "kWh"
                ET.SubElement(data, "T-FACTOR").text = "1"
                ET.SubElement(data, "INTERVAL").text = "00:15:00"
                ET.indent(data, space="")
                # block
                block = ET.SubElement(data, "BLOCK")
                ET.SubElement(block, "START-DATETIME").text = d.isoformat()
                # ET.indent(block, space=" ")
                for i in osp.get_solar_production_with_clouds_absolute():
                    E = ET.SubElement(block, "E")
                    ET.SubElement(E, "V").text = "1234.0000"
                    ET.SubElement(E, "F2").text = "W"
                    E.tail='\n'
                block.tail = '\n'
                data.tail='\n'
    return ET.ElementTree(root)

def generate_files(elo, podszam, batchsize):
    tree1 = generate1()    
    
    filename = f"e:/okosmeres/EHE_{elo}_15W-NKMENERGIA-6_{freq}_SM_Egyedi1_{gen_date}_{gen_time}_{batch_nr}.xml"
    
    if indent:
        ET.indent(tree1, space='    ', level=0)
    
    tree1.write(filename, 
        encoding="ISO-8859-1", 
        xml_declaration=True,
        short_empty_elements=True)
EHE110_15X-DEMASZ-ESZ-G_Napi_FF_Egyedi1_20240224_064530.xml
if __name__ == "__main__":
    for elo in om_piac:
        generate_files(elo["eloszto"], )
