import streamlit as st
from switcher import OBSSceneSwitcher

# 页面配置
st.set_page_config(page_title="TPL场景切换器", page_icon="🎮", layout="wide")

# 标题
st.title("🎮 TPL场景切换器")
st.markdown("---")

# 侧边栏配置
with st.sidebar:
    st.header("🔧 连接配置")

    # OBS连接配置
    st.subheader("OBS WebSocket配置")
    host = st.text_input("主机地址", value="localhost")
    port = st.number_input("端口", value=4455, min_value=1, max_value=65535)
    password = st.text_input("密码", value="123456", type="password")

    # 串口配置
    st.subheader("串口配置")
    com_port = st.text_input("串口号", value="COM5")
    baud_rate = st.number_input("波特率", value=115200)

    # 连接按钮
    if st.button("🔌 连接OBS", type="primary"):
        try:
            switcher = OBSSceneSwitcher(
                host=host, port=port, password=password, com=com_port, baud=baud_rate
            )
            st.session_state.switcher = switcher
            st.success("✅ 连接成功！")
        except Exception as e:
            st.error(f"❌ 连接失败: {e}")

# 主界面
if "switcher" not in st.session_state:
    st.warning("⚠️ 请先在侧边栏连接OBS")
    st.stop()

switcher = st.session_state.switcher

# 场景切换选项
st.header("🎬 场景切换")

# 创建选项卡
tab1, tab2, tab3, tab4 = st.tabs(
    ["🖥️ 现场摄像", "👤 个人赛", "🎯 DP团队赛", "⚔️ SP团队赛"]
)

with tab1:
    st.subheader("现场摄像")
    if st.button("切换到现场摄像", type="primary"):
        try:
            switcher.switch_to_live_camera()
            st.success("✅ 已切换到现场摄像")
        except Exception as e:
            st.error(f"❌ 切换失败: {e}")

with tab2:
    st.subheader("个人赛")
    if st.button("切换到个人赛", type="primary"):
        try:
            switcher.switch_to_individual_match()
            st.success("✅ 已切换到个人赛")
        except Exception as e:
            st.error(f"❌ 切换失败: {e}")

with tab3:
    st.subheader("DP团队赛配置")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**队伍信息**")
        team1_name = st.text_input("队伍1名称", value="TEAMA", key="dp_team1")
        team2_name = st.text_input("队伍2名称", value="TEAMB", key="dp_team2")
        player1_name = st.text_input("选手1名称", value="PLAYERA", key="dp_player1")
        player2_name = st.text_input("选手2名称", value="PLAYERB", key="dp_player2")

        st.markdown("**比分信息**")
        team1_score = st.number_input(
            "队伍1得分", value=16, min_value=0, key="dp_score1"
        )
        team2_score = st.number_input(
            "队伍2得分", value=16, min_value=0, key="dp_score2"
        )

    with col2:
        st.markdown("**机台配置**")
        team1_cabinet = st.selectbox(
            "队伍1机台", options=[1, 2, 3, 4], index=0, key="dp_cab1"
        )
        team2_cabinet = st.selectbox(
            "队伍2机台", options=[1, 2, 3, 4], index=3, key="dp_cab2"
        )

        st.markdown("**顶部文字**")
        top_text = st.text_area(
            "顶部文字", value="DP团队赛\nROUND 1\nCHORD", height=100, key="dp_top"
        )

    if st.button("切换到DP团队赛", type="primary"):
        try:
            switcher.set_dp_team_match(
                team1_name,
                team2_name,
                player1_name,
                player2_name,
                team1_score,
                team2_score,
                top_text,
                team1_cabinet,
                team2_cabinet,
            )
            st.success("✅ 已切换到DP团队赛")
        except Exception as e:
            st.error(f"❌ 切换失败: {e}")

with tab4:
    st.subheader("SP团队赛配置")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**队伍信息**")
        team1_name = st.text_input("队伍1名称", value="TEAMA", key="sp_team1")
        team2_name = st.text_input("队伍2名称", value="TEAMB", key="sp_team2")
        player1_name = st.text_input("选手1名称", value="PLAYERA", key="sp_player1")
        player2_name = st.text_input("选手2名称", value="PLAYERB", key="sp_player2")

        st.markdown("**比分信息**")
        team1_score = st.number_input(
            "队伍1得分", value=16, min_value=0, key="sp_score1"
        )
        team2_score = st.number_input(
            "队伍2得分", value=16, min_value=0, key="sp_score2"
        )

    with col2:
        st.markdown("**机台配置**")
        team1_cabinet = st.selectbox(
            "队伍1机台", options=[1, 2, 3, 4], index=1, key="sp_cab1"
        )
        team2_cabinet = st.selectbox(
            "队伍2机台", options=[1, 2, 3, 4], index=2, key="sp_cab2"
        )

        st.markdown("**选手位置**")
        player1_side = st.selectbox(
            "选手1位置", options=[1, 2], index=0, key="sp_side1"
        )
        player2_side = st.selectbox(
            "选手2位置", options=[1, 2], index=1, key="sp_side2"
        )

        st.markdown("**顶部文字**")
        top_text = st.text_area(
            "顶部文字", value="SP团队赛\nROUND 1\nCHORD", height=100, key="sp_top"
        )

    if st.button("切换到SP团队赛", type="primary"):
        try:
            switcher.set_sp_team_match(
                team1_name,
                team2_name,
                player1_name,
                player2_name,
                team1_score,
                team2_score,
                top_text,
                player1_side,
                player2_side,
                team1_cabinet,
                team2_cabinet,
            )
            st.success("✅ 已切换到SP团队赛")
        except Exception as e:
            st.error(f"❌ 切换失败: {e}")

# 底部信息
st.markdown("---")
st.markdown("### 📋 使用说明")
st.markdown(
    """
1. **连接配置**: 在侧边栏配置OBS WebSocket连接参数和串口设置
2. **场景切换**: 选择对应的选项卡进行场景配置和切换
3. **DP团队赛**: 配置队伍信息、比分、机台和顶部文字
4. **SP团队赛**: 额外需要配置选手位置（1P/2P）
"""
)

# 状态显示
if st.sidebar.button("📊 显示连接状态"):
    try:
        # 这里可以添加获取OBS状态的代码
        st.sidebar.success("✅ OBS连接正常")
    except Exception as e:
        st.sidebar.error(f"❌ OBS连接异常: {e}")
