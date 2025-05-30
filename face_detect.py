import cv2
import numpy as np
import streamlit as st
from PIL import Image

st.set_page_config(
    layout='wide',
)

# 页面的标题
st.markdown(
    body=f"<h1 style='text-align: center;'>人脸检测任务平台</h1>",
    unsafe_allow_html=True
)

st.divider()

# 加载分类器
faceCascade = cv2.CascadeClassifier("xml/haarcascade_frontalface_default.xml")
eyeCascade = cv2.CascadeClassifier("xml/haarcascade_eye.xml")

ctrl, pic = st.columns(spec=2)

with ctrl:
    left, right = st.columns(spec=2)

    with left:
        face_min_size = st.number_input("请设置面部检测的最小边长：", min_value=1, max_value=10000, step=1, value=20)
        face_max_size = st.number_input("请设置面部检测的最大边长：", min_value=1, max_value=10000, step=1, value=200)

        face_scale_factor = st.number_input("请设置面部检测的scaleFactor参数：", min_value=1.01, max_value=1.5,
                                            value=1.1,
                                            help="scaleFactor取值一般为1.05-1.3；取值越大，检测速度越快，但漏检概率变大；取值越小，检测更精细，但误检概率增大")
        face_min_neighbors = st.number_input("请设置面部检测的minNeighbors参数：", min_value=1, max_value=20, step=1,
                                             value=15,
                                             help="minNeighbors取值一般为1-10；取值越大，误检越少，但更容易漏检；取值越小，检测到的人脸更多，但误检概率增大")

    with right:
        eye_min_size = st.number_input("请设置眼部检测的最小边长：", min_value=1, max_value=10000, step=1, value=10)
        eye_max_size = st.number_input("请设置眼部检测的最大边长：", min_value=1, max_value=10000, step=1, value=500)

        eye_scale_factor = st.number_input("请设置眼部检测的scaleFactor参数：", min_value=1.01, max_value=1.5, value=1.1,
                                           help="scaleFactor取值一般为1.05-1.3；取值越大，检测速度越快，但漏检概率变大；取值越小，检测更精细，但误检概率增大")
        eye_min_neighbors = st.number_input("请设置眼部检测的minNeighbors参数：", min_value=1, max_value=20, step=1,
                                            value=8,
                                            help="minNeighbors取值一般为1-10；取值越大，误检越少，但更容易漏检；取值越小，检测到的人眼更多，但误检概率增大")

    # 文件上传器
    uploaded_file = st.file_uploader("请上传一张人脸图片：", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:

    # 将上传的文件转换为OpenCV格式
    image = Image.open(uploaded_file)
    img = np.array(image)

    # OpenCV需要BGR格式，而PIL是RGB格式
    if len(img.shape) == 3 and img.shape[-1] == 3:  # 检查是否有3个颜色通道
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # 人脸检测
    faces = faceCascade.detectMultiScale(
        img,
        scaleFactor=face_scale_factor,
        minNeighbors=face_min_neighbors,
        minSize=(face_min_size, face_min_size),
        maxSize=(face_max_size, face_max_size)
    )

    # 在检测到的人脸上绘制矩形并检测眼睛
    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        img_r = img[y:y + h, x:x + w]
        eyes = eyeCascade.detectMultiScale(
            img_r,
            scaleFactor=eye_scale_factor,
            minNeighbors=eye_min_neighbors,
            minSize=(eye_min_size, eye_min_size),
            maxSize=(eye_max_size, eye_max_size)
        )
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(img_r, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)

    # 显示处理后的图片
    with pic:
        st.image(img, caption="人脸和眼睛检测结果", channels="BGR", use_container_width=True)
