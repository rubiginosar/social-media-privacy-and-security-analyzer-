import glob
import os

def execute_scripts_in_directory(directory):
    os.chdir(directory)  # Change to the specified directory
    
    # Fetch all Python files in the directory
    python_files = glob.glob("*.py")

    for script in python_files:
        with open(script) as f:
            script_content = f.read()
            exec(script_content)

# List of directories to process
directories = [
    "C:\\Users\\THINKPAD T470\\Desktop\\social-media-privacy-and-security-analyzer-\\facebook\\audience_and_visibility",
    "C:\\Users\\THINKPAD T470\\Desktop\\social-media-privacy-and-security-analyzer-\\facebook\\interactions"
]

# Execute scripts in each directory
for directory in directories:
    execute_scripts_in_directory(directory)
