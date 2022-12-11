## Standford Dataset dogs
Link to dataset http://vision.stanford.edu/aditya86/ImageNetDogs/
Steps:
- Download [List](http://vision.stanford.edu/aditya86/ImageNetDogs/lists.tar). This is list for training and testing list.
- Download [Training Feature](http://vision.stanford.edu/aditya86/ImageNetDogs/train_data.mat) && [Test Feature](http://vision.stanford.edu/aditya86/ImageNetDogs/test_data.mat)  


Every download file need to be extracted in root directory of this project.

Then run
```bash
python main.py
```
This will create YoloV6 dataset strucuture.

```
custom_dataset
├── images
│   ├── train
│   │   ├── train0.jpg
│   │   └── train1.jpg
│   ├── val
│   │   ├── val0.jpg
│   │   └── val1.jpg
│   └── test
│       ├── test0.jpg
│       └── test1.jpg
└── labels
    ├── train
    │   ├── train0.txt
    │   └── train1.txt
    ├── val
    │   ├── val0.txt
    │   └── val1.txt
    └── test
        ├── test0.txt
        └── test1.txt
```
All anotation will be converted to YoloV6 format and they will be normalized.
YoloV6 Format:
```json
# class_id center_x center_y bbox_width bbox_height
0 0.300926 0.617063 0.601852 0.765873
# this second annotation is here is there are for example two dogs in one picture. (But this is not case in this dataset)
1 0.575 0.319531 0.4 0.551562
```
## Reference to dataset
Primary:  
Aditya Khosla, Nityananda Jayadevaprakash, Bangpeng Yao and Li Fei-Fei. Novel dataset for Fine-Grained Image Categorization. First 
Workshop on Fine-Grained Visual Categorization (FGVC), IEEE       Conference on Computer Vision and Pattern Recognition (CVPR), 2011.

Secondary:  
  J. Deng, W. Dong, R. Socher, L.-J. Li, K. Li and L. Fei-Fei, ImageNet: A Large-Scale Hierarchical Image Database. IEEE Computer Vision and Pattern Recognition (CVPR), 2009.
