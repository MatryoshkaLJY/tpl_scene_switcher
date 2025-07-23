#!/usr/bin/env python3
"""
TPL场景切换器 - Streamlit应用启动脚本
"""

import subprocess
import sys


def main():
    """启动Streamlit应用"""
    try:
        # 检查是否安装了streamlit
        import streamlit

        print("✅ Streamlit已安装")
    except ImportError:
        print("❌ Streamlit未安装，正在安装依赖...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✅ 依赖安装完成")

    # 启动Streamlit应用
    print("🚀 启动TPL场景切换器...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])


if __name__ == "__main__":
    main()
