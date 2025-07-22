from switcher import OBSSceneSwitcher

# 创建场景切换器实例
switcher = OBSSceneSwitcher()

top_text = """SP团队赛
ROUND 1
CHORD
"""
# 配置 "DP团队赛" 场景
#switcher.set_dp_team_match("TEAMA", "TEAMB", "PLAYERA", "PLAYERB", 16 ,16, top_text, 1, 4)

# 配置 "SP团队赛" 场景
switcher.set_sp_team_match("TEAMA", "TEAMB", "PLAYERA", "PLAYERB", 16 ,16, top_text, 1, 2, 2, 3)

# 切换到其他场景
# switcher.switch_to_live_camera()
# switcher.switch_to_individual_match()
# switcher.switch_to_sp_team_match()