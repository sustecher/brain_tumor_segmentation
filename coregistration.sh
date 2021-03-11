modal=("flair" "t1" "t2")
id=$1

workdir1=./Raw_data/${id}
workdir2=./CoReg/${id}
mkdir -p ${workdir2}

for j in ${modal[@]}
do
  flirt -in ${workdir1}/${id}_${j}.nii -ref ${workdir1}/${id}_t1ce.nii -out ${workdir2}/${id}_${j}.nii.gz -omat ${workdir2}/${id}_${j}.mat -bins 256 -cost mutualinfo -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 6  -interp trilinear
done

cp -r ${workdir1}/${id}_t1ce.nii.gz ${workdir2}/${id}_t1ce.nii.gz