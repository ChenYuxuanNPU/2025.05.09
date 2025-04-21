import streamlit as st

# 初始化 session_state（仅在首次运行时设置默认值）
if "user_input" not in st.session_state:
    st.session_state.user_input = "默认值"  # 默认值仅在首次加载时生效

# 显示 text_area，绑定到 session_state
user_input = st.text_area(
    "输入框",
    value=st.session_state.user_input,  # 始终从 session_state 读取
    key="user_input"  # 直接绑定到 session_state 的键
)

st.write("当前内容：", user_input)