import base64
import json
import random
import re
from pathlib import Path

import pandas as pd
import pyperclip
import streamlit as st

import sys

sys.path.append(
    str(
        Path(__file__).resolve().parent.parent
    )
)

current_class = "七年5班"  # 请输入当前班级，格式不限，例：七年1班

# todo:这里设置了三个任务，如果要修改任务数量，要在这里改任务一二三
if not Path(fr"{current_class}.json").exists():
    Path(f"{current_class}.json").write_text(
        json.dumps({fr'{i}': {} for i in ["任务一"]}, ensure_ascii=False, indent=4),
        encoding="UTF-8", )

st.set_page_config(
    layout='wide',
    initial_sidebar_state="collapsed"  # 这里设置了左侧展开栏默认关闭
)

with st.sidebar:
    st.markdown(
        body=f"<h1 style='text-align: center;'>常见标签及其作用</h1>",
        unsafe_allow_html=True
    )
    st.dataframe(
        pd.DataFrame(
            {
                "标签": ["<head></head>", "<title></title>", "<body></body>", "<h1></h1>", "<h2></h2>", "<p></p>",
                         "<center></center>", "<img src='***/***.jpg'>", "<a href='xxxx'></a>"],
                "作用": ["设置文档头部", "设置网页标题", "设置文档主体", "设置内容的一级标题", "设置内容的二级标题",
                         "设置新段落", "将元素水平居中对齐", "设置图像", "设置超链接"]
            }
        ),
        hide_index=True
    )

# 页面的标题
st.markdown(
    body=f"<h1 style='text-align: center;'>html任务平台</h1>",
    unsafe_allow_html=True
)

img_file = st.file_uploader(label="请选择文件", help="选择图像文件并返回带有对应base64编码的img标签",
                            type=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'])
if img_file is not None:
    img_left, img_right = st.columns(spec=2)

    with img_left:
        with st.container(border=True, height=600):
            st.markdown(
                body=f"<h1 style='text-align: center;'>原始图像</h1>",
                unsafe_allow_html=True
            )
            st.image(img_file)

    with img_right:
        with st.container(border=True, height=600):
            st.markdown(
                body=f"<h1 style='text-align: center;'>对应的base64编码</h1>",
                unsafe_allow_html=True
            )
            base4_code = f"<img src='data:{f'image/{img_file.type}' if img_file.type in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'] else 'image/jpeg'};base64,{base64.b64encode(img_file.read()).decode('utf-8')}'>"

            st.text(base4_code, )

            while True:
                pyperclip.copy(str(base4_code))

                if pyperclip.paste() == str(base4_code):
                    st.toast("对着img标签快速三次单击可以全选喔", icon="📋")
                    break

with st.container(border=True):
    st.markdown(
        body=f"<h2 style='text-align: center;'>学生任务</h2>",
        unsafe_allow_html=True
    )

    st.markdown("<h5>任务一</h5>", unsafe_allow_html=True)
    st.checkbox("1.标题更换")
    st.write("将网页中的标题换成：颜乐天纪念中学——开学活动")
    st.checkbox("2.文字更换")
    st.write("将文字简介更换为：开学活动中有一项游戏为猜灯谜，猜中了即可获得奖励")
    st.checkbox("3.图片更换")
    st.write("将图片替换为：灯笼.jpg")
    st.checkbox("4.超链接插入")
    st.write(
        "在灯笼图片的下方插入超链接,链接文字显示“点此了解更多”，链接到的网址为：https://cj.sina.com.cn/articles/view/5787187353/158f1789902001tu4a")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h5>任务二</h5>", unsafe_allow_html=True)
    st.checkbox("1.base64编码转换")
    st.markdown("将“笑脸.jpg”转换为代码再插入到网页代码中。<br>", unsafe_allow_html=True)
