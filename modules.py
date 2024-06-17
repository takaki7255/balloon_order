import cv2
import os
import numpy as np
import xml.etree.ElementTree as ET


# アノテーションファイルからページごとにオブジェクトのバウンディングボックス情報を取得
def get_baundingbox_info_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    pages = root.findall(".//page")
    page_objects = {}
    for page in pages:
        page_index = page.get("index")
        # to int
        page_index = int(page_index)
        objects = []

        for obj in page:
            if obj.tag in ["frame", "text", "body", "face"]:
                obj_data = {
                    "type": obj.tag,
                    "id": obj.get("id"),
                    "xmin": obj.get("xmin"),
                    "ymin": obj.get("ymin"),
                    "xmax": obj.get("xmax"),
                    "ymax": obj.get("ymax"),
                }
                objects.append(obj_data)

        page_objects[page_index] = objects

    return page_objects

# アノテーションファイルからページごとにパネルのバウンディングボックス情報を取得
def get_panelbbox_info_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    pages = root.findall(".//page")
    page_objects = {}
    for page in pages:
        page_index = page.get("index")
        # to int
        page_index = int(page_index)
        objects = []

        for obj in page:
            if obj.tag in ["frame"]:
                obj_data = {
                    "type": obj.tag,
                    "id": obj.get("id"),
                    "xmin": obj.get("xmin"),
                    "ymin": obj.get("ymin"),
                    "xmax": obj.get("xmax"),
                    "ymax": obj.get("ymax"),
                }
                objects.append(obj_data)

        page_objects[page_index] = objects

    return page_objects


# アノテーションファイルからページごとにテキストのバウンディングボックスのみ情報を取得
def get_textbbox_info_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    pages = root.findall(".//page")
    page_objects = {}
    for page in pages:
        page_index = page.get("index")
        # to int
        page_index = int(page_index)
        objects = []

        for obj in page:
            if obj.tag in ["text"]:
                obj_data = {
                    "type": obj.tag,
                    "id": obj.get("id"),
                    "xmin": obj.get("xmin"),
                    "ymin": obj.get("ymin"),
                    "xmax": obj.get("xmax"),
                    "ymax": obj.get("ymax"),
                }
                objects.append(obj_data)

        page_objects[page_index] = objects

    return page_objects

def get_text_and_frame_bbox_info_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    pages = root.findall(".//page")
    page_objects = {}
    for page in pages:
        page_index = page.get("index")
        # to int
        page_index = int(page_index)
        objects = []

        for obj in page:
            if obj.tag in ["text", "frame"]:
                obj_data = {
                    "type": obj.tag,
                    "id": obj.get("id"),
                    "xmin": obj.get("xmin"),
                    "ymin": obj.get("ymin"),
                    "xmax": obj.get("xmax"),
                    "ymax": obj.get("ymax"),
                }
                objects.append(obj_data)

        page_objects[page_index] = objects

    return page_objects

def get_bounded_text(panel_info, text_info):
    panel_xmin = int(panel_info["xmin"])
    panel_ymin = int(panel_info["ymin"])
    panel_xmax = int(panel_info["xmax"])
    panel_ymax = int(panel_info["ymax"])

    # 範囲内のテキストのバウンディングボックスを取得
    bounded_text = []
    for text in text_info:
        text_xmin = int(text["xmin"])
        text_ymin = int(text["ymin"])
        text_xmax = int(text["xmax"])
        text_ymax = int(text["ymax"])
        if panel_xmin <= text_xmin and text_xmax <= panel_xmax and panel_ymin <= text_ymin and text_ymax <= panel_ymax:
            bounded_text.append(text)
    return bounded_text


# 画像ファイル名をインデックスから取得
def index_to_img_path(index, img_folder_path):
    img_path = img_folder_path + str(index).zfill(3) + ".jpg"
    return img_path


# バウンディングボックスを画像に描画
def draw_bbox(img, page_objects, output_path):
    colors = {
        "frame": (0, 255, 0),  # 緑
        "body": (255, 0, 0),  # 青
        "face": (0, 0, 255),  # 赤
        "text": (255, 255, 0),  # シアン
    }
    for obj in page_objects:
        obj_type = obj["type"]
        xmin = int(obj["xmin"])
        ymin = int(obj["ymin"])
        xmax = int(obj["xmax"])
        ymax = int(obj["ymax"])
        color = colors[obj_type]
        # バウンディングボックスの中心座標を計算
        center = (int((xmin + xmax) / 2), int((ymin + ymax) / 2))
        # print(f"type:{obj_type}, xmin:{xmin}, ymin:{ymin}, xmax:{xmax}, ymax:{ymax}, center:{center}")
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, 2)
    return img
    cv2.imshow("img", img)
    # cv2.imwrite(output_path, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
