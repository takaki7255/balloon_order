import math
import os
import cv2
from modules import *
import math

def get_distance(x1, y1, x2, y2):
    """2点間の距離を計算する"""
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def find_nearest_balloon(panel, bounded_text):
    """コマの右上座標に最も近い吹き出しを見つける"""
    if not bounded_text:
        return None
    
    panel_xmax, panel_ymin = int(panel['xmax']), int(panel['ymin'])
    min_dist = float('inf')
    nearest_balloon = None
    
    for balloon in bounded_text:
        try:
            balloon_x = (int(balloon['xmin']) + int(balloon['xmax'])) / 2
            balloon_y = (int(balloon['ymin']) + int(balloon['ymax'])) / 2
            dist = get_distance(panel_xmax, panel_ymin, balloon_x, balloon_y)
            print("dist", dist)
            if dist < min_dist:
                min_dist = dist
                nearest_balloon = balloon
        except (ValueError, TypeError):
            continue
    
    return nearest_balloon


def order_balloons(panel, bounded_text):
    panel_xmin, panel_ymin = int(panel['xmin']), int(panel['ymin'])
    start = find_nearest_balloon(panel, bounded_text)
    
    if start is None:
        # bounded_textが空の場合など、適切に処理する
        return []

    start_xmin, start_ymin = int(start['xmin']), int(start['ymin'])
    start_xmax, start_ymax = int(start['xmax']), int(start['ymax'])
    start_x, start_y = (start_xmin + start_xmax) / 2, (start_ymin + start_ymax) / 2
    ordered_balloons = [start]
    unordered_balloons = [b for b in bounded_text if b != start]
    
    while unordered_balloons:
        min_dist = float('inf')
        nearest_balloon = None
        
        for balloon in unordered_balloons:
            balloon_xmin, balloon_ymin = int(balloon['xmin']), int(balloon['ymin'])
            balloon_xmax, balloon_ymax = int(balloon['xmax']), int(balloon['ymax'])
            balloon_x, balloon_y = (balloon_xmin + balloon_xmax) / 2, (balloon_ymin + balloon_ymax) / 2
            dist = get_distance(start_x, start_y, balloon_x, balloon_y) + get_distance(balloon_x, balloon_y, panel_xmin, panel_ymin)
            if dist < min_dist:
                min_dist = dist
                nearest_balloon = balloon
        
        ordered_balloons.append(nearest_balloon)
        unordered_balloons.remove(nearest_balloon)
        start_xmin, start_ymin = int(nearest_balloon['xmin']), int(nearest_balloon['ymin'])
        start_xmax, start_ymax = int(nearest_balloon['xmax']), int(nearest_balloon['ymax'])
        start_x, start_y = (start_xmin + start_xmax) / 2, (start_ymin + start_ymax) / 2
    
    return ordered_balloons




if __name__ == '__main__':
    # パスの設定
    manga109_ano_dir = "./../Manga109_released_2021_12_30/annotations.v2020.12.18/"  # アノテーションファイルのディレクトリ
    manga109_img_dir = "./../Manga109_released_2021_12_30/images/"  # 画像ファイルのディレクトリ
    files = os.listdir(manga109_ano_dir)  # アノテーションファイルのリスト
    img_folders = os.listdir(manga109_img_dir)  # 画像フォルダのリスト

    # マンガのタイトルを指定
    manga_title = "Belmondo"
    ano_file_path = manga109_ano_dir + manga_title + ".xml"
    img_folder_path = manga109_img_dir + manga_title + "/"

    # 画像ファイル名を取得
    imgs = os.listdir(img_folder_path)
    imgs.sort()

    panels = get_panelbbox_info_from_xml(ano_file_path)
    balloons = get_textbbox_info_from_xml(ano_file_path)

    for page_index in balloons.keys():
        img_path = index_to_img_path(page_index, img_folder_path)
        print("img_path", img_path)
        for panel in panels[page_index]:
            print("panel", panel)
            bounded_text = get_bounded_text(panel, balloons[page_index])
            print("bounded_text", bounded_text)
            img = cv2.imread(img_path)
            draw_img = draw_bbox(img, [panel], (0, 255, 0))
            # draw_img = draw_bbox(draw_img, bounded_text, (0, 0, 255))
            cv2.imshow("img", draw_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            ordered_balloons = order_balloons(panel, bounded_text)
            drawimg = draw_bbox(img, [panel], "output.jpg")
            for balloon in ordered_balloons:
                drawimg = draw_bbox(drawimg, [balloon], "output.jpg")
                cv2.imshow("img", drawimg)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            print("ordered_balloons", ordered_balloons)