import argparse
import json
import logging
import os
from pathlib import Path

import Backend.API
import Backend.Utils
import Backend.Templates

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Sync files from a reMarkable tablet via USB HTTP REST API.")
    parser.add_argument("--clearDB", action="store_true", help="Clear the sync database.")
    parser.add_argument("--forceSync", action="store_true", help="Force sync all files, even if they do not appear different.")
    #parser.add_argument("--configFile", type=str, default="reMarkable_db.json", help="Path to the config file (default: reMarkable_db.json).")
    parser.add_argument("--configFile", type=str, default="sync_config.json", help="Path to the config file which includes sync parameters.")
    parser.add_argument("--debug", action="store_true", help="Enable verbose debugging output.")
    return parser.parse_args()




def main():
    args = parse_arguments()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    config = Backend.Utils.load_config(args.configFile)

    if args.clearDB:
        # clear and reset the database which keeps tracks of synced files
        Backend.Utils.save_sync_database(Backend.Templates.DEFAULT_SYNC_DB, config['syncDatabase'])
        logger.info("Sync database cleared.")
        return

    sync_db = Backend.Utils.load_sync_database(args.configFile)  # not used yet
    api = Backend.API.RemarkableAPI(config['url'])

    ## Main loop

    # create list of all existing files and folders on the reMarkable
    file_tree, file_list = Backend.Utils.build_file_tree(api=api)


    # setup base folder, and create if non-existing
    base_folder = Path(config['baseFolder'])
    if not base_folder.exists():
        logger.info(f'Creating folder to sync reMarkable files: {base_folder.absolute()}')
        base_folder.mkdir(parents=True)

    
    # sync the folder structure
    folder_lookup = {}
    Backend.Utils.sync_folder_structure(file_tree, base_folder, folder_lookup)

    # now check in sync db which files to download, to delete and to ignore
    # TODO: has to be implemented

    # download all files from the remarkable
    logger.info('Sync files do download')

    for guid, file in file_list:
        file_name = Backend.Utils.clean_filepath(file['name'])
        folder_guid = file['parent']
        folder_path = folder_lookup[folder_guid]
        file_path = Path(folder_path) / (file_name + '.pdf')  # TODO: add option for rmdoc
        # todo: add pdf of 
        logger.info(f'Download file {file_name} from reMarkable to {folder_path}')
        api.download_document(guid, file_path=file_path, filetype='pdf')

    logger.info('Done')


if __name__ == "__main__":
    main()
