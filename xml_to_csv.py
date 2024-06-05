import logging
import os
import hydra
import parse



logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def check_file_exists(full_path):
    # Construct the full path to the file
    
    # Check if the file exists
    if os.path.isfile(full_path):
        return True
    else:
        return False


@hydra.main(config_path="./conf", config_name="config", version_base=None)
def main(cfg):
    """
    XML Parsing tool: write a script to parse the downloaded XML file.
    """
    # Check if the file exists
    full_path = os.path.join(cfg.download.out_dir, 'LEXICON.xml')
    if check_file_exists(full_path):
        #If the download XML file exists, parse it with the parse_xml_to_dataframe function
        LOGGER.info("The LEXICON.xml file exists.")
        Base, InflVars, Noun_Prop, Adj_Prop, Adv_Prop, Acronyms, Abbreviations = parse.parse_xml_to_dataframe(os.path.join(cfg.download.out_dir, 'LEXICON.xml'))
        LOGGER.info(f"Parsing finished.")
        LOGGER.info(f"Writing the parsed data to CSV files...")
        # Write the parsed data to CSV files
        Base.to_csv(os.path.join(cfg.download.out_dir, 'Base.csv'), index=False)
        InflVars.to_csv(os.path.join(cfg.download.out_dir, 'InflVars.csv'), index=False)
        Noun_Prop.to_csv(os.path.join(cfg.download.out_dir, 'Noun_Prop.csv'), index=False)
        Adj_Prop.to_csv(os.path.join(cfg.download.out_dir, 'Adj_Prop.csv'), index=False)
        Adv_Prop.to_csv(os.path.join(cfg.download.out_dir, 'Adv_Prop.csv'), index=False)
        Acronyms.to_csv(os.path.join(cfg.download.out_dir, 'Acronyms.csv'), index=False)
        Abbreviations.to_csv(os.path.join(cfg.download.out_dir, 'Abbreviations.csv'), index=False)
        LOGGER.info(f"Writing finished.")
        return
        
    else:
        msg = f"Failed to find the file LEXICON.xml in {cfg.download.out_dir}"
        LOGGER.error(msg)
        raise FileNotFoundError(msg)
    
    
    
if __name__ == '__main__':
    main()    