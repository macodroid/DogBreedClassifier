import os
import random
from typing import Tuple
import cv2
import numpy as np
import xml.etree.ElementTree as ET
import scipy.io
import shutil
import pandas as pd


def get_label_information(anotation_file_path: str) -> tuple:
    name = None
    width, height = None, None
    x_start, y_start, x_end, y_end = None, None, None, None
    tree = ET.parse(f"Annotation/{anotation_file_path}")
    root = tree.getroot()
    for x in root.findall("size"):
        width = int(x.find("width").text)
        height = int(x.find("height").text)

    for x in root.findall("object"):
        name = x.find("name").text
        for y in x.findall("bndbox"):
            x_start = int(y.find("xmin").text)
            y_start = int(y.find("ymin").text)
            x_end = int(y.find("xmax").text)
            y_end = int(y.find("ymax").text)
    return (width, height), (x_start, y_start), (x_end, y_end), name


def get_labels_category_indexes(file_name: str) -> dict:
    dataset_list = []
    file_mat_content = scipy.io.loadmat(file_name)
    for i in file_mat_content["file_list"]:
        dataset_list.append(i[0][0])
    df = pd.DataFrame(dataset_list)
    df = df[0].str.split("-", n=1, expand=True)
    df = df[1].str.split("/", n=1, expand=True)
    categories = df[0]
    unique_cat = categories.unique()
    labels = {}
    for i, cat in enumerate(unique_cat):
        labels[cat] = i
    return labels


def create_dataset_directory_structure():
    root_dir = "YOLOv6/data/custom_dataset"
    sub_dirs = ["train", "val", "test"]
    try:
        os.mkdir(root_dir)
        os.mkdir(f"{root_dir}/images")
        for d in sub_dirs:
            os.mkdir(f"{root_dir}/images/{d}")
        os.mkdir(f"{root_dir}/labels")
        for d in sub_dirs:
            os.mkdir(f"{root_dir}/labels/{d}")
    except:
        shutil.rmtree(root_dir)
        create_dataset_directory_structure()


# class_id center_x center_y bbox_width bbox_height -> yolo format
# width_height = (width, height)
# xy_start = (x_start, y_start)
# width_height = (x_end, y_end)
def convert_annotaion_info_to_yolo_format(annotation_file: str):
    (
        (image_width, image_height),
        (x_start, y_start),
        (x_end, y_end),
        label_name,
    ) = get_label_information(annotation_file)
    x_center = ((x_start + x_end) / 2) / image_width
    y_center = ((y_start + y_end) / 2) / image_height
    bbox_width = (x_end - x_start) / image_width
    bbox_height = (y_end - y_start) / image_height
    return x_center, y_center, bbox_width, bbox_height, label_name


def create_annotation_file(
    center_x, center_y, bb_width, bb_height, label_index, split_type, file_name
):
    with open(f"custom_dataset/labels/{split_type}/{file_name}.txt", mode="w") as f:
        f.write(f"{label_index} {center_x} {center_y} {bb_width} {bb_height}")


if __name__ == "__main__":
    tmp_file_name = None
    items = ["train_list.mat", "test_list.mat"]
    create_dataset_directory_structure()
    labels: dict = get_labels_category_indexes("train_list.mat")
    for i in items:
        split_type = i.split("_")[0]
        file_mat_content = scipy.io.loadmat(i)
        for j, image_name in enumerate(file_mat_content["file_list"]):
            image = image_name[0][0]
            # want to get rid of .jpg at the end
            annotation_file_name = image_name[0][0][:-4]
            breed_folder, file_name = annotation_file_name.split("/")
            if split_type == "train" and tmp_file_name != breed_folder:
                tmp_file_name = breed_folder
                validation_indexes = np.random.choice(
                    range(j, j + 100 - 1), 20, replace=False
                )
            (
                center_x,
                center_y,
                bb_width,
                bb_height,
                label_name,
            ) = convert_annotaion_info_to_yolo_format(
                annotation_file=annotation_file_name,
            )
            if split_type == "train" and j in validation_indexes:
                create_annotation_file(
                    center_x,
                    center_y,
                    bb_width,
                    bb_height,
                    labels[label_name],
                    "val",
                    file_name,
                )
                shutil.copy(
                    f"Images/{image}", f"custom_dataset/images/val/{file_name}.jpg"
                )
            else:
                create_annotation_file(
                    center_x,
                    center_y,
                    bb_width,
                    bb_height,
                    labels[label_name],
                    split_type,
                    file_name,
                )
                shutil.copy(
                    f"Images/{image}",
                    f"custom_dataset/images/{split_type}/{file_name}.jpg",
                )
