import os
import shutil
from pathlib import Path
import stat
import pathspec

def load_gitignore(project_dir):
    """Load the .gitignore file and compile the ignore patterns using pathspec."""
    gitignore_file = Path(project_dir) / ".gitignore"
    if not gitignore_file.exists():
        return None

    with open(gitignore_file, "r") as f:
        gitignore_content = f.read()
    
    # Compile the ignore patterns using pathspec
    spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, gitignore_content.splitlines())
    return spec

def should_ignore(file_path, spec, source_dir):
    """Check if the file matches any of the ignore patterns using pathspec."""
    if spec is None:
        return False

    # Get the relative path from the source directory
    rel_path = os.path.relpath(file_path, source_dir)
    
    # Special case: Ignore any .git directories
    if '.git' in Path(file_path).parts:
        return True

    # Match using the compiled spec
    return spec.match_file(rel_path)

def copy_project_files(source_dir, dest_dir):
    """Copy files from source_dir to dest_dir, excluding .gitignore files."""
    spec = load_gitignore(source_dir)

    for root, dirs, files in os.walk(source_dir):
        relative_path = os.path.relpath(root, source_dir)

        # Skip directories that should be ignored
        if should_ignore(root, spec, source_dir):
            continue

        # Create destination directory if it doesn't exist
        dest_subdir = Path(dest_dir) / relative_path
        if not dest_subdir.exists():
            dest_subdir.mkdir(parents=True, exist_ok=True)

        for file in files:
            file_path = os.path.join(root, file)
            if not should_ignore(file_path, spec, source_dir):
                dest_file_path = Path(dest_subdir) / file
                shutil.copy2(file_path, dest_file_path)

def cleanup_directory(directory):
    """Remove the destination directory and all its contents."""
    if Path(directory).exists():
        shutil.rmtree(directory, onerror=onerror)
        print(f"Deleted {directory}")

def onerror(func, path, exc_info):
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

# Example usage:
# source_directory = '/path/to/source'
# destination_directory = '/path/to/destination'
# copy_project_files(source_directory, destination_directory)
# cleanup_directory(destination_directory)
