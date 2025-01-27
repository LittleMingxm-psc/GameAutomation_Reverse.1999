import time
import pyautogui
import numpy as np
import easyocr
import random
import win32gui
import os
from PIL import Image,ImageDraw,ImageFont

from pywinauto.findwindows import find_window
from datetime import datetime

def match_template(image, model, confidence_threshold=0.6 ,output_dir="test"):
    """
    识别目标并绘制边界框，同时保存未经标注的原始图片。

    参数:
        image (numpy.ndarray | PIL.Image.Image): 输入图像，可以是 numpy 格式或 PIL.Image 格式。
        model: 目标检测模型，需支持返回 `results.boxes`。
        confidence_threshold (float): 置信度阈值。
        output_dir (str): 输出文件夹路径。

    返回:
        detections (list): 检测到的目标信息列表。
    """
    results = model.predict(image, conf=0.6)

    # 确保图像是 PIL.Image 格式
    if isinstance(image, np.ndarray):
        original_image = Image.fromarray(image)  # 保存原始图像
    else:
        original_image = image.copy()  # 保存原始图像

    image = original_image.copy()  # 用于绘制标注的图像

    # 如果结果是列表，取第一个
    if isinstance(results, list):
        results = results[0]

    detections = []

    if hasattr(results, "boxes"):
        boxes = results.boxes
        for box in boxes:
            cls_id = int(box.cls)  # 类别 ID
            confidence = box.conf  # 置信度
            coords = box.xyxy.tolist()[0]  # 边界框坐标
            x1, y1, x2, y2 = map(int, coords)

            # 如果置信度满足阈值要求，记录检测结果
            if confidence >= confidence_threshold:
                detections.append({
                    "class_id": cls_id,
                    "confidence": confidence,
                    "box": (x1, y1, x2, y2)
                })

        # 绘制所有检测框
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.load_default()
        except IOError:
            font = None

        for detection in detections:
            x1, y1, x2, y2 = detection["box"]
            cls_id = detection["class_id"]

            # 绘制边界框
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

            # 绘制类别 ID
            text = f"ID: {cls_id}"
            if font:
                text_bbox = font.getbbox(text)  # 使用 getbbox 获取文本边界框
                text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])  # 宽度和高度
            else:
                text_bbox = draw.textbbox((0, 0), text)  # 如果没有字体，用 draw.textbbox
                text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])

                # 确定文本位置
                text_position = (x1, y1 - text_size[1] if y1 > text_size[1] else y1 + 2)
                draw.text(text_position, text, fill="red", font=font)
    else:
        print("未检测到有效的边界框")

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 保存原始图片到 original 文件夹
    original_dir = os.path.join(output_dir, "original")
    os.makedirs(original_dir, exist_ok=True)
    original_path = os.path.join(original_dir, f"original_image_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jpg")
    original_image.save(original_path)

    # 保存标注后的图片
    annotated_path = os.path.join(output_dir, f"annotated_image_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jpg")
    image.save(annotated_path)

    return detections


def find_window(window_title):
    def enum_window_callback(hwnd, results):
        title = win32gui.GetWindowText(hwnd).lower()
        if window_title.lower() in title:
            rect = win32gui.GetWindowRect(hwnd)  # 获取窗口的矩形边界
            results.append(rect)

    windows = []
    win32gui.EnumWindows(enum_window_callback, windows)  # 枚举所有窗口

    if windows:
        left, top, right, bottom = windows[0]
        print(f"找到模拟器窗口位置：{window_title}")
        print(f"模拟器窗口位于:{left,top,right,bottom}")
        return left, top, right, bottom

    print(f"未找到模拟器窗口: {window_title}")
    return False


def open_game(window_region,model):
    if not window_region:
        print("无法找到模拟器窗口")
        return False

    screenshot = pyautogui.screenshot(region = window_region)
    detections = match_template(screenshot,model)

    for detection in detections:
        if detection["class_id"] == 0:
            print(f"已经找到游戏图标")
            location = detection["box"]
            click(window_region,location)
            time.sleep(40)
        else:
            print(f"未找到游戏图标")
            return False

    screenshot = pyautogui.screenshot(region=window_region)
    detections = match_template(screenshot,model)

    for detection in detections:
        if detection["class_id"] == 1:
            print(f"已经找到游戏logo")
            location = detection["box"]
            click(window_region,location)
        else:
            print(f"未找到游戏开始界面Logo")
            return False



def extract_resource_amount(position):
    x1 , y1 ,x2 ,y2 = position
    offset_x = 25
    offset_y = 0
    width = 60
    height = 20
    region = (x1 + offset_x, y1 + offset_y,width,height)
    screenshot = pyautogui.screenshot(region)
    screenshot_np = np.array(screenshot)

    reader = easyocr.Reader(['en'])
    result = reader.readtext(screenshot_np)

    for bbox,text,confidence in result:
        print(f"识别到的文本:{text},置信度:{confidence}")
    return [text for _,text, _ in result]

def click(window_region,location):
    window_x, window_y, _, _ = window_region
    x1, y1, x2, y2 = location
    position = [x1 + window_x, y1 + window_y, x2 + window_x, y2 + window_y]
    center_x = (position[0] + position[2]) // 2
    center_y = (position[1] + position[3]) // 2

    for _ in range(1):
        time.sleep(random.uniform(0.1,0.2))
        pyautogui.click(center_x, center_y)
        time.sleep(random.uniform(0.1,0.2))

def screenshot(window_title):
    window_region = find_window(window_title)
    if not window_region:
        print(f"无法找到窗口: {window_title}")
        return

    output_folder = os.path.join(os.getcwd(), "screen")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"已创建文件夹: {output_folder}")

    try:
        while True:
            window_region = find_window(window_title)
            window_height = window_region[3] - window_region[1]
            window_width = window_region[2] - window_region[0]

            # 截图指定区域
            screenshot = pyautogui.screenshot(region=(
                window_region[0],  # 左上角 X 坐标
                window_region[1],  # 左上角 Y 坐标
                window_width,  # 截图宽度
                window_height  # 截图高度
            ))

            # 保存截图到 'screen' 文件夹
            timestamp = int(time.time())  # 当前时间戳
            filename = os.path.join(output_folder, f"screenshot_{timestamp}.png")
            screenshot.save(filename)
            print(f"截图已保存: {filename}")

            # 等待 2 秒
            time.sleep(2)

    except KeyboardInterrupt:
        print("程序已停止")
