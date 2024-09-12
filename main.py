import os
import subprocess
import shutil
from push import *
from source_copy import *

def load_config():
    return {
        'source_directory': os.getenv('SOURCE_DIRECTORY'),
        'git_repo_url': os.getenv('GIT_REPO_URL'),
        'commit_message': os.getenv('COMMIT_MESSAGE')
    }

if __name__ == "__main__":
    ## Inputs##
    config = load_config()
    source_directory = config['source_directory']
    git_repo_url = config['git_repo_url']
    commit_message = config['commit_message']
       
    ## Values
    repo_name = git_repo_url.split('/')[-1].replace('.git', '')
    repo_path = os.path.join(os.getcwd(), repo_name)
    destination_directory = os.path.join(os.getcwd(), repo_name)

    ## Functions
    clone_repo(git_repo_url)
    print("Clone repo done.")

    remove_files_except_git(repo_path)
    print("Remove remote file done.")

    copy_project_files(source_directory, destination_directory)
    print("Copied files.")

    git_add_commit_push(repo_name, commit_message)
    print("Project is committed and pushed.")

    cleanup_directory(destination_directory)
    print("Success done!")
