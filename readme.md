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
    + [Using the Docker image](#Using-the-Docker-image)

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
This step is used to aligin multi-modals images with difference size.

As shown in the followling table, the image size has also been changed to the same.



  |         | T1 | T2ce | T2| FLAIR |
  |---------|----|------|---|----|
  | Before  |256\*320\*19| 348\*384\*256  |612\*768\*19|320\*320\*28| 
  | After   |348\*384\*256|348\*384\*256 |348\*384\*256 |348\*384\*256|   

```bash
# Bash
modal=("flair" "t1" "t2")
num=("0032")
for i in ${num[@]}
do
  workdir1=./Raw_data/SYSU${i}
  workdir2=./CoReg/SYSU${i}
  mkdir -p ${workdir2}
  for j in ${modal[@]}
  do
    flirt -in ${workdir1}/SYSU${i}_${j}.nii -ref ${workdir1}/SYSU${i}_t1ce.nii -out ${workdir2}/SYSU${i}_${j}.nii.gz -omat ${workdir2}/SYSU${i}_${j}.mat -bins 256 -cost mutualinfo -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 6  -interp trilinear
  done
  cp -r ${workdir1}/SYSU${i}_t1ce.nii.gz ${workdir2}/SYSU${i}_t1ce.nii.gz
done
```

### Normalization to 1mm
We define the 3D resizing function as follow.

```python
# python 
import os
from scipy import ndimage as nd
import SimpleITK as sitk

def ThreeD_resize(imgs,Normlize_VS,img_vs): 
   #order The order of the spline interpolation, default is 3. The order has to be in the range 0-5. 
   zf0=img_vs[0]/Normlize_VS[0] 
   zf1=img_vs[1]/Normlize_VS[1] 
   zf2=img_vs[2]/Normlize_VS[2] 
   new_imgs = nd.zoom(imgs, [zf0, zf1, zf2], order=0) 
   return new_imgs

Normlize_VS=[1,1,1]
num=["0032"]
modal=["t1", "t1ce", "t2", "flair"]
for i in range(len(num)):
    dir_Nor = './CoReg_Nor/' + 'SYSU' + num[i]
    if not os.path.exists(dir_Nor):
        os.makedirs(dir_Nor)
    for j in range(len(modal)):
        dir_img = './CoReg/' + 'SYSU' + num[i] + '/SYSU' + num[i]+'_' + modal[j] + '.nii.gz'
        save_path = './CoReg_Nor/' + 'SYSU' + num[i] + '/SYSU' + num[i]+'_' + modal[j] + '.nii.gz'
        data_img = sitk.ReadImage(dir_img)
        array_img = sitk.GetArrayFromImage(data_img)
        Spacing_img = data_img.GetSpacing()[::-1]
        Img_array = ThreeD_resize(array_img, Normlize_VS, Spacing_img)
        Img_ni = sitk.GetImageFromArray(Img_array)
        Img_ni.SetDirection(data_img.GetDirection())
        sitk.WriteImage(Img_ni,save_path)
```

### Skull stripping

```bash
# Bash 
modal=("flair")
num=("0032")
for i in ${num[@]}
do
  workdir1=/home/huilin/Zhong/temp/CoReg_Nor/SYSU${i}
  workdir2=/home/huilin/Zhong/temp/CoReg_Nor_Bet/SYSU${i}
  mkdir -p ${workdir2}
  for j in ${modal[@]}
  do
    bet ${workdir1}/SYSU${i}_${j}.nii.gz ${workdir2}/SYSU${i}_${j}.nii.gz -m
  done
done
```

Then we use the skull mask of FLAIR MR images to all four modal 

```python
# python 
import os
import numpy as np
import SimpleITK as sitk

num=["0032"]
modal=["t1", "t1ce", "t2", "flair"]
for i in range(len(num)):
    dir_Nor = './BraTS_Format/' + 'SYSU' + num[i]
    if not os.path.exists(dir_Nor):
        os.makedirs(dir_Nor)
    for j in range(len(modal)):
        mask_path = './CoReg_Nor_Bet/' + 'SYSU' + num[i] + '/SYSU' + num[i] + '_flair_mask.nii.gz'
        dir_img = './CoReg_Nor/' + 'SYSU' + num[i] + '/SYSU' + num[i] + '_' + modal[j] + '.nii.gz'
        save_path = './BraTS_Format/' + 'SYSU' + num[i] + '/SYSU' + num[i] + '_' + modal[j] + '.nii.gz'
        data=sitk.ReadImage(mask_path)
        mask=sitk.GetArrayFromImage(data)
        I=sitk.GetArrayFromImage(sitk.ReadImage(dir_img))
        I=I*mask
        I_new=sitk.GetImageFromArray(I)
        I_new.CopyInformation(data)
        sitk.WriteImage(I_new,save_path)
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
  |         | local path | path inside the Docker image| 
  |---------|----|------|---|----|
  | Input path   |./BraTS_Format/SYSU0032/| /app/data/ |
  | Output path   |./Results|/app/results/ |

```bash
#bash
docker run -it --rm --gpus all -v ./BraTS_Format/SYSU0032/:/app/data/ -v ../Results:/app/results/ sustechmedical/brain_tumor_segmentation/ python runner.py
```
docker run -it --rm --gpus all -v /data1/zhangy/ResultsPath/SYSU0032/:/app/data/ -v /data1/zhangy/ResultsPath/Results/:/app/results/ sustechmedical/brain_tumor_segmentation python runner.py




# Reference

One example and the intermediate results for this example have been shared in Google Drive.

    https://drive.google.com/drive/folders/1HQb4CuMmGDqIA6DdFXo20JDNxi77z5UL?usp=sharing


For more information about this work, please read the following paper:

    Yue Zhang, Pinyuan Zhong, Dabin Jie, Jiewei Wu, Shanmei Zeng, Jianping Chu, Yilong Liu, Ed X. Wu and Xiaoying Tang. Brain Tumor Segmentation via Ensembling UNets with Different Inputs.

Please also cite our paper if you think our codes is helpful.


The implementation of UNet is based on the https://github.com/MIC-DKFZ/nnUNet. 
Many thanks for their great work. 

    Isensee, F., Jaeger, P. F., Kohl, S. A., Petersen, J., & Maier-Hein, K. H. (2020). nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation. Nature Methods, 1-9.