import base64

import pyperclip
import streamlit as st

st.set_page_config(
    layout='wide'
)


def func1():
    return ["""
<html>
<head>
    <title>简单页面</title>
</head>
<body>
    <h1>你好世界</h1>
    <p>这是一个极简HTML页面</p>
<p><img src="app/static/1.png"></p>
</body>
</html>
    """,]


st.markdown(
    body=f"<h1 style='text-align: center;'>html页面</h1>",
    unsafe_allow_html=True
)

kind = st.selectbox(label="操作类型", options=["任务一", "任务二 -- 编码转换"])

if kind == "任务一":
    left, right = st.columns(spec=2)

    with left:
        with st.container(border=True, height=800):
            edited_code0 = st.text_area("代码编辑区:", value=func1(), height=740, key=0)

    with right:
        with st.container(border=True, height=800):
            st.html(edited_code0)


elif kind == "任务二 -- 编码转换":

    img_file = st.file_uploader(label="请选择文件", help="选择图像文件并返回带有对应base64编码的img标签",
                                type=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'])
    if img_file is not None:
        img_left, img_right = st.columns(spec=2)

        with img_left:
            st.markdown(
                body=f"<h1 style='text-align: center;'>原始图像</h1>",
                unsafe_allow_html=True
            )
            st.image(img_file)

        with img_right:
            st.markdown(
                body=f"<h1 style='text-align: center;'>对应的base64编码</h1>",
                unsafe_allow_html=True
            )
            base4_code = f"<img src='data:{f'image/{img_file.type}' if img_file.type in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'] else 'image/jpeg'};base64,{base64.b64encode(img_file.read()).decode('utf-8')}'>"
            st.text(base4_code, )
            pyperclip.copy(str(base4_code))

            st.toast("base64编码复制成功！", icon="📋")
