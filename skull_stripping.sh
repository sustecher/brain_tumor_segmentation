modal=("flair")
id=$1

workdir1=./CoReg_Nor/${id}
workdir2=./CoReg_Nor_Bet/${id}
mkdir -p ${workdir2}

for j in ${modal[@]}
do
  bet ${workdir1}/${id}_${j}.nii.gz ${workdir2}/${id}_${j}.nii.gz -m
done