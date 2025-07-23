import obswebsocket
from obswebsocket import requests
import time
import serial

class OBSSceneSwitcher:
    def __init__(self, host="localhost", port=4455, password="123456", com="COM5", baud=115200):

        self.ws = obswebsocket.obsws(host, port, password)
        self.cab_list = ["IIDX#1", "IIDX#2", "IIDX#3", "IIDX#4"]
        self.cam_list = ["IIDX#1", "CAM#2", "CAM#3", "IIDX#4"]
        try:
            self.serial = serial.Serial(com, baud, timeout=1)
            print(f"已打开串口 {com}，波特率 {baud}")
        except serial.SerialException as e:
            print(f"打开串口失败: {e}")
        try:
            self.ws.connect()
            print("已连接到 OBS WebSocket")
        except Exception as e:
            print(f"无法连接到 OBS WebSocket: {e}")
            raise

    def write_digit_to_serial(self, digit):
        try:
            if not isinstance(digit, int) or digit < 0 or digit > 9:
                raise ValueError("输入必须是 0-9 的整数")
            byte_data = str(digit).encode('ascii')
            self.serial.write(byte_data)
            print(f"已向串口写入数字: {digit}")
        except Exception as e:
            print(f"串口写入失败: {e}")
    
    def switch_to_scene(self, scene_name):
        try:
            self.ws.call(requests.SetCurrentProgramScene(sceneName=scene_name))
            print(f"已切换到场景：{scene_name}")
        except Exception as e:
            print(f"切换到场景 {scene_name} 失败：{e}")

    def set_dp_team_match(self, team1_name, team2_name, player1_name, player2_name, team1_score, team2_score, top_text, team1_cabinet, team2_cabinet):
        scene_name = "DP团队赛"
        self.switch_to_scene(scene_name)
        self.set_text_team( team1_name, team2_name, player1_name, player2_name, team1_score, team2_score, top_text)
        self.set_group_visibility(scene_name, "DPLUI", self.cab_list[team1_cabinet - 1], 0)
        self.set_group_visibility(scene_name, "DPRUI", self.cab_list[team2_cabinet - 1], 0)
        self.set_group_visibility(scene_name, "DPMIDUI", self.cab_list[team1_cabinet - 1], 0)
        self.set_group_visibility(scene_name, "DPLCAM", self.cam_list[team1_cabinet - 1], 0)
        self.set_group_visibility(scene_name, "DPRCAM", self.cam_list[team2_cabinet - 1], 0)
        self.write_digit_to_serial(team1_cabinet)

    def set_sp_team_match(self, team1_name, team2_name, player1_name, player2_name, team1_score, team2_score, top_text, player1_side, player2_side, team1_cabinet, team2_cabinet):
        scene_name = "SP团队赛"
        self.switch_to_scene(scene_name)
        self.set_text_team( team1_name, team2_name, player1_name, player2_name, team1_score, team2_score, top_text)
        self.set_group_visibility(scene_name, "SPLUI", self.cab_list[team1_cabinet - 1], player1_side)
        self.set_group_visibility(scene_name, "SPRUI", self.cab_list[team2_cabinet - 1], player2_side)
        self.set_group_visibility(scene_name, "SPMIDUI", self.cab_list[team1_cabinet - 1], player1_side)
        self.set_group_visibility(scene_name, "SPLCAM", self.cam_list[team1_cabinet - 1], 0)
        self.set_group_visibility(scene_name, "SPRCAM", self.cam_list[team2_cabinet - 1], 0)
        self.write_digit_to_serial(team1_cabinet)

    def set_text_team(self, team1_name, team2_name, player1_name, player2_name, team1_score, team2_score, top_text):
        text_sources = {
            "LSCORE": f"{team1_score}\n    ",
            "RSCORE": f"{team2_score}\n    ",
            "TOPTEXT": top_text + "\n       ",
            "LTEAM": team1_name + "\n       ",
            "RTEAM": team2_name + "\n       ",
            "LPLAYER": player1_name + "\n       ",
            "RPLAYER": player2_name + "\n       "
        }
        for source_name, text_content in text_sources.items():
            try:
                self.ws.call(requests.SetInputSettings(inputName=source_name, inputSettings={"text": text_content}))
                print(f"已将 {source_name} 的文字内容设置为：{text_content}")
            except Exception as e:
                print(f"设置 {source_name} 的文字内容失败：{e}")

    def set_group_visibility(self, scene_name, group_name, item_name, side):
        try:
            # 获取场景中的源列表
            scene_items = self.ws.call(requests.GetSceneItemList(sceneName=scene_name)).getSceneItems()
            for item in scene_items:
                if item["sourceName"] == group_name and item["isGroup"]:
                    # 获取组内的源列表
                    group_items = self.ws.call(requests.GetGroupSceneItemList(sceneName=group_name)).getSceneItems()
                    for index, group_item in enumerate(group_items):
                        source_name = group_item["sourceName"]
                        item_id = group_item["sceneItemId"]  # 获取源的 ID
                        # 检查源名称是否与指定的机台号匹配
                        display_flag = True
                        if side > 0:
                            if index % 2 != side % 2:
                                display_flag = False
                        if source_name == item_name and display_flag:
                            self.ws.call(requests.SetSceneItemEnabled(
                                sceneName=group_name, 
                                sceneItemId=item_id, 
                                sceneItemEnabled=True
                            ))
                            print(f"在组 {group_name} 中将 {source_name} 设置为可见")
                        else:
                            self.ws.call(requests.SetSceneItemEnabled(
                                sceneName=group_name, 
                                sceneItemId=item_id, 
                                sceneItemEnabled=False
                            ))
                            print(f"在组 {group_name} 中将 {source_name} 设置为不可见")
        except Exception as e:
            print(f"设置组 {group_name} 的可见性失败：{e}")

    def switch_to_live_camera(self):
        self.switch_to_scene("现场摄像")

    def switch_to_individual_match(self):
        self.switch_to_scene("个人赛")

    def switch_to_sp_team_match(self):
        self.switch_to_scene("SP团队赛")

    def __del__(self):
        self.ws.disconnect()
        print("已断开 OBS WebSocket 连接")