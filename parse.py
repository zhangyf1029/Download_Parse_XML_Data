import logging
import os
import pandas as pd
import xml.etree.ElementTree as ET


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def parse_xml_to_dataframe(local_path):
    try:
        LOGGER.info(f"Parsing the XML file: {local_path}")
        # Parse the XML file
        tree = ET.parse(local_path)
        root = tree.getroot()
        # Initialize a list to hold the parsed data
        Base_data = []
        InflVars_data  = []
        Noun_Prop = []
        Adj_Prop = []
        Adv_Prop = []
        Acronyms_data = []
        Abbreviations_data = []
        # Iterate through the XML tree
        for child in root:
            # Extract the Base data from the XML tree
            curr_base = {
                'base': child.find('base').text,
                'eui': child.find('eui').text,
                'cat': child.find('cat').text,
            }
            if child.find('spellingVars') is not None:
                curr_base['spellingVars'] = child.find('spellingVars').text    
            Base_data.append(curr_base) 
            
            # Extract the InflVars data from the XML tree    
            for element in child.findall('inflVars'):
                curr_InflVars = {**element.attrib, **{'inflVars': element.text}}
                InflVars_data.append(curr_InflVars)
            
            # Extract the Acronyms and Abbreviations data from the XML tree   
            for element in child.findall('acronyms'):
                try:
                    Acronyms, Acronyms_EUI = element.text.strip().split('|')
                except:
                    Acronyms = element.text.strip()
                    Acronyms_EUI = ''
                curr_Acronyms = {
                    'eui': child.find('eui').text,
                    'acronyms': Acronyms,
                    'acronyms_eui': Acronyms_EUI
                }
                Acronyms_data.append(curr_Acronyms)
                
            for element in child.findall('abbreviations'):
                try:
                    Abbreviations, Abbreviations_EUI = element.text.strip().split('|')
                except:
                    Abbreviations = element.text.strip()
                    Abbreviations_EUI = ''
                curr_Abbreviations = {
                    'eui': child.find('eui').text,
                    'abbreviations': Abbreviations,
                    'abbreviations_eui': Abbreviations_EUI
                }
                Abbreviations_data.append(curr_Abbreviations)
                
            # Extract the Noun, Adj, and Adv properties from the XML tree
            curr_prop = {'eui':child.find('eui').text}
            if child.find('cat').text == 'noun':
                for subchild in child.find('nounEntry'):
                    curr_prop[subchild.tag] = subchild.text
                Noun_Prop.append(curr_prop)
            elif child.find('cat').text == 'adj':
                for subchild in child.find('adjEntry'):
                    curr_prop[subchild.tag] = subchild.text
                Adj_Prop.append(curr_prop)
            elif child.find('cat').text == 'adv':
                for subchild in child.find('advEntry'):
                    curr_prop[subchild.tag] = subchild.text
                Adv_Prop.append(curr_prop)

        return pd.DataFrame(Base_data), pd.DataFrame(InflVars_data), pd.DataFrame(Noun_Prop), pd.DataFrame(Adj_Prop),\
            pd.DataFrame(Adv_Prop), pd.DataFrame(Acronyms_data), pd.DataFrame(Abbreviations_data) 
    
    except ET.ParseError as e:
        LOGGER.error(f"ParseError: {e}") 
