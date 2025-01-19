import json
import logging
from Backend import Templates

from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__ + '.Utils')



def load_config(config_file):
    logger.debug(f'Opening config file: {config_file}')
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        logger.warning(f"Config file {config_file} not found or corrupted. Creating a default configuration file.")
        with open(config_file, 'w') as f:
            json.dump(Templates.DEFAULT_CONFIG, f, indent=4)
        return Templates.DEFAULT_CONFIG


## TODO: add named tuple structure for files and folders - if needed
def load_sync_database(sync_file):
    logger.debug(f'Loading sync database: {sync_file}')
    try:
        with open(sync_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        logger.warning(f"Sync database file {sync_file} not found or corrupted. Creating an empty one.")
        return Templates.DEFAULT_SYNC_DB


def save_sync_database(sync_db, sync_file):
    logger.debug(f'Saving sync database: {sync_file}')
    with open(sync_file, 'w') as f:
        json.dump(sync_db, f, indent=4)



### Function to parse the files and folders on the reMarkable:

def iterate_folder(api, folder_name, guid, file_tree, file_list):
    # get elements in folder
    logger.info(f'Fetching folder: {folder_name}')
    reMarkable_entries = api.get_documents(guid=guid)
    logger.debug(f'Found {len(reMarkable_entries)} items')
    for entry in reMarkable_entries:
        if entry['type'] == 'DocumentType':
            file_list.append((entry['ID'], entry))

        elif entry['type'] == 'CollectionType':
            folder_id = entry['ID']
            
            # jump to nested folder, use function recursion
            nested_file_tree = {}
            iterate_folder(api=api, folder_name=entry['name'], guid=folder_id, file_tree=nested_file_tree, file_list=file_list)
            file_tree[folder_id] = entry
            file_tree[folder_id]['subfolders'] = nested_file_tree  # append the subfolders
            

        else:
            raise NotImplementedError(f'Unkown document type: {entry['type']}')


def build_file_tree(api):
    file_tree = {'': ''}  # add base folder
    file_list = []
    # start building folder tree and file list
    iterate_folder(api=api, folder_name='My files', guid='', file_tree=file_tree, file_list=file_list)

    return file_tree, file_list


### Functions to handle folder and files on disk

def sync_folder_structure(tree: dict, base_folder: Path, folder_lookup: dict):
    for guid, folder_info in tree.items():
        if not guid:
            # base folder, ignore as base folder is already created
            folder_lookup[''] = base_folder.absolute()
            continue

        folder_name = folder_info['name']
        folder_path = Path(base_folder, folder_name)  # create physical 
        if not folder_path.exists():
            print(f"Creating folder: {folder_path}")
            folder_path.mkdir(parents=True)
        # TODO: add deletion of folders in sync_db!
        folder_lookup[guid] = folder_path.absolute()  # save full path to guid to path lookup for later file download

        sync_folder_structure(folder_info['subfolders'], base_folder / folder_name, folder_lookup)


def clean_filepath(filename: str):
    # remove illegal characters from (windows) file path and recreate filename
    invalid = '<>:"/\\|?* '
    new_filename = str(filename)
    had_to_replace = False
    for char in invalid:
        if char in new_filename:
            new_filename = new_filename.replace(char, ' ')
    if had_to_replace:
        logger.warning(f'Special characters from reMarkable filename had to be replaced. File "{str(filename)}" was replaced to "{new_filename}"')
    return new_filename