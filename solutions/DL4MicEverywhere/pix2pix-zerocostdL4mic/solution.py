###album catalog: cellcanvas

# based on https://github.com/IvanHCenalmor/DL4MicEverywhere/blob/main/notebooks/ZeroCostDL4Mic_notebooks/pix2pix_DL4Mic/configuration.yaml
# and https://github.com/betaseg/solutions/blob/main/solutions/io.github.betaseg/cellsketch-plot/solution.py

import shutil

from album.runner.api import setup


def install():
    import requests
    from pathlib import Path
    from album.runner.api import get_app_path

    # URL of the notebook you want to download
    notebook_url = "https://raw.githubusercontent.com/HenriquesLab/ZeroCostDL4Mic/master/Colab_notebooks/pix2pix_ZeroCostDL4Mic.ipynb"
    
    notebook_path = get_app_path().joinpath("pix2pix_ZeroCostDL4Mic.ipynb")
    notebook_path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(notebook_url)
    response.raise_for_status()
    
    with open(notebook_path, 'wb') as notebook_file:
        notebook_file.write(response.content)
    
    assert notebook_path.exists(), "Notebook download failed"


def run():
    from album.runner.api import get_args, get_app_path, get_cache_path
    import papermill as pm
    import os
    import subprocess
    from pathlib import Path
    import shutil

    # Fetch arguments and paths
    args = get_args()
    app_path = get_app_path()
    
    # Path to the downloaded notebook
    notebook_path = app_path.joinpath("pix2pix_ZeroCostDL4Mic.ipynb")

    # Ensure the notebook exists
    assert notebook_path.exists(), "Notebook does not exist"

    # Output path for running the notebook
    output_path = args.path
    os.makedirs(output_path, exist_ok=True)
    print(f"Saving output to {output_path}")

    # Optionally, launch the Jupyter notebook to show the results
    subprocess.run(["jupyter", "notebook", str(notebook_path)], cwd=str(output_path))

setup(
    group="DL4MicEverywhere",
    name="pix2pix-zerocostdL4mic",
    version="0.1.0",
    solution_creators=["DL4Mic team", "album team"],
    title="pix2pix (2D) Implementation",
    description="Paired image-to-image translation of 2D images. pix2pix is a deep-learning method that can be used to translate one type of images into another. While pix2pix can potentially be used for any type of image-to-image translation, we demonstrate that it can be used to predict a fluorescent image from another fluorescent image. Note - visit the ZeroCostDL4Mic wiki to check the original publications this network is based on and make sure you cite these.",
    documentation="https://raw.githubusercontent.com/HenriquesLab/ZeroCostDL4Mic/master/BioimageModelZoo/README.md",
    tags=["colab", "notebook", "pix2pix", "ZeroCostDL4Mic", "2D", "dl4miceverywhere"],
    args=[{
        "name": "path",
        "type": "string",
        "default": ".",
        "description": "What is your working path?"
    }],
    cite=[{
        "text": "von Chamier, L., Laine, R.F., Jukkala, J. et al. Democratising deep learning for microscopy with ZeroCostDL4Mic. Nat Commun 12, 2276 (2021)",
        "doi": "https://doi.org/10.1038/s41467-021-22518-0"
    }, {
        "text": "Iván Hidalgo-Cenalmor, Joanna W Pylvänäinen, Mariana G Ferreira, Craig T Russell, Ignacio Arganda-Carreras, AI4Life Consortium, Guillaume Jacquemet, Ricardo Henriques, Estibaliz Gómez-de-Mariscal. DL4MicEverywhere: Deep learning for microscopy made flexible, shareable, and reproducible. bioRxiv 2023",
        "doi": "https://doi.org/10.1101/2023.11.19.567606"
    }, {
        "text": "Phillip Isola, Jun-Yan Zhu, Tinghui Zhou, Alexei A. Efros. Image-to-Image Translation with Conditional Adversarial Networks. arXiv:1611.07004.",
        "doi": "https://arxiv.org/abs/1611.07004"
    }],
    album_api_version="0.5.1",
    covers=[],
    run=run,
    install=install,
    dependencies={'environment_file': """channels:
- conda-forge
- defaults
dependencies:
- python=3.8
- ffmpeg
- papermill=2.3.4
- notebook=6.5.2
- git=2.39.2
- gitpython=3.1.31
- opencv==4.5.3
- pip
- pip:
    - astropy==5.2.2
    - Augmentor==0.2.12
    - bioimageio.core==0.5.11
    - dominate>=2.4.0, < 2.8.5
    - fpdf2==2.7.4
    - google==2.0.3
    - imageio==2.25.1
    - ipywidgets==8.0.7
    - lpips==0.1.4
    - matplotlib==3.7.1
    - numexpr==2.8.4
    - numpy==1.22.4
    - pandas==1.5.3
    - pathlib==1.0.1
    - pip==23.1.2
    - scikit-image==0.19.3
    - scikit-learn==1.2.2
    - scipy==1.10.1
    - tifffile==2023.7.10
    - torch==2.0.1
    - torchvision>=0.5.0, <0.15.5
    - tqdm==4.65.0
    - visdom>=0.1.8.8, < 0.2.5
    - wandb>= 0.15.0, < 0.16
    - -r "/Users/esti/Documents/PROYECTOS/DL4MicEverywhere/ALBUM/dl4miceverywhere-album/src/pix2pix_album/pytorch-CycleGAN-and-pix2pix/requirements.txt" 
"""}
)
