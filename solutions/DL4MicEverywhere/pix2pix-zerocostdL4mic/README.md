# Conditional generative model for Image-to-Image Translation

## Description
This notebook reproduces the training, evaluation and inference of a conditional cycle-Generative Adversarial Network (cycleGAN), popularly known as pix2pix, to transform images from one domain into another (e.g., to predict a DAPI nuclei staining fluorescence channel from a brightfield image of cells). 
The conditional cycleGAN allows for a supervised training of the network. 
Thus, pix2pix is trained using a pair set of images. 
This is a DL4MicEverywhere notebook developed upon the work “Image-to-Image Translation with Conditional Adversarial Networks" by Isola et al. (https://arxiv.org/abs/1611.07004).
Further details about how to train a similar model are given in [ZeroCostDL4Mic wiki](https://github.com/HenriquesLab/ZeroCostDL4Mic/wiki).

 ## Reference and Citation
If you use this notebook for your research, please refer to the ZeroCostDL4Mic paper, DL4MicEverywhere paper and the original Pix2Pix model paper:
			
- von Chamier, L., Laine, R.F., Jukkala, J. et al. Democratising deep learning for microscopy with ZeroCostDL4Mic. Nat Commun 12, 2276 (2021). https://doi.org/10.1038/s41467-021-22518-0
- Hidalgo-Cenalmor, I., Pylvänäinen, J.W., Ferreira, M.G., et al. DL4MicEverywhere: Deep learning for microscopy made flexible, shareable, and reproducible. bioRxiv (2023). https://doi.org/10.1101/2023.11.19.567606
- Isola, P., Zhu, J. Y., Zhou, T., & Efros, A. A. Image-to-Image Translation with Conditional Adversarial Networks (2016). arXiv preprint arXiv:1611.07004



