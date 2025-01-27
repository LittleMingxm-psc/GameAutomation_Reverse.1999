from itertools import count

import pyautogui
import ncnn
from mouseinfo import position

import Utils
import pathlib
import time
from ultralytics import YOLO

from GameScreenDesign import GameScreen
from Initialization import data
from Utils import click, screenshot

current_dir = pathlib.Path(__file__).parent
model = YOLO(current_dir / "YOLOresult" / "best.pt")
model_2 = YOLO(current_dir / "YOLOresult" / "best_2.pt")
#open = YOLO(current_dir / "YOLOresult" / "open.pt")\

param_path = str(current_dir / "YOLOresult" / "best.ncnn.param")
bin_path = str(current_dir / "YOLOresult" / "best.ncnn.bin")

net = ncnn.Net()
net.load_param(param_path)  # 确保路径是字符串
net.load_model(bin_path)    # 确保路径是字符串


def main():
    window_title = "雷电模拟器"
    window_region = Utils.find_window(window_title)
    window_height = window_region[3]-window_region[1]
    window_width = window_region[2]-window_region[0]
    #Utils.open_game(window_region,model)

    #screenshot(window_title)

    GameScreen.data = data
    main_screen = GameScreen("main_screen")
    battle_type = GameScreen("battle_type")
    battle_choose_resource = GameScreen("battle_choose_resource")
    character_select = GameScreen("character_select")
    LP1LP2 = GameScreen("LP1LP2")
    MA1M2A = GameScreen("MA1M2A")
    HP1H2P = GameScreen("HP1H2P")
    NO1CCO = GameScreen("NO1CCO")
    victory = GameScreen("victory")
    wilder = GameScreen("wilder")
    count = GameScreen("count")
    mission = GameScreen("mission")
    gift = GameScreen("gift")

    main_screen.update_state(window_title,model)
    click(window_region,main_screen.buttons["battle"]["position"])
    time.sleep(1)

    battle_type.update_state(window_title,model)
    click(window_region,battle_type.buttons["resource_1"]["position"])
    time.sleep(1)

    battle_choose_resource.update_state(window_title, model)
    if battle_choose_resource.buttons["NO1CCO"]["position"] == [0, 0, 0, 0]:
        print(f"1")
        pyautogui.moveTo(battle_type.buttons["out_of_the_box"]["position"][0],battle_type.buttons["out_of_the_box"]["position"][1]-window_height/4,duration=0.5)
        pyautogui.drag(xOffset=-window_width/1.5, yOffset=0, duration=1, button='right')

    battle_choose_resource.update_state(window_title, model)
    click(window_region,battle_choose_resource.buttons["NO1CCO"]["position"])
    time.sleep(1)

    NO1CCO.update_state(window_title, model)
    click(window_region,NO1CCO.buttons["NO1CCO_7"]["position"])
    time.sleep(1)
    NO1CCO.update_state(window_title, model)
    click(window_region,NO1CCO.buttons["start"]["position"])
    time.sleep(4)

    character_select.update_state(window_title, model)
    if not character_select.buttons["auto_1"]["position"] == [0, 0, 0, 0]:
        click(window_region,character_select.buttons["auto_1"]["position"])
        character_select.update_state(window_title, model)

    click(window_region,character_select.buttons["time_choose"]["position"])

    character_select.update_state(window_title, model)
    click(window_region,character_select.buttons["time_1"]["position"])
    time.sleep(1)
    click(window_region,character_select.buttons["recurrence"]["position"])

    success = False  # 标志变量，记录是否成功完成任务

    for i in range(20):
        time.sleep(5)  # 等待 5 秒
        victory.update_state(window_title, model)  # 更新状态

        # 检查是否检测到胜利按钮
        if not victory.buttons["victory"]["position"] == [0, 0, 0, 0]:
            click(window_region, victory.buttons["victory"]["position"])  # 点击按钮
            success = True  # 成功完成任务
            break  # 提前退出循环

        # 未检测到胜利按钮，打印等待时间
        print(f"战斗仍未结束，已经等待{(i + 1) * 5}秒")

    # 循环结束后检查是否成功
    if not success:
        print("已经等待120秒，等待时间超过时长")
        return False

    print(f"1")
    time.sleep(3)

    click(window_region,character_select.buttons["back_to_the_main"]["position"])
    print(f"自动作战已经结束")
    time.sleep(5)


    main_screen.update_state(window_title, model)
    click(window_region,main_screen.buttons["wilder"]["position"])
    time.sleep(15)

    wilder.update_state(window_title, model_2)
    if not wilder.buttons["trust"]["position"] == [0, 0, 0, 0]:
        click(window_region,wilder.buttons["trust"]["position"])
        time.sleep(3)

    if not wilder.buttons["money_1"]["position"] == [0, 0, 0, 0]:
        click(window_region,wilder.buttons["money_1"]["position"])
        time.sleep(2)
        wilder.update_state(window_title, model_2)
        click(window_region,wilder.buttons["money_2"]["position"])
        time.sleep(1)
        click(window_region,wilder.buttons["money_1"]["position"])
        time.sleep(1)
        wilder.update_state(window_title, model_2)
        click(window_region,wilder.buttons["money_3"]["position"])
        time.sleep(1)

    click(window_region,wilder.buttons["back_to_the_main"]["position"])
    time.sleep(5)

    main_screen.update_state(window_title, model)
    #pyautogui.click(((main_screen.buttons["battle"]["position"][0] + main_screen.buttons["mission"]["position"][0]) / 2,(main_screen.buttons["battle"]["position"][1] + main_screen.buttons["mission"]["position"][1]) / 2))
    time.sleep(1)
    click(window_region,main_screen.buttons["mission"]["position"])
    time.sleep(1)

    mission.update_state(window_title, model_2)
    if mission.buttons["finish"]["position"] == [0, 0, 0, 0]:
        click(window_region,mission.buttons["daily"]["position"])
        time.sleep(1)
        click(window_region,mission.buttons["claim_2"]["position"])
        time.sleep(3)
        click(window_region,mission.buttons["claim_2"]["position"])
        time.sleep(1)
        click(window_region,mission.buttons["weekly"]["position"])
        time.sleep(1)
        click(window_region,mission.buttons["claim_2"]["position"])
        time.sleep(1)
        click(window_region,mission.buttons["claim_2"]["position"])
        time.sleep(3)

    click(window_region,mission.buttons["back_to_the_main"]["position"])
    time.sleep(3)

    main_screen.update_state(window_title, model)
    click(window_region,main_screen.buttons["gift"]["position"])
    time.sleep(1)

    gift.update_state(window_title, model_2)
    click(window_region,gift.buttons["mission"]["position"])
    time.sleep(1)
    click(window_region,gift.buttons["claim_1"]["position"])
    time.sleep(3)
    click(window_region,gift.buttons["mission"]["position"])
    time.sleep(1)
    click(window_region,gift.buttons["prize"]["position"])
    time.sleep(1)
    click(window_region,gift.buttons["claim_1"]["position"])
    time.sleep(3)
    click(window_region,gift.buttons["prize"]["position"])
    time.sleep(1)
    click(window_region,gift.buttons["back_to_the_main"]["position"])
    time.sleep(1)

    print(f"自动每日完成")









if __name__ == "__main__":
    main()
