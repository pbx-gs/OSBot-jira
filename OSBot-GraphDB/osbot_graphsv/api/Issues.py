from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Json import Json


class Issues:

    def __init__(self,file_system):
        self.file_system = file_system
        self.filename_metadata = 'metadata.json'

    def by_issue_type(self,issue_type_name, indexed_by=None):
        data = []
        file_filter = "{0}/{1}/{2}".format(self.file_system.folder_data, issue_type_name ,'*.json')
        for path in Files.find(file_filter):
            if self.filename_metadata not in path:          # don't load metadata file
                data.append(Json.load_json(path))
        if indexed_by is None:
            return data
        indexed_data = {}
        for item in data:
            key   = item.get('Key')
            index = item.get(indexed_by)
            if index:
                if indexed_data.get(index) is None: indexed_data[index] = {}
                indexed_data[index][key] = item
        return indexed_data


    def roles(self, indexed_by='Summary'):
        return self.by_issue_type('Role', indexed_by)

    def persons(self, indexed_by='Summary'):
        return self.by_issue_type('Person', indexed_by)




    # def all(self):
    #     data = []
    #     file_filter = Files.path_combine(self.file_system.folder_data, '**/*.json')
    #     for path in Files.find(file_filter):
    #         if self.filename_metadata not in path:          # don't load metadata file
    #             data.append(Json.load_json(path))
    #     return data