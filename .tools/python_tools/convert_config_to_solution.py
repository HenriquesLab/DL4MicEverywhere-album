import requests
import yaml
import sys
import os
import re

def convert_config_to_solution(config_path):
    # Use regular expressions tu extract the base path and the notebook folder
    DL4MicEverywhere_path, notebook_folder = re.findall(r"(.*).notebooks.ZeroCostDL4Mic_notebooks.(.*).configuration.yaml", config_path)[0]
    convert_config_to_solution(DL4MicEverywhere_path=DL4MicEverywhere_path, notebook_folder=notebook_folder)

def convert_config_to_solution(DL4MicEverywhere_path, notebook_folder):
    config_path = os.path.join(DL4MicEverywhere_path, "notebooks", "ZeroCostDL4Mic_notebooks", notebook_folder, "configuration.yaml") 
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"The configuration file {config_path} does not exist.")

    online_config_path = f"https://github.com/HenriquesLab/DL4MicEverywhere/blob/main/notebooks/ZeroCostDL4Mic_notebooks/{notebook_folder}/configuration.yaml"

    # Load the configuration
    with open(config_path, "r") as f:
        config_data = yaml.safe_load(f)

    # Extract the values from the configuration file
    notebook_url = config_data["config"]["dl4miceverywhere"]["notebook_url"]
    notebook_name = os.path.basename(notebook_url)
    sections_to_remove = config_data["config"]["dl4miceverywhere"]["sections_to_remove"]
    version = config_data["version"]
    tags = config_data["tags"]
    cite = config_data["cite"]
    description = config_data["description"]
    python_version = config_data["config"]["dl4miceverywhere"]["python_version"]
    cuda_toolkit_version = config_data["config"]["dl4miceverywhere"]["cuda_version"]
    cudnn_version = config_data["config"]["dl4miceverywhere"]["cudnn_version"]
    # Fix the cuDNN version to fit the conda library
    cudnn_version = re.search(r"\d+\.\d+\.\d+", cudnn_version).group()

    # Others need to be created
    name = notebook_name.lower().replace(".ipynb", "").replace("_", "-")
    title = f"{name} implementation."

    # And finally, the requirements file needs to downloaded and processed
    response = requests.get(config_data["config"]["dl4miceverywhere"]["requirements_url"])
    response.raise_for_status()

    requirements_text = response.text
    requirements = requirements_text.split("\n")[1:]
    requirements = [f"    - {r}" for r in requirements if r]

    # Add additional requirements
    if python_version in ["3.8", "3.9", "3.10", "3.11"]:
        # For Python between 3.8 and 3.11
        nbformat_version = "5.9.2"
    else:
        # For Python 3.7 or lower
        nbformat_version = "5.0.2"

    if python_version in ["3.7", "3.8", "3.9", "3.10", "3.11"]:
        # For Python between 3.7 and 3.11
        ipywidgets_version = "8.1.0"
        jupyterlab_version = "3.4.0"
    elif python_version in ["3.6", "3.5"]:
        # For Python 3.5 and 3.6
        ipywidgets_version = "8.0.0a0"
        jupyterlab_version = "2.3.2"
    else:
        # For Python 3.4 or lower
        ipywidgets_version = "7.8.1"
        jupyterlab_version = "0.23.0"

    if "nbformat" not in requirements_text:
        requirements.append(f"    - nbformat=={nbformat_version}")
    if "ipywidgets" not in requirements_text:
        requirements.append(f"    - ipywidgets=={ipywidgets_version}")
    if "jupyterlab" not in requirements_text:
        requirements.append(f"    - jupyterlab=={jupyterlab_version}")

    requirements = "\n".join(requirements)
        
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "solution_template"), "r") as album_template:
        solution_file_text = album_template.read()

    # Replace the placeholders in the template
    solution_file_text = solution_file_text.replace("CONFIG_PATH", str(online_config_path))
    solution_file_text = solution_file_text.replace("NOTEBOOK_URL", str(notebook_url))
    solution_file_text = solution_file_text.replace("NOTEBOOK_NAME", str(notebook_name))
    solution_file_text = solution_file_text.replace("SECTIONS_TO_REMOVE", str(sections_to_remove))
    solution_file_text = solution_file_text.replace("NAME", str(name))
    solution_file_text = solution_file_text.replace("TITLE", str(title))
    solution_file_text = solution_file_text.replace("DESCRIPTION", str(description))
    solution_file_text = solution_file_text.replace("TAGS", str(tags))
    solution_file_text = solution_file_text.replace("CITE", str(cite))
    solution_file_text = solution_file_text.replace("PYTHON_VERSION", str(python_version))
    solution_file_text = solution_file_text.replace("CUDATOOLKIT_VERSION", str(cuda_toolkit_version))
    solution_file_text = solution_file_text.replace("CUDNN_VERSION", str(cudnn_version))
    solution_file_text = solution_file_text.replace("REQUIREMENTS", str(requirements))
    solution_file_text = solution_file_text.replace("NBFORMAT_VERSION", str(nbformat_version))
    solution_file_text = solution_file_text.replace("IPYWIDGETS_VERSION", str(ipywidgets_version))
    solution_file_text = solution_file_text.replace("JUPYTERLAB_VERSION", str(jupyterlab_version))
    ## Needs to be the last one to avoid conflicts with PYTHON_VERSION, CUDATOOLKIT_VERSION and CUDNN_VERSION
    solution_file_text = solution_file_text.replace("VERSION", str(version))

    # Create the album folder
    album_folder_name = notebook_folder.replace("DL4Mic", "album")
    repository_folder_path = os.sep.join(os.path.dirname(os.path.abspath(__file__)).split(os.sep)[:-1])
    album_folder_path = os.path.join(repository_folder_path, "src", album_folder_name)
    print(album_folder_path)
    os.makedirs(album_folder_path, exist_ok=True)

    # Write the solution file
    with open(os.path.join(album_folder_path, "solution.py"), "w") as solution_file:
        solution_file.write(solution_file_text)

def main(dl4miceverywhere_path=None):

    # Check if paths to the repositories have been provided and if not, it will be assumed that they are located in the same folder.
    if dl4miceverywhere_path is None:
        dl4miceverywhere_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', '..', 'DL4MicEverywhere'))

    notebook_path = os.path.join(dl4miceverywhere_path, "notebooks", "ZeroCostDL4Mic_notebooks")
    
    for notebook_name in os.listdir(notebook_path):
        if os.path.isdir(os.path.join(notebook_path, notebook_name)):
            convert_config_to_solution(DL4MicEverywhere_path=dl4miceverywhere_path, notebook_name=notebook_name)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        # Precondition: Both DL4MicEverywhere and DL4Miceverywhere-album need to be located in the same folder.
        # This can be done on GitHub CI with a double checkout. 
        sys.exit(main())
    elif len(sys.argv) == 2:
        # Configuration path is provided
        sys.exit(convert_config_to_solution(config=sys.argv[1]))
    elif len(sys.argv) == 3:
        # DL4MicEverywhere path and notebook_folder name are provided
        sys.exit(convert_config_to_solution(DL4MicEverywhere_path=sys.argv[1], notebook_name=sys.argv[2]))
    else:
        sys.exit(1)