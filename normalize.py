# -*- coding:utf-8 -*-
import os
import argparse
from scipy import ndimage as nd
import SimpleITK as sitk


def ThreeD_resize(imgs, Normlize_VS, img_vs): 
   #order The order of the spline interpolation, default is 3. The order has to be in the range 0-5. 
   zf0 = img_vs[0] / Normlize_VS[0] 
   zf1 = img_vs[1] / Normlize_VS[1] 
   zf2 = img_vs[2] / Normlize_VS[2] 
   new_imgs = nd.zoom(imgs, [zf0, zf1, zf2], order=0) 
   return new_imgs


parser = argparse.ArgumentParser()
parser.add_argument("--id", type=str, help="")
args = parser.parse_args()

Normlize_VS = [1, 1, 1]
id_ = args.id
modal = ["t1", "t1ce", "t2", "flair"]

dir_Nor = './CoReg_Nor/' + id_
if not os.path.exists(dir_Nor):
    os.makedirs(dir_Nor)

for j in range(len(modal)):
    dir_img = './CoReg/' + id_ + '/' + id_ +'_' + modal[j] + '.nii.gz'
    save_path = './CoReg_Nor/' + id_ + '/' + id_ +'_' + modal[j] + '.nii.gz'
    data_img = sitk.ReadImage(dir_img)
    array_img = sitk.GetArrayFromImage(data_img)
    Spacing_img = data_img.GetSpacing()[::-1]
    Img_array = ThreeD_resize(array_img, Normlize_VS, Spacing_img)
    Img_ni = sitk.GetImageFromArray(Img_array)
    Img_ni.SetDirection(data_img.GetDirection())
    sitk.WriteImage(Img_ni,save_path)