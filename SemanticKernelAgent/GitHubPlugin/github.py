import os
import json
import requests  
from config import CONSTS
from semantic_kernel.functions import kernel_function
from utils.constants import LIST_OF_PROJECTS, LIST_OF_FILES, READ_CONTENTS

header = {"Accept": "application/vnd.github+json",
          "Authorization": f"{CONSTS.git_hub_pat}",
          "X-GitHub-Api-Version": "2022-11-28"} 


class GitHubPlugin():
    
    """GitHub data fetch like projects """
    
    @kernel_function(description="search for all projects with the given username")
    def get_all_projects(self, user_name):        
        print("plugin::get_all_projects")
        
        proj_list = []
        auth_response = requests.get(url=LIST_OF_PROJECTS.format(user_name),headers=header)
        
        if auth_response.status_code==200:
            response = json.loads(auth_response.text)
            for res in response:
                proj_list.append(res['name'])
            return proj_list
        else:
            return "Unable to fetch the project list"
            
  
    @kernel_function(description="fetch the list of files using repository name and owner name")
    def get_repository_tree(self, owner_name, repository_name):
        print("plugin::get_repository_tree")
        """Fetch the repository tree (list of all files).""" 
        
        api_url = LIST_OF_FILES.format(owner_name,repository_name)
            
        def get_file_paths(url):  
        
            auth_response = requests.get(url, headers=header)  
            if auth_response.status_code==200:
                response=json.loads(auth_response.text)  
              
                paths = []  
                for item in response:  
                    if item["type"] == "file":  
                        paths.append(item["path"])  
                    elif item["type"] == "dir":  
                        paths.extend(get_file_paths(item["url"]))  
                return paths  
            
            else:
                return "Error in processing files"
        
        return get_file_paths(api_url)
      
    @kernel_function(description="fetch the contents of the selected file using owner_name, repository_name and file_path of the file")
    def get_file_contents(self, owner_name, repository_name, file_path):  
        print("plugin::get_file_contents")
        """Fetch the contents of a specific file."""  
        
        api_url = READ_CONTENTS.format(owner_name,repository_name, file_path)
        auth_response = requests.get(api_url, headers=header)  
        
        if auth_response.status_code==200:
            response = auth_response.text
            return response
        else: 
            return "Unable to retrieve the file contents" 