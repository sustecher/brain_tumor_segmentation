# Table of Contents
- [Dataset](#Dataset)
- [Usage](#usage)
  * [Preprocessing](#Preprocessing)
    + [Coregestrition](#Coregestrition)
	+ [Normalization](#Normalization)
	+ [Skull-stripping](#Skull-stripping])
    + [Summary](#Summary])
  * [Segmentation using Docker](#Segmentation-using-Docker)
    + [Download the Docker image](#Download-the-Docker-image)

- [Refenerce](#Reference)


# Dataset
For our self-obtained data, for example, this looks like this:

    SYSU
    ├── Raw_data
    │   └── SYSU0032
    │       ├──SYSU0032_t1.nii.gz
    |       ├──SYSU0032_t1ce.nii.gz
    |       ├──SYSU0032_t2.nii.gz          
    |       ├──SYSU0032_flair.nii.gz
    ├── BraTS_Format
    │   └── SYSU0032
    │       ├──SYSU0032_t1.nii.gz
    |       ├──SYSU0032_t1ce.nii.gz
    |       ├──SYSU0032_t2.nii.gz          
    |       ├──SYSU0032_flair.nii.gz

# Usage

## Preprocessing for clinical dataset
The clinical data (in folder "/Raw_data") has vaired images size and direction.
As such, we need to do some preprocessing to make is suitable to the BraTS dataset, the output of which is saved in folder "/BraTS_Format".
Then, we will use one case "SYSU_0032" as the examle to show how to conduct the prprocessing.

### Coregestrition
This step 
The image size has also been changed.

  |         | T1 | T2ce | T2| FLAIR |
  |---------|----|------|---|----|
  | Before  |256\*320\*19| 348\*384\*256  |612\*768\*19|320\*320\*28| 
  | After   |348\*384\*256|348\*384\*256 |348\*384\*256 |348\*384\*256|   

```bash
fsl ./Raw_data/SYSU0032/ ./Coregistration/SYSU0032/ 
```

### Normalization to 1mm
We define the 3D resizing function as follow.

```bash
from scipy import ndimage as nd
Normlize_VS=[1,1,1]
def ThreeD_resize(imgs,Normlize_VS,img_vs): 
   #order The order of the spline interpolation, default is 3. The order has to be in the range 0-5. 
   zf0=img_vs[0]/Normlize_VS[0] 
   zf1=img_vs[1]/Normlize_VS[1] 
   zf2=img_vs[2]/Normlize_VS[2] 
   new_imgs = nd.zoom(imgs, [zf0, zf1, zf2], order=0) 
   return new_imgs
```


### Skull stripping

### Summary

As shown in the following figure, the raw clinical can be transformed to the format like BraTS dataset step by step.


## Segmentation using Docker

### Download the Docker image


```bash
docker pull sustechmedical/brain_tumor_segmentation
```


# Reference

For more information about this work, please read the following paper:

    Yue Zhang et al. Brain Tumor Segmentation using Ensemble UNets with Different Inputs.

Please also cite this paper if you think our codes is helpful.


The implementation of UNet is based on the https://github.com/MIC-DKFZ/nnUNet