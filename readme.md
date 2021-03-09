
Please read these documents before opening a new issue!


# Copyright

For more information about this work, please read the following paper:


    Yue Zhang et al. Brain Tumor Segmentation using Ensemble UNets with Different Inputs.

Please also cite this paper if you think our codes is helpful.


# Table of Contents
- [Dataset](#Dataset)
- [Usage](#usage)
  * [Preprocessing](#Preprocessing)
    + [Coregestrition](#Coregestrition)
	+ [Normalization](#Normalization)
	+ [Skull-stripping](#Skull-stripping])
  + [Summary](#Summary])
  * [Segmentation using Docker](#Segmentation-using-Docker)
* [Refenerce](#Reference)


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

The image size has also been changed.

|                                   | t1 | t2ce | t2| flair |
|-----------------------------------|----------------------------|---------------------|---------------------|---------------------|-----------------------|-------------------|
| Before                  |           256 $$\times$$ 320\times 19          |        69.07        |        73.22        |        82.27        |  
| After                 |            71.80           |        73.44        |        78.63        |        86.11        |   
|

### Normalization to 1mm

### Coregestrition

### Skull stripping

### Summary


```bash
bet <input> <output> [options]
```

# Segmentation using Docker

# Reference

