# Data_augmentation

Scripts for data augmentation. Data augmentation should be performed after preprocessing (generate jpg files and re-organize file systems) and before VOC dataset building.

## Rotation and horizontal flip

Nematodes image can be rotated or horizontal flipped. This creates 4x data samples of original data.

Usage:

```bash
python rotate_flip.py --img_folder new_img --label_folder new_lbl --aug_img_folder aug_img --aug_label_folder aug_lbl --quality 95
```

`--quality` is the output JPG quality.

## Illumination augmentation

Nematodes will still be nematodes if illumination changes. For each image, we adjust the Gamma of the image to 0.5, 1 and 2.0

Usage:

```bash
python illumination.py --img_folder new_img --label_folder new_lbl --aug_img_folder aug_img --aug_label_folder aug_lbl --quality 95
```

`--quality` is the output JPG quality.
