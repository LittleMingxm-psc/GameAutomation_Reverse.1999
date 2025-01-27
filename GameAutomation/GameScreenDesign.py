import numpy as np
import pyautogui
import Utils

class GameScreen:
    def __init__(self,name,resources=None,buttons=None):
        self.name = name
        self.buttons = buttons or {}
        self.resources = resources or {}
        self.children = {}

        self._initialize_screens()

    def _initialize_screens(self):
        if self.name in GameScreen.data:
            content = GameScreen.data[self.name]

            if "resources" in content:
                for resource_name, resource_data in content["resources"].items():
                    self.add_resource(
                        name=resource_name,
                        code=resource_data["code"],
                        amount=resource_data["amount"],
                        position=resource_data["position"]
                    )

            if "buttons" in content:
                for button_name, button_data in content["buttons"].items():
                    self.add_button(
                        name=button_name,
                        code=button_data["code"],
                        position=button_data["position"]
                    )

    def add_resource(self,name,code,amount,position):
        self.resources[name] = {"code": code, "amount": amount, "position": position}

    def add_button(self,name,code,position):
        self.buttons[name] = {"code": code, "position": position}

    def update_state(self, window_title, model):
        window_region = Utils.find_window(window_title)
        window_x, window_y, _, _ = window_region
        screenshot = pyautogui.screenshot(region=window_region)

        unmatched_resources = []
        unmatched_buttons = []

        for resource_name, resource_data in self.resources.items():
            detections = Utils.match_template(screenshot,model)
            matched = False

            for detection in detections:
                if detection["class_id"] == resource_data["code"]:
                    #x1, y1, x2, y2 = detection["box"]
                    resource_data["position"] = detection["box"]
                    print(f"资源 {resource_name} 匹配成功，位置: {resource_data['position']}")
                    matched = True
                    break
            if not matched:
                unmatched_resources.append(resource_name)

        # 匹配 buttons
        for button_name, button_data in self.buttons.items():
            detections = Utils.match_template(screenshot,model)
            matched = False
            for detection in detections:
                if detection["class_id"] == button_data["code"]:
                    #x1, y1, x2, y2 = detection["box"]
                    button_data["position"] = detection["box"]
                    print(f"按钮 {button_name} 匹配成功，位置: {button_data['position']}")
                    matched = True
                    break
            if not matched:
                unmatched_buttons.append(button_name)

        if unmatched_resources:
            print(f"未匹配的资源: {', '.join(unmatched_resources)}")
        if unmatched_buttons:
            print(f"未匹配的按钮: {', '.join(unmatched_buttons)}")

    def add_transition(self,button_name,target_screen):
        if button_name in self.buttons:
            self.children[button_name] = target_screen
            print(f"已经添加从 {self.name} 通过 {button_name} 跳转到 {target_screen.name} 的关系")
        else:
            print(f"按钮 {button_name} 不存在于 {self.name} 的按钮列表中")

class MenuTree:
    def __init__(self, root_node):
        self.root = root_node

    def find_path(self, start_node, target_screen_name):
        path = []
        visited = set()
        found = self._find_path_dfs(start_node, target_screen_name, path, visited)
        if found:
            return path
        else:
            print("未找到路径")
            return None

    def _find_path_dfs(self, current_game_screen, target_screen_name, path, visited):
        if current_game_screen.screen_name in visited:
            return False
        visited.add(current_game_screen.screen_name)
        if current_game_screen.screen_name == target_screen_name:
            return True
        for button_name, child_node in current_game_screen.children.items():
            path.append((button_name, child_node.screen_name))  # 将当前跳转操作添加到路径中
            if self._find_path_dfs(child_node, target_screen_name, path, visited):
                return True
            path.pop()
        return False


