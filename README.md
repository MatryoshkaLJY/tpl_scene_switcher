# TPL场景切换器

这是一个用于控制TPL比赛中推流导播的OBS场景切换器。

## 功能特性

- 简洁的Web界面
- 可配置的OBS WebSocket连接
- 支持多种场景切换模式：
  - 现场摄像
  - 个人赛
  - DP团队赛
  - SP团队赛

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行应用

```bash
streamlit run streamlit_app.py
```

应用将在浏览器中打开，默认地址为 `http://localhost:8501`

## 使用说明

### 1. 连接配置
在侧边栏配置以下参数：
- **OBS WebSocket配置**：
  - 主机地址：默认为 `localhost`
  - 端口：默认为 `4455`
  - 密码：默认为 `123456`
- **串口配置**：
  - 串口号：默认为 `COM5`
  - 波特率：默认为 `115200`

### 2. 场景切换

#### 现场摄像
- 点击"切换到现场摄像"按钮即可

#### 个人赛
- 点击"切换到个人赛"按钮即可

#### DP团队赛
需要配置以下参数：
- **队伍信息**：队伍名称、选手名称
- **比分信息**：双方得分
- **机台配置**：选择机台号（1-4）
- **顶部文字**：显示的文字内容

#### SP团队赛
除了DP团队赛的配置外，还需要：
- **选手位置**：选择1P或2P位置

## 文件结构

```
tpl_scene_switcher/
├── streamlit_app.py    # Streamlit前端应用
├── switcher.py         # OBS场景切换核心逻辑
├── main.py            # 原始命令行测试文件
├── requirements.txt    # Python依赖
└── README.md          # 说明文档
```
