import os
import subprocess
import shutil

def clone_repo(repo_url):
    subprocess.run(['git', 'clone', repo_url])

def remove_files_except_git(repo_path):
    for item in os.listdir(repo_path):
        item_path = os.path.join(repo_path, item)
        if item == '.git':
            continue
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

def git_add_commit_push(repo_path, commit_message):
    subprocess.run(['git', 'add', '.'], cwd=repo_path)
    subprocess.run(['git', 'commit', '-m', commit_message], cwd=repo_path)
    subprocess.run(['git', 'push'], cwd=repo_path)