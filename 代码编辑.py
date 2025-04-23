import json
import random
import re
from pathlib import Path

import pandas as pd
import streamlit as st

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

# 任务保存的代码，初始赋值给的是任务一示例代码
if 'code_0' not in st.session_state:
    st.session_state.code_0 = """
<html>
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


def save_code():
    st.session_state.code_0 = code_0
    st.toast("代码暂存成功！", icon="😋")


def submit_code(code: str, route: str) -> None:
    """
    将学生填写的代码发送到教师机(route格式为："任务一/05")\n
    route中第一项必须为任务x，其中x为汉字大写字符
    route中第二项调用student_number
    :param code: 学生输入的代码
    :param route: 教师机内json文件中学生对应代码的路径
    :return:
    """
    route_item = route.split("/")

    with open(fr'{current_class}.json', mode="r", encoding="UTF-8") as f:
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

    with open(rf'{current_class}.json', mode="w", encoding="UTF-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# 页面的标题
st.markdown(
    body=f"<h1 style='text-align: center;'>html任务平台</h1>",
    unsafe_allow_html=True
)

# 这里要输了大于0的学号才能显示下面的任务内容，学号范围1到60
student_number = st.number_input("请输入您的学号：", min_value=0, max_value=60, step=1)

# if student_number > 0:

# todo 添加任务首先要在这里加任务的title

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

# todo 添加任务还得在这加分支（记得python3.9不支持match语法）
left, right = st.columns(spec=2)

with left:
    with st.container(border=True, height=730):
        code_0 = st.text_area("代码编辑区:", value=st.session_state.code_0, height=520)

        if is_html_correct(html=code_0)[0]:
            st.success("html代码标签基本正确", icon="😋")
        else:
            st.warning(f"html代码中双标签有误：{is_html_correct(html=code_0)[1]}", icon="😳")

        l, r = st.columns(spec=2)
        with l:
            st.button("保存代码", on_click=save_code)
        with r:
            st.button("提交代码", on_click=submit_code, disabled=True if student_number == 0 else False,
                      kwargs={"code": code_0, "route": f"任务一/{student_number}"})

with right:
    with st.container(border=True, height=730):
        st.markdown(code_0, unsafe_allow_html=True)

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
    st.write("将图片替换为：灯笼.png")
    st.checkbox("4.超链接插入")
    st.write(
        "在灯笼图片的下方插入超链接,链接文字显示“点此了解更多”，链接到的网址为：https://cj.sina.com.cn/articles/view/5787187353/158f1789902001tu4a")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h5>任务二</h5>", unsafe_allow_html=True)
    st.checkbox("1.base64编码转换")
    st.markdown("将“笑脸.jpg”转换为代码再插入到网页代码中。<br>", unsafe_allow_html=True)

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
