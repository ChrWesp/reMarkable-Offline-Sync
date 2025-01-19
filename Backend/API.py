import logging
import requests
import warnings

from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)


class RemarkableAPI:

    def __init__(self, url):
        self.url = url
        if self.url[-1] == '/':  # clean up uri
            self.url = self.url[:-1]
        # TODO: add test, if URL can be accessed


    def check_response(self, request_response, use_uri, method='GET'):
        if request_response.status_code != 200:
            logger.error(f'Error fetcing {method} {use_uri}')
            return False
        return True


    def get_documents(self, guid=''):
        use_uri = self.url + f'/documents/{guid}'
        logger.debug(f'Get folder infos for GUID {guid} on URI {use_uri}')
        r = requests.get(use_uri)
        if self.check_response(r, use_uri=use_uri, method='GET'):
            # TODO: add json parse error checker?
            r.encoding = "utf-8"
            return self.get_relevant_fields(r.json())
        return {}


    
    def download_document(self, guid, file_path, filetype='pdf', ):
        # TODO: add raw rmdoc download
        # TOOD: add propper file logging / keep track of files which were not downloaded

        use_uri = self.url + f'/download/{guid}/{filetype}'

        try:
            # Send a GET request to the URL with stream=True
            logger.debug(f'Download {use_uri}')
            warnings.simplefilter("ignore", category=UserWarning)  # suppress warning from the reMarkable https server
            response = requests.get(use_uri, stream=False)  # reMarkable does not like chunkd
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

            # Open the file in binary write mode and write the content
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading the file: {e}")
            return False
        except IOError as e:
            logger.error(f"Error writing the file: {e}")
            return False    
        


    def get_relevant_fields(self, collection_data):
        parsed_data = []
        for entry in collection_data:
            item = {
                'ID':   entry['ID'],
                'date': entry['ModifiedClient'],
                'type': entry['Type'],
                'name': entry['VissibleName'],  # TODO fix encoding!
                'parent': entry['Parent'],
                'docType': entry.get('fileType'),
                # omitted: bookmarked, current page, fileType
            }
            parsed_data.append(item)
        return parsed_data


