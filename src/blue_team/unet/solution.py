from album.runner.api import get_args, setup
import sys

def run():
    import subprocess
    import os

    args = get_args()
    jupyter_working_dir = args.jupyter_working_dir

    os.environ["LD_LIBRARY_PATH"] = f"{os.environ['LD_LIBRARY_PATH']}:{os.environ['CONDA_PREFIX']}/lib"

    # run jupyter notebopok file in a subprocess
    subprocess.run(["jupyter", "lab", "--port=8888", "--notebook-dir=" + str(jupyter_working_dir)], cwd=str(jupyter_working_dir))

    print("Done")
    return 


setup(
    group="blue_team",
    name="unet2d",
    version="0.1.0",
    album_api_version="0.5.5",
    title="UNet 2D",
    description="Album solution for the UNet notebook",
    tags=["unet", "segmentation", "image", "2d"],
    cite=[{
        "text": "PaperTitle",
        "doi": "123/123",
    }],
    covers=[{
        "description": "UNet_prediction",
        "source": "cover.png"
    }],
    solution_creators=["blue_team", "motto", "Iván"],
    dependencies={"environment_file": "u-net_2d_zerocostdl4mic-latest.yml"},
    args=[
        {
            "name": "jupyter_working_dir",
            "description": "Path to the folder in which we want to run the jupyter notebook.",
            "default": "./",
            "required": False,
        }
    ],
    run=run,
)
