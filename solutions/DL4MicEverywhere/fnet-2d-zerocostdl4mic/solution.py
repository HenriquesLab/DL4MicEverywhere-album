###album catalog: cellcanvas

# Based on https://github.com/HenriquesLab/DL4MicEverywhere/blob/main/notebooks/ZeroCostDL4Mic_notebooks/fnet_2D_DL4Mic/configuration.yaml
# and https://github.com/betaseg/solutions/blob/main/solutions/io.github.betaseg/cellsketch-plot/solution.py

from album.runner.api import setup
import subprocess

try:
    subprocess.check_output('nvidia-smi')
    gpu_access = True
except Exception: 
    gpu_access = False

def install():
    from album.runner.api import get_app_path
    from git import Repo
    import subprocess
    import requests
    import shutil
    import os

    # Clone the DL4MicEverywhere repository
    clone_url = "https://github.com/HenriquesLab/DL4MicEverywhere"
    repo_path = get_app_path().joinpath("DL4MicEverywhere")
    Repo.clone_from(clone_url, repo_path)
    assert (repo_path.exists())

    # URL of the notebook you want to download
    notebook_url = "https://raw.githubusercontent.com/HenriquesLab/ZeroCostDL4Mic/master/Colab_notebooks/fnet_2D_ZeroCostDL4Mic.ipynb"
    
    notebook_path = get_app_path().joinpath("fnet_2D_ZeroCostDL4Mic.ipynb")
    notebook_path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(notebook_url)
    response.raise_for_status()
    
    with open(notebook_path, 'wb') as notebook_file:
        notebook_file.write(response.content)
    
    assert notebook_path.exists(), "Notebook download failed"

    # Convert the notebook to its colabless form
    section_to_remove = "1.1. 1.2. 2. 6.3."
    section_to_remove = section_to_remove.split(' ')
    
    python_command = ["python", ".tools/notebook_autoconversion/transform.py", "-p", f"{get_app_path()}", "-n", "fnet_2D_ZeroCostDL4Mic.ipynb", "-s"]
    python_command += section_to_remove

    subprocess.run(python_command, cwd=to)
    subprocess.run(["mv", get_app_path().joinpath("colabless_fnet_2D_ZeroCostDL4Mic.ipynb"), get_app_path().joinpath("fnet_2D_ZeroCostDL4Mic.ipynb")])

    # Remove the cloned DL4MicEverywhere repository
    if os.name == 'nt':
        os.system(f'rmdir /s /q "{to}"')
    else:
        # rmtree has no permission to do this on Windows
        shutil.rmtree(to) 

def run():
    from album.runner.api import get_args, get_app_path
    import subprocess
    import os

    # Fetch arguments and paths
    args = get_args()
    app_path = get_app_path()
    
    # Path to the downloaded notebook
    notebook_path = app_path.joinpath("fnet_2D_ZeroCostDL4Mic.ipynb")

    # Ensure the notebook exists
    assert notebook_path.exists(), "Notebook does not exist"

    # Output path for running the notebook
    output_path = args.path
    os.makedirs(output_path, exist_ok=True)
    print(f"Saving output to {output_path}")

    # Set the LD_LIBRARY_PATH to allow TensorFlow to find the CUDA libraries
    global gpu_access
    if gpu_access:
        os.environ["LD_LIBRARY_PATH"] = f"{os.environ['LD_LIBRARY_PATH']}:{os.environ['CONDA_PREFIX']}/lib"

    # Optionally, launch the Jupyter notebook to show the results
    subprocess.run(["jupyter", "lab", str(notebook_path)], cwd=str(output_path))

if gpu_access:
    channels = """
- conda-forge
- nvidia
- anaconda
- defaults
"""
    dependencies = """
- python=3.7
- cudatoolkit=11.8.0
- cudnn=8.6.0
- pip
- pkg-config
"""
else:
    channels = """
- conda-forge
- defaults
"""
    dependencies = f"""
- python=3.7
- pip
- pkg-config
"""

env_file = f"""
channels:
{channels}
dependencies:
{dependencies}
- pip:
    - GitPython==3.1.43 
    - certifi==2020.12.5
    - chardet==3.0.4
    - fpdf==1.7.2
    - gast==0.2.2
    - google==2.0.3
    - h5py==2.10.0
    - httplib2==0.17.4
    - idna==2.10
    - image==1.5.33
    - imageio==2.4.1
    - multiprocess==0.70.11.1
    - numpy==1.19.5
    - oauth2client==4.1.3
    - opencv-python==3.4.14.53
    - pandas==1.2.3
    - portpicker==1.3.1
    - protobuf==3.20.*
    - py==1.10.0
    - pyasn1==0.4.8
    - pydot==1.3.0
    - requests==2.23.0
    - rsa==4.7.2
    - scipy==1.2.0
    - scikit-image==0.18.0
    - six==1.15.0
    - tensorboard==1.15.0
    - tensorflow==1.15.2
    - termcolor==1.1.0
    - uritemplate==3.0.1
    - urllib3==1.24.3
    - wrapt==1.12.1
"""

setup(
    group="DL4MicEverywhere",
    name="fnet-2d-zerocostdl4mic",
    version="1.14.1",
    solution_creators=["DL4Mic team", "album team"],
    title="fnet-2d-zerocostdl4mic implementation.",
    description="Paired image-to-image translation of 2D images. Label-free Prediction (fnet) is a neural network used to infer the features of cellular structures from brightfield or EM images without coloured labels. The network is trained using paired training images from the same field of view, imaged in a label-free (e.g. brightfield) and labelled condition (e.g. fluorescent protein). When trained, this allows the user to identify certain structures from brightfield images alone. The performance of fnet may depend significantly on the structure at hand. Note - visit the ZeroCostDL4Mic wiki to check the original publications this network is based on and make sure you cite these.",
    documentation="https://raw.githubusercontent.com/HenriquesLab/ZeroCostDL4Mic/master/BioimageModelZoo/README.md",
    tags=['colab', 'notebook', 'fnet', 'labelling', 'ZeroCostDL4Mic', '2D', 'dl4miceverywhere'],
    args=[{
        "name": "path",
        "type": "string",
        "default": ".",
        "description": "What is your working path?"
    }],
    cite=[{'doi': 'https://doi.org/10.1038/s41467-021-22518-0', 'text': 'von Chamier, L., Laine, R.F., Jukkala, J. et al. Democratising deep learning for microscopy with ZeroCostDL4Mic. Nat Commun 12, 2276 (2021). https://doi.org/10.1038/s41467-021-22518-0'}, {'doi': 'https://doi.org/10.1038/s41592-018-0111-2', 'text': 'Ounkomol, C., Seshamani, S., Maleckar, M.M. et al. Label-free prediction of three-dimensional fluorescence images from transmitted-light microscopy. Nat Methods 15, 917–920 (2018). https://doi.org/10.1038/s41592-018-0111-2'}],
    album_api_version="0.5.1",
    covers=[],
    run=run,
    install=install,
    dependencies={"environment_file": env_file},
)
