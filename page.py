import base64
import json
import random
import re
from pathlib import Path

import pandas as pd
import pyperclip
import streamlit as st


def is_html_correct(html: str) -> list:
    """
    初步判断html文本是否合法
    :param html: html文本
    :return: 布尔值
    """
    stack = []
    # 正则匹配所有 HTML 标签（包括自闭合标签）
    tags = re.findall(r'<(/?)(\w+)[^>]*>', html)

    for is_close, tag_name in tags:
        # 跳过自闭合标签（如 <img />）
        if tag_name in ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source',
                        'track', 'wbr']:
            continue

        if not is_close:  # 开始标签（如 <div>）
            stack.append(tag_name)
        else:  # 结束标签（如 </div>）
            if not stack:
                return [False, f"{tag_name}无对应的开始标签"]  # 结束标签无匹配的开始标签
            if stack[-1] != tag_name:
                return [False, f"缺失了结束标签</{stack[-1]}>或出现了标签交叉"]  # 标签交叉（如 <div><p></div></p>）
            stack.pop()  # 匹配成功，弹出栈顶

    return [len(stack) == 0, f"以下标签缺少结束标签：<{None if len(stack) == 0 else stack[-1]}>"]  # 栈为空则所有标签匹配


def give_positive_feedback() -> None:
    """
    给成功提交正确代码的学生提供正反馈
    :return:
    """

    number = random.randint(0, 1)

    if number == 0:
        st.snow()
        return None

    elif number == 1:
        st.balloons()
        return None

    else:
        return None


def save_code():
    st.session_state.new_code_0 = st.session_state.code_0
    st.toast("代码暂存成功！", icon="😋")


def save_stu_num():
    st.session_state.new_student_number = st.session_state.student_number


def submit_code(code: str, route: str) -> None:
    """
    将学生填写的代码发送到教师机(route格式为："代码/05")\n
    route中第一项必须为任务x，其中x为汉字大写字符
    route中第二项调用student_number
    :param code: 学生输入的代码
    :param route: 教师机内json文件中学生对应代码的路径
    :return:
    """
    route_item = route.split("/")

    with open(fr'{st.session_state.current_class}.json', mode="r", encoding="UTF-8") as f:
        data = dict(json.load(f))

    if not route_item[1] in data[route_item[0]]:
        st.toast("代码已上传！", icon="🥳")

        if is_html_correct(html=code)[0]:
            give_positive_feedback()

    elif data[route_item[0]][route_item[1]] == code:
        st.toast("代码与提交版本相同！", icon="😯")

    else:
        st.toast("代码已更新！", icon="😇")

        if is_html_correct(html=code)[0]:
            give_positive_feedback()

    data[route_item[0]][route_item[1]] = code

    with open(rf'{st.session_state.current_class}.json', mode="w", encoding="UTF-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def initial_session_state():
    """
    初始化全局变量
    :return:
    """
    # 任务保存的代码，初始赋值给的是示例代码
    if 'code_0' not in st.session_state:
        st.session_state.code_0 = """<html>
<head>
<title>校园科技节</title>
</head>

<body >
<center>
<h2>科技节体验项目——</h2><h1> 3D打印</h1>
</center>
<p></p><p></p>
<p>3D打印，即三维打印，是一种以数字模型文件为基础，运用金属或塑料等粉末材料以及黏合剂，通过逐层打印的方式来构造物体的技术。当三维打印机为小型化的设备时，此技术称为桌面三维打印。</p>
<center> 
<img src="app/static/3D.jpg" width="348"/>
<p></p>
</center>
<p></p>
<center> 
<<< 主页 >>>
</center>
</body>
</html>
"""

    if "new_code_0" not in st.session_state:
        st.session_state.new_code_0 = st.session_state.code_0

    # todo 课前在这里修改班级
    if "current_class" not in st.session_state:
        st.session_state.current_class = "七年1班"

    if "student_number" not in st.session_state:
        st.session_state.student_number = 0

    if "new_student_number" not in st.session_state:
        st.session_state.new_student_number = st.session_state.student_number

    if not Path(fr"{st.session_state.current_class}.json").exists():
        Path(f"{st.session_state.current_class}.json").write_text(
            json.dumps({fr'{i}': {} for i in ["代码"]}, ensure_ascii=False, indent=4),
            encoding="UTF-8", )


initial_session_state()

st.set_page_config(
    layout='wide',
    initial_sidebar_state="expanded"  # 这里设置了左侧展开栏默认关闭
)

# 使用 CSS 强制页面内所有按钮居中
st.markdown(
    """
    <style>
        .stButton>button {
            display: block;
            margin: 0 auto;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 页面的标题
st.markdown(
    body=f"<h1 style='text-align: center;'>html任务平台</h1>",
    unsafe_allow_html=True
)

st.divider()

with st.sidebar:
    st.markdown(
        body=f"<h3 style='text-align: center;'>常见标签及其作用</h3>",
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

    with st.container(border=True):
        st.markdown("<h5>任务一</h5>", unsafe_allow_html=True)
        st.checkbox("1.标题更换")
        st.write("将网页中的标题换成：颜乐天纪念中学——开学活动")
        st.checkbox("2.文字更换")
        st.write("将文字简介更换为：开学活动中有一项游戏为猜灯谜，猜中了即可获得奖励")
        st.checkbox("3.图片更换")
        st.write("将图片替换为：灯笼.png")
        st.checkbox("4.超链接插入")
        st.write(
            "在灯笼图片的下方插入超链接,链接文字显示“点此了解更多”，链接到的网址为：https://cj.sina.com.cn/articles/view/5787187353/158f1789902001tu4a")
        st.markdown("<h5>任务二</h5>", unsafe_allow_html=True)
        st.checkbox("1.base64编码转换")
        st.markdown("将“笑脸.jpg”转换为代码再插入到网页代码中。<br>", unsafe_allow_html=True)

left, right = st.columns(spec=2)

with left:
    with st.container(border=True, height=850):
        st.text_area("代码编辑区:", height=710, key="code_0", value=st.session_state.new_code_0, on_change=save_code)

        if is_html_correct(html=st.session_state.new_code_0)[0]:
            st.success("html代码标签基本正确", icon="😋")
        else:
            st.warning(f"html代码中双标签有误：{is_html_correct(html=st.session_state.new_code_0)[1]}", icon="😳")

with right:
    with st.container(border=True, height=850):
        with st.container(border=False, height=675):
            st.markdown(st.session_state.new_code_0, unsafe_allow_html=True)

        st.number_input("请输入您的学号：", min_value=0, max_value=60, step=1, key="student_number",
                        value=st.session_state.new_student_number, on_change=save_stu_num)

        st.button("提交代码", on_click=submit_code,
                  disabled=True if st.session_state.new_student_number == 0 else False,
                  kwargs={
                      "code": st.session_state.new_code_0, "route": f"代码/{st.session_state.new_student_number}"
                  })

# with st.container(border=True):
#     st.markdown(
#         body=f"<h2 style='text-align: center;'>学生任务</h2>",
#         unsafe_allow_html=True
#     )
#
#     st.markdown("<h5>任务一</h5>", unsafe_allow_html=True)
#     st.checkbox("1.标题更换")
#     st.write("将网页中的标题换成：颜乐天纪念中学——开学活动")
#     st.checkbox("2.文字更换")
#     st.write("将文字简介更换为：开学活动中有一项游戏为猜灯谜，猜中了即可获得奖励")
#     st.checkbox("3.图片更换")
#     st.write("将图片替换为：灯笼.png")
#     st.checkbox("4.超链接插入")
#     st.write(
#         "在灯笼图片的下方插入超链接,链接文字显示“点此了解更多”，链接到的网址为：https://cj.sina.com.cn/articles/view/5787187353/158f1789902001tu4a")
#     st.markdown("<br>", unsafe_allow_html=True)
#     st.markdown("<h5>任务二</h5>", unsafe_allow_html=True)
#     st.checkbox("1.base64编码转换")
#     st.markdown("将“笑脸.jpg”转换为代码再插入到网页代码中。<br>", unsafe_allow_html=True)
#
#     st.markdown(
#         """
# 任务一：\n
# 1.将网页中的标题换成：\n颜乐天纪念中学——开学活动\n
# 2.文字简介换成：\n开学活动中有一项游戏为猜灯谜，猜中了即可获得奖励\n
# 3.将图片替换为：灯笼.png\n
# 4.在灯笼图片的下方插入一个超链接:\n链接文字显示“点此了解更多”，\n链接到的网址为：https://cj.sina.com.cn/articles/view/5787187353/158f1789902001tu4a\n<br>
# 任务二：\n
#
#         """
#         , unsafe_allow_html=True)


with st.expander(label="课程资源（点击展开）"):
    img_file = st.file_uploader(label="请选择文件", help="选择图像文件并返回带有对应base64编码的img标签",
                                type=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'])
    if img_file is not None:
        img_left, img_right = st.columns(spec=2)

        with img_left:
            with st.container(border=True, height=600):
                st.markdown(
                    body=f"<h2 style='text-align: center;'>原始图像</h2>",
                    unsafe_allow_html=True
                )
                st.image(img_file)

        with img_right:
            with st.container(border=True, height=600):
                st.markdown(
                    body=f"<h2 style='text-align: center;'>对应的base64编码</h2><br><p style='text-align: center;'>快速三次点击文本可以全选img标签</p>",
                    unsafe_allow_html=True
                )
                base4_code = f"<img src='data:{f'image/{img_file.type}' if img_file.type in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'] else 'image/jpeg'};base64,{base64.b64encode(img_file.read()).decode('utf-8')}'>"

                st.text(base4_code, )

                while True:
                    pyperclip.copy(str(base4_code))

                    if pyperclip.paste() == str(base4_code):
                        break

    # st.image("pic/3D.jpg")
    image_paths = ["pic/3D.jpg", "pic/灯笼.jpg", "pic/笑脸.png"]  # 替换为你的实际图片路径

    a, b, c = st.columns(spec=3)

    with a:
        with st.container(height=430):
            st.image("pic/3D.jpg", use_container_width=True)

        with open("pic/3D.jpg", "rb") as f:
            _, col2, _ = st.columns([1.75, 1, 1.75])
            with col2:
                st.download_button(
                    label=f"3D.jpg",
                    data=f,
                    file_name="3D.jpg",
                )

    with b:
        with st.container(height=430):
            st.image("pic/灯笼.png", use_container_width=True)

        with open("pic/灯笼.png", "rb") as f:
            _, col2, _ = st.columns([1.6, 1, 1.6])
            with col2:
                st.download_button(
                    label=f"灯笼.png",
                    data=f,
                    file_name="灯笼.png",
                )

    with c:
        with st.container(height=430):
            st.image("pic/笑脸.png", use_container_width=True)

        with open("pic/笑脸.png", "rb") as f:
            _, col2, _ = st.columns([1.6, 1, 1.6])
            with col2:
                st.download_button(
                    label=f"笑脸.png",
                    data=f,
                    file_name="笑脸.png",
                )
