# -*- coding:utf-8 -*-
import os
import numpy as np
import argparse
import SimpleITK as sitk


parser = argparse.ArgumentParser()
parser.add_argument("--id", type=str, help="")
args = parser.parse_args()

id_ = args.id
modal=["t1", "t1ce", "t2", "flair"]
dir_Nor = './BraTS_Format/' + id_

if not os.path.exists(dir_Nor):
    os.makedirs(dir_Nor)

for j in range(len(modal)):
    mask_path = './CoReg_Nor_Bet/' + id_ + '/' + id_ + '_flair_mask.nii.gz'
    dir_img = './CoReg_Nor/' + id_ + '/' + id_ + '_' + modal[j] + '.nii.gz'
    save_path = './BraTS_Format/' + id_ + '/' + id_ + '_' + modal[j] + '.nii.gz'
    data = sitk.ReadImage(mask_path)
    mask = sitk.GetArrayFromImage(data)
    I = sitk.GetArrayFromImage(sitk.ReadImage(dir_img))
    I = I * mask
    I_new = sitk.GetImageFromArray(I)
    I_new.CopyInformation(data)
    sitk.WriteImage(I_new,save_path)