# Table of Contents
- [Dataset](#Dataset)
- [Usage](#usage)
  * [Preprocessing](#Preprocessing)
    + [Coregistration](#Coregistration)
	+ [Normalization](#Normalization)
	+ [Skull-stripping](#Skull-stripping])
    + [Summary](#Summary])
  * [Segmentation using Docker](#Segmentation-using-Docker)
    + [Download the Docker image](#Download-the-Docker-image)
    + [Using the Docker image](#Using-the-Docker-image)

- [Reference](#Reference)


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
**Test environment**: Python 3.8.5, NVIDIA driver 455.23.04

## Preprocessing for clinical dataset
The clinical data (in the folder "/Raw_data") has vairied image size and direction.
As such, we need to do some preprocessing to make is suitable to the BraTS dataset, the output of which is saved in the folder "/BraTS_Format".
Then, we will use one case "SYSU_0032" as the examle to show how to conduct the prprocessing.

### Coregistration
This step is used to aligin multi-modals images with difference size.

As shown in the followling table, the size of all images has also been changed to the same.



  |        | T1 | T2ce | T2| FLAIR |
  |--------|----|------|---|-------|
  | Before | 256\*320\*19  | 348\*384\*256 | 612\*768\*19  | 320\*320\*28  |
  | After  | 348\*384\*256 | 348\*384\*256 | 348\*384\*256 | 348\*384\*256 |

```bash
# bash
bash coregistration.sh "SYSU0032"
```

### Normalization to 1mm

```bash
# bash
python normalize.py --id "SYSU0032"
```

### Skull stripping

```bash
# bash
bash skull_stripping.sh "SYSU0032"
```

Then we use the skull mask of FLAIR MR images to all four modal 

```bash
# bash
python skull_stripping.py --id "SYSU0032"
```

### Summary

As shown in the following figure, the raw clinical can be transformed to the format like BraTS dataset step by step.


## Segmentation using Docker

### Download the Docker image


```bash
# bash
docker pull sustechmedical/brain_tumor_segmentation
```

### Using the Docker image

  |         | local path | path inside the Docker image | 
  |---------|------------|------------------------------|
  | Input path  | ./BraTS_Format/SYSU0032/ | /app/data/    |
  | Output path | ./Results                | /app/results/ |

```bash
# bash
docker run -it --rm --gpus all -v <-your-path>/BraTS_Format/SYSU0032/:/app/data/ -v <-your-path>/Results:/app/results/ sustechmedical/brain_tumor_segmentation python runner.py
```

# Reference

One example and the intermediate results for this example have been shared in [Google Drive](https://drive.google.com/drive/folders/1HQb4CuMmGDqIA6DdFXo20JDNxi77z5UL?usp=sharing).

For more information about this work, please read the following paper:

    Yue Zhang, Pinyuan Zhong, Dabin Jie, Jiewei Wu, Shanmei Zeng, Jianping Chu, Yilong Liu, Ed X. Wu and Xiaoying Tang. Brain Tumor Segmentation via Ensembling UNets with Different Inputs.

Please also cite our paper if you think our codes are helpful.

The implementation of UNet is based on the [nnUNet](https://github.com/MIC-DKFZ/nnUNet). 
Many thanks for their great work. 

    Isensee, F., Jaeger, P. F., Kohl, S. A., Petersen, J., & Maier-Hein, K. H. (2020). nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation. Nature Methods, 1-9.