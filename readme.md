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
# Bash
modal=("flair" "t1" "t2")
num=("0032")

date
hostname
for i in ${num[@]}
workdir1=./Raw_data/SYSU${i}/
workdir2=./CoReg/SYSU${i}/

do
  for j in ${modal[@]}
  do
flirt -in ${workdir1}/SYSU${i}_${j}.nii -ref ${workdir1}/SYSU${i}_t1ce.nii -out ${workdir2}/SYSU${i}_${j}.nii.gz -omat ${workdir2}/SYSU${i}_${j}.mat -bins 256 -cost mutualinfo -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 6  -interp trilinear
done
done
date
```

### Normalization to 1mm
We define the 3D resizing function as follow.

```bash
# python 
from scipy import ndimage as nd
Normlize_VS=[1,1,1]
def ThreeD_resize(imgs,Normlize_VS,img_vs): 
   #order The order of the spline interpolation, default is 3. The order has to be in the range 0-5. 
   zf0=img_vs[0]/Normlize_VS[0] 
   zf1=img_vs[1]/Normlize_VS[1] 
   zf2=img_vs[2]/Normlize_VS[2] 
   new_imgs = nd.zoom(imgs, [zf0, zf1, zf2], order=0) 
   return new_imgs

num=["0032"]
modal=["t1", "t1ce", "t2", "flair", "t1ce_ET"]
data_path = '/'
for i in range(len(num)):
    for j in range(len(modal)):
        dir_img = './CoReg/' + 'SYSU' + num[i] + '/SYSU' + num[i]+'_' + modal[j] + '.nii.gz'
        save_path ='./Normalization/' + 'SYSU' + num[i] + '/SYSU' + num[i]+'_' + modal[j] + '.nii.gz'
        data_img = sitk.ReadImage(dir_img)
        array_img = sitk.GetArrayFromImage(data_img)
        Spacing_img = data_img.GetSpacing()[::-1]
        print(Spacing_img)
        Img_array = ThreeD_resize(array_img, Normlize_VS, Spacing_img)
        Img_ni = sitk.GetImageFromArray(Img_array) 
        Img_ni.SetDirection(data_img.GetDirection()) 
        sitk.WriteImage(Img_ni,save_path) 
```

### Skull stripping

```bash
# Bash 
modal=("flair" "t1" "t2" "t1ce")
num=("0032")
date
hostname
for i in ${num[@]}
workdir1=./Raw_data/SYSU${i}/
workdir3=./CoReg/SYSU${i}/
do
  for j in ${modal[@]}
  do
bet ${workdir1}/SYSU${i}_${j}.nii.gz ${workdir3}/SYSU${i}_${j}.nii.gz -m
done
done
date
```

Then we use the skull mask of FLAIR MR images to all four modal 

```bash
# python 
from scipy import ndimage as nd
Normlize_VS=[1,1,1]
def ThreeD_resize(imgs,Normlize_VS,img_vs): 
   #order The order of the spline interpolation, default is 3. The order has to be in the range 0-5. 
   zf0=img_vs[0]/Normlize_VS[0] 
   zf1=img_vs[1]/Normlize_VS[1] 
   zf2=img_vs[2]/Normlize_VS[2] 
   new_imgs = nd.zoom(imgs, [zf0, zf1, zf2], order=0) 
   return new_imgs

num=["0032"]
modal=["t1", "t1ce", "t2", "flair"]
data_path = '/'
for i in range(len(num)):
    for j in range(len(modal)):
        dir_img = './CoReg/' + 'SYSU' + num[i] + '/SYSU' + num[i]+'_' + modal[j] + '.nii.gz'
        save_path ='./Normalization/' + 'SYSU' + num[i] + '/SYSU' + num[i]+'_' + modal[j] + '.nii.gz'
        mask_path = data_path + 'resize_bet/' + 'SYSU' + num[i] + '_flair_reb_mask.nii.gz'
        dir_img1 = data_path + 'resize/' + 'SYSU' + num[i] + '_' + modal[j] + '_re.nii.gz'
        save_path1 = data_path + 'resize_bet_mask/' + 'SYSU' + num[i] + '_' + nnU[j] + '.nii.gz'
        data=sitk.ReadImage(mask_path)
        mask=sitk.GetArrayFromImage(data)
        print(np.shape(mask))

        T=sitk.GetArrayFromImage(sitk.ReadImage(dir_img1))
        T=T*mask
        T_new=sitk.GetImageFromArray(T)
        T_new.CopyInformation(data)
        sitk.WriteImage(T_new,save_path1)
```


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