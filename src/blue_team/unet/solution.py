from album.runner.api import setup
from pathlib import Path


env_file = """channels:
  - conda-forge
  - nvidia
  - anaconda
  - defaults
dependencies:
  - python=3.10
  - cudatoolkit=11.2.2
  - cudnn=8.1.0
  - pip
  - pkg-config
  - pip:
    - unzip
    - GitPython
    - PTable==0.9.2
    - Pillow==8.4.0
    - bioimageio.core==0.5.9
    - data==0.4
    - fpdf2==2.7.4
    - future==0.18.3
    - google==2.0.3
    - matplotlib==3.7.1
    - numexpr==2.8.4
    - numpy==1.22.4
    - pandas==1.5.3
    - pathlib==1.0.1
    - pip==23.1.2
    - requests==2.28.0
    - scikit-image==0.19.3
    - scikit-learn==1.2.2
    - scipy==1.10.1
    - tensorflow==2.12.0
    - tifffile==2023.7.4
    - tqdm==4.65.0
    - wget==3.2
    - zarr==2.15.0
    - nbformat==5.9.2
    - ipywidgets==8.1.0
    - jupyterlab==3.6.0
name: dl4miceverywhere
"""


def install():
    from album.runner.api import get_app_path
    from git import Repo
    import subprocess
    import requests
    import shutil
    import os

    # Clone the DL4MicEverywhere repository
    clone_url = "https://github.com/HenriquesLab/DL4MicEverywhere"
    to = get_app_path().joinpath("DL4MicEverywhere")
    Repo.clone_from(clone_url, to)
    assert (to.exists())

    # Download the notebook that will execute the solution
    notebook_name = "U-Net_2D_ZeroCostDL4Mic.ipynb"
    notebook_url = f"https://raw.githubusercontent.com/HenriquesLab/ZeroCostDL4Mic/master/Colab_notebooks/{notebook_name}"
    
    notebook_path = get_app_path().joinpath(notebook_name)
    notebook_path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(notebook_url)
    response.raise_for_status()
    
    with open(notebook_path, 'wb') as notebook_file:
        notebook_file.write(response.content)
    
    assert notebook_path.exists(), "Notebook download failed"

    # Convert the notebook to its colabless form
    subprocess.run(["python", ".tools/notebook_autoconversion/transform.py", "-p", f"{get_app_path()}", "-n", f"{notebook_name}", "-s", "1.1.", "1.2.", "2.", "6.3."], cwd=to)
    subprocess.run(["mv", get_app_path().joinpath(f"colabless_{notebook_name}"), get_app_path().joinpath(f"{notebook_name}")])

    # Remove the cloned DL4MicEverywhere repository
    if os.name == 'nt':
        os.system(f'rmdir /s /q "{to}"')
    else:
        shutil.rmtree(to) # rmtree has no permission to do this on Windows

def run():
    from album.runner.api import get_args, get_app_path
    import subprocess
    import os

    # Fetch arguments and paths
    args = get_args()
    app_path = get_app_path()
    
    # Path to the downloaded notebook
    notebook_path = app_path.joinpath("U-Net_2D_ZeroCostDL4Mic.ipynb")

    # Ensure the notebook exists
    assert notebook_path.exists(), f"Notebook {notebook_path} does not exist"

    # Output path for running the notebook
    output_path = args.path
    os.makedirs(output_path, exist_ok=True)
    print(f"Saving output to {output_path}")

    # Set the LD_LIBRARY_PATH to allow TensorFlow to find the CUDA libraries
    os.environ["LD_LIBRARY_PATH"] = f"{os.environ['LD_LIBRARY_PATH']}:{os.environ['CONDA_PREFIX']}/lib"

    # Optionally, launch the Jupyter notebook to show the results
    subprocess.run(["jupyter", "lab", str(notebook_path)], cwd=str(output_path))


setup(
    group="blue_team",
    name="unet2d-zerocostdL4mic",
    version="0.1.0",
    album_api_version="0.5.1",
    title="U-Net 2D",
    description="2D binary segmentation. U-Net is an encoder-decoder architecture originally used for image segmentation. The first half of the U-Net architecture is a downsampling convolutional neural network which acts as a feature extractor from input images. The other half upsamples these results and restores an image by combining results from downsampling with the upsampled images. Note - visit the ZeroCostDL4Mic wiki to check the original publications this network is based on and make sure you cite these.",
    documentation="https://raw.githubusercontent.com/HenriquesLab/ZeroCostDL4Mic/master/BioimageModelZoo/README.md",
    covers=[],
    cite=[{
        "text": "von Chamier, L., Laine, R.F., Jukkala, J. et al. Democratising deep learning for microscopy with ZeroCostDL4Mic. Nat Commun 12, 2276 (2021)",
        "doi": "https://doi.org/10.1038/s41467-021-22518-0"
    }, {
        "text": "Iván Hidalgo-Cenalmor, Joanna W Pylvänäinen, Mariana G Ferreira, Craig T Russell, Ignacio Arganda-Carreras, AI4Life Consortium, Guillaume Jacquemet, Ricardo Henriques, Estibaliz Gómez-de-Mariscal. DL4MicEverywhere: Deep learning for microscopy made flexible, shareable, and reproducible. bioRxiv 2023",
        "doi": "https://doi.org/10.1101/2023.11.19.567606"
    }, {
        "text": "Ronneberger, Olaf, Philipp Fischer, and Thomas Brox. U-net: Convolutional networks for biomedical image segmentation. Medical image computing and computer-assisted intervention–MICCAI 2015: 18th international conference, Munich, Germany, October 5-9, 2015, proceedings, part III 18. Springer International Publishing, 2015.",
        "doi": "https://doi.org/10.48550/arXiv.1505.04597"
    }, {
        "text": "Falk, T., Mai, D., Bensch, R. et al. U-Net: deep learning for cell counting, detection, and morphometry. Nat Methods 16, 67–70 (2019).",
        "doi": "https://doi.org/10.1038/s41592-018-0261-2"
    }],
    solution_creators=["DL4MicEverywhere team", "album team"],
    dependencies={"environment_file": env_file},
    tags=["unet", "segmentation", "colab", "notebook", "U-Net", "ZeroCostDL4Mic", "2D", "dl4miceverywhere"],
    args=[
        {
            "name": "path",
            "type": "string",
            "default": ".",
            "description": "What is your working path?"
        }
    ],
    run=run,
    install=install,
)
