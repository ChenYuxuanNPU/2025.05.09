import random
from collections import Counter

import jieba
import matplotlib.pyplot as plt
import streamlit as st
from pandas.core.computation.ops import isnumeric
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie, WordCloud, Radar, Scatter, PictorialBar
from pyecharts.globals import SymbolType
from streamlit_echarts import st_pyecharts


def draw_word_cloud_chart(words: list, title: str, shape: str = "circle") -> None:
    """
    绘制词云图
    :param words: 词列表，以出现频率作为数值
    :param title: 图表标题
    :param shape: 词云图形状，默认圆形
    :return:
    """

    st_pyecharts(
        chart=(
            WordCloud()
            .add(series_name=title, data_pair=words, word_size_range=[25, 40], shape=shape, width="900px",
                 height=f"600px", pos_top="10%")
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=title, title_textstyle_opts=opts.TextStyleOpts(font_size=40), pos_left="center", pos_top="2%"
                ),
            )
        ),
        height=f"600px"
    )

    return None


def draw_radar(data: dict, indicator: dict, title: str):
    chart = Radar()

    chart.add_schema(
        schema=[
            opts.RadarIndicatorItem(name=key, max_=value) for key, value in indicator.items()
        ],
        splitarea_opt=opts.SplitAreaOpts(
            is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
        ),
        textstyle_opts=opts.TextStyleOpts(color="black"),
    )

    for key, value in data.items():
        chart.add(
            series_name=key,
            data=value[0],
            color=value[1]
        )

    chart.set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    chart.set_global_opts(
        title_opts=opts.TitleOpts(title=title), legend_opts=opts.LegendOpts()
    )

    st_pyecharts(
        chart=chart,
        height="600px"
    )


def draw_scatter(data: list, ):
    data.sort(key=lambda x: x[0])
    x_data = [d[0] for d in data]
    y_data = [d[1] for d in data]

    chart = Scatter()
    chart.add_xaxis(
        xaxis_data=x_data
    )
    chart.add_yaxis(
        series_name="",
        y_axis=y_data,
        symbol_size=20,
        label_opts=opts.LabelOpts(is_show=False),
    )
    chart.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
        ),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        tooltip_opts=opts.TooltipOpts(is_show=False),
    )

    st_pyecharts(
        chart=chart,
        height="600px"
    )


def draw_PictorialBar(data: dict, title: str):
    chart = PictorialBar()

    chart.add_xaxis(list(data.keys()))
    chart.add_yaxis(
        "",
        list(data.values()),
        label_opts=opts.LabelOpts(is_show=False),
        symbol_size=18,
        symbol_repeat="fixed",
        symbol_offset=[0, 0],
        is_symbol_clip=True,
        symbol=SymbolType.ROUND_RECT,
    )

    chart.reversal_axis()
    chart.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        xaxis_opts=opts.AxisOpts(is_show=False),
        yaxis_opts=opts.AxisOpts(
            axistick_opts=opts.AxisTickOpts(is_show=False),
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(opacity=0)
            ),
        ),
    )

    st_pyecharts(
        chart=chart,
        height="600px"
    )


st.set_page_config(
    layout='wide',
    initial_sidebar_state="collapsed"
)

with st.sidebar:
    st.markdown("""
更多图表示例链接：<br>
<a href="https://echarts.apache.org/examples/en/index.html">echarts官方示例<a><br>
<a href="https://gallery.pyecharts.org/#/README">pyecharts官方示例<a><br>
<a href="https://matplotlib.org/stable/gallery/index.html#">matplotlib官方示例<a><br>
""", unsafe_allow_html=True)

# 页面的标题
st.markdown(
    body=f"<h1 style='text-align: center;'>数据大屏demo</h1>",
    unsafe_allow_html=True
)

st.divider()

st.markdown(
    body=f"<h3 style='text-align: center;'>基础图表示例</h3>",
    unsafe_allow_html=True
)

left, mid, right = st.columns(spec=3)

with left:
    with st.container(border=True, height=449):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        fig, ax = plt.subplots()

        x = [item for item in range(20)]
        y = [random.randint(20, 60) for _ in range(20)]

        ax.bar(x, y)

        ax.set_ylabel('Y轴')
        ax.set_xlabel("X轴")
        ax.set_title('随机数图表1')

        st.pyplot(fig)

    with st.expander("代码实现"):
        st.code("""
plt.rcParams['font.sans-serif'] = ['SimHei']
fig, ax = plt.subplots()

x = [item for item in range(20)]
y = [random.randint(20, 60) for _ in range(20)]

ax.bar(x, y)

ax.set_ylabel('Y轴')
ax.set_xlabel("X轴")
ax.set_title('随机数图表1')

st.pyplot(fig)
""", language="python")

    with st.container(border=True, height=450):
        chart = Bar()
        chart.add_xaxis(x)
        chart.add_yaxis("取值", y)
        chart.set_global_opts(title_opts=opts.TitleOpts(title="随机数图表4"))
        chart.set_series_opts(label_opts=opts.LabelOpts(position="top"))

        st_pyecharts(
            chart=chart,
            height=f"400px"
        )

    with st.expander("代码实现"):
        st.code("""
x = [item for item in range(20)]
y = [random.randint(20, 60) for _ in range(20)]

chart = Bar()
chart.add_xaxis(x)
chart.add_yaxis("取值", y)
chart.set_global_opts(title_opts=opts.TitleOpts(title="随机数图表4"))
chart.set_series_opts(label_opts=opts.LabelOpts(position="top"))

st_pyecharts(
    chart=chart,
    height=f"400px"
)
""", language="python")

with mid:
    with st.container(border=True, height=447):
        # 创建Matplotlib图形
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x, y, label='取值', color='blue', linewidth=2)
        ax.set_title("随机数图表2")
        ax.set_xlabel("X轴")
        ax.set_ylabel("Y轴")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.5)

        # 在Streamlit中显示图形
        st.pyplot(fig)

    with st.expander("代码实现"):
        st.code("""
x = [item for item in range(20)]
y = [random.randint(20, 60) for _ in range(20)]

# 创建Matplotlib图形
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x, y, label='取值', color='blue', linewidth=2)
ax.set_title("随机数图表2")
ax.set_xlabel("X轴")
ax.set_ylabel("Y轴")
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)

# 在Streamlit中显示图形
st.pyplot(fig)
""", language="python")

    with st.container(border=True, height=450):
        chart = Line()
        chart.add_xaxis(x)
        chart.add_yaxis("取值", y, is_symbol_show=True)
        chart.set_global_opts(title_opts=opts.TitleOpts(title="随机数图表5"))
        chart.set_series_opts(label_opts=opts.LabelOpts(position="top"))

        st_pyecharts(
            chart=chart,
            height=f"400px"
        )
    with st.expander("代码实现"):
        st.code("""
x = [item for item in range(20)]
y = [random.randint(20, 60) for _ in range(20)]

chart = Line()
chart.add_xaxis(x)
chart.add_yaxis("取值", y, is_symbol_show=True)
chart.set_global_opts(title_opts=opts.TitleOpts(title="随机数图表5"))
chart.set_series_opts(label_opts=opts.LabelOpts(position="top"))

st_pyecharts(
    chart=chart,
    height=f"400px"
)
""", language="python")

    with right:
        with st.container(border=True, height=448):
            labels = ['Python', 'C', 'Java', 'HTML']
            sizes = [random.randint(10, 30) for _ in range(4)]

            fig, ax = plt.subplots(figsize=(4, 20), )
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', textprops={'fontsize': 8})

            st.pyplot(fig, use_container_width=True)

        with st.expander("代码实现"):
            st.code("""
labels = ['Python', 'C', 'Java', 'HTML']
sizes = [random.randint(10, 30) for _ in range(4)]

fig, ax = plt.subplots(figsize=(4, 20), )
ax.pie(sizes, labels=labels, autopct='%1.1f%%', textprops={'fontsize': 8})

st.pyplot(fig, use_container_width=True)
""", language="python")

        with st.container(border=True, height=450):
            chart = Pie()
            chart.add("", [list(z) for z in
                           zip(['Python', 'C', 'Java', 'HTML'], [random.randint(10, 30) for _ in range(4)])])
            chart.set_global_opts(title_opts=opts.TitleOpts(title="随机图表6"))

            st_pyecharts(
                chart=chart,
                height=f"400px"
            )
        with st.expander("代码实现"):
            st.code("""
chart = Pie()
chart.add("", [list(z) for z in
               zip(['Python', 'C', 'Java', 'HTML'], [random.randint(10, 30) for _ in range(4)])])
chart.set_global_opts(title_opts=opts.TitleOpts(title="随机图表6"))

st_pyecharts(
    chart=chart,
    height=f"400px"
)
""", language="python")

st.divider()

st.markdown(
    body=f"<h2 style='text-align: center;'>拓展图表示例</h2>",
    unsafe_allow_html=True
)

st.markdown(
    body=f"<h4>1.词云图</h4>",
    unsafe_allow_html=True
)

l, r = st.columns(spec=2)

with l:
    paragraph = st.text_area("请输入需要文本分析的文章：", height=600,
                             value="人工智能作为新一轮科技革命的核心驱动力，正深刻重构人类生产生活方式，成为推动教育变革、重塑人才培养模式的关键力量。2017年，国务院发布《新一代人工智能发展规划》，首次将人工智能发展提升至国家战略高度，明确要求在中小学阶段设置人工智能相关课程。2024年，教育部发布《关于加强中小学人工智能教育的通知》，从课程设置、教学资源、师资建设等方面对中小学人工智能教育提出具体要求。广东省教育厅发布《广东省人工智能赋能基础教育行动方案（2024-2027）》，提出人工智能教育课程建设行动，强调制定课程建设基准、课程体系与知识图谱及实施办法。为响应国家“人工智能+”行动战略，落实人工智能教育的高质量实施，特制定本纲要，为我省中小学人工智能课程体系建设和教学提供指引。各地在执行过程中，可结合本地实际和技术发展，因地制宜实施和完善。中小学人工智能课程以全面提升学生人工智能素养为目标，帮助学生形成理性的人工智能观念，掌握人工智能技术应用能力，发展智能思维，培养智能社会责任。本纲要汲取国内外人工智能教育的研究成果，根据教育部和我省对人工智能课程和教学的明确要求，结合人工智能技术的发展前沿，构建具有广东特色的人工智能课程体系。纲要通过“体验与认识、理解与应用、设计与创造”学段目标逐层深化，帮助学生掌握数据、算法、算力等核心概念，强化人机协同意识，践行安全、包容、公正的伦理准则，助力学生从技术使用者向技术设计者进阶，培育兼具家国情怀、科学素养与创新能力的时代新人。")

    words_stat = [[k, str(v)] for k, v in dict(
        Counter([item for item in jieba.lcut(paragraph) if item != '\n' or not isnumeric(item)])).items()]

with r:
    pass
    draw_word_cloud_chart(words=words_stat, title="词频统计结果")

with st.expander("代码实现"):
    st.code(f"""
    def draw_word_cloud_chart(words: list, title: str, shape: str = "circle") -> None:
        # words示例：{words_stat}
    
        st_pyecharts(
            chart=(
                WordCloud()
                .add(series_name=title, data_pair=words, word_size_range=[25, 40], shape=shape, width="900px",
                     height=f"600px", pos_top="10%")
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=title, title_textstyle_opts=opts.TextStyleOpts(font_size=40), pos_left="center", pos_top="2%"
                    ),
                )
            ),
            height=f"600px"
        )
    
        return None
    """, language="python")

st.markdown(
    body=f"<h4>2.雷达图</h4>",
    unsafe_allow_html=True
)

draw_radar(
    data={
        "学生1": [[[82, 115, 110, 93, 92, 75, 70, 70]], "#4587E7"],
        "学生2": [[[100, 80, 97, 76, 72, 83, 86, 68]], "#b3e4a1"]
    },
    indicator={
        "语文": 120,
        "数学": 120,
        "英语": 120,
        "物理": 100,
        "化学": 100,
        "道法": 90,
        "历史": 90,
        "体育": 70
    },
    title="学生成绩雷达图"
)

with st.expander("代码实现"):
    st.code(f"""
def draw_radar(data: dict, indicator: dict, title: str):
    '''data示例：{{
        "学生1": [[[82, 115, 110, 93, 92, 75, 70, 70]], "#4587E7"],
        "学生2": [[[100, 80, 97, 76, 72, 83, 86, 68]], "#b3e4a1"]
    }}'''
    
    '''indicator示例：{{
        "语文": 120,
        "数学": 120,
        "英语": 120,
        "物理": 100,
        "化学": 100,
        "道法": 90,
        "历史": 90,
        "体育": 70
    }}'''
    
    chart = Radar()

    chart.add_schema(
        schema=[
            opts.RadarIndicatorItem(name=key, max_=value) for key, value in indicator.items()
        ],
        splitarea_opt=opts.SplitAreaOpts(
            is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
        ),
        textstyle_opts=opts.TextStyleOpts(color="black"),
    )

    for key, value in data.items():
        chart.add(
            series_name=key,
            data=value[0],
            color=value[1]
        )

    chart.set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    chart.set_global_opts(
        title_opts=opts.TitleOpts(title=title), legend_opts=opts.LegendOpts()
    )

    st_pyecharts(
        chart=chart,
        height="600px"
    )
    """, language="python")

st.markdown(
    body=f"<h4>3.散点图</h4>",
    unsafe_allow_html=True
)

draw_scatter(
    data=[
        [random.randint(5, 95), random.randint(5, 95)] for _ in range(50)
    ]
)

with st.expander("代码示例"):
    st.code(f"""
def draw_scatter(data: list, ):
    # data示例：{[[random.randint(5, 95), random.randint(5, 95)] for _ in range(50)]}

    data.sort(key=lambda x: x[0])
    x_data = [d[0] for d in data]
    y_data = [d[1] for d in data]

    chart = Scatter()
    chart.add_xaxis(
        xaxis_data=x_data
    )
    chart.add_yaxis(
        series_name="",
        y_axis=y_data,
        symbol_size=20,
        label_opts=opts.LabelOpts(is_show=False),
    )
    chart.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
        ),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        tooltip_opts=opts.TooltipOpts(is_show=False),
    )

    st_pyecharts(
        chart=chart,
        height="600px"
    )
""", language="python")

st.markdown(
    body=f"<h4>4.象型柱状图</h4>",
    unsafe_allow_html=True
)

draw_PictorialBar(
    data={
        "中山大学": 20,
        "华南理工大学": 25,
        "暨南大学": 45,
        "华南师范大学": 60,
        "华南农业大学": 89,
        "广东工业大学": 95,
        "广州大学": 120,
        "广东外语外贸大学": 128,
    },
    title="各高校录取人数"
)

with st.expander("代码示例"):
    st.code(f"""
def draw_PictorialBar(data: dict, title: str):
    '''data示例：{{
    "中山大学": 20,
    "华南理工大学": 25,
    "暨南大学": 45,
    "华南师范大学": 60,
    "华南农业大学": 89,
    "广东工业大学": 95,
    "广州大学": 120,
    "广东外语外贸大学": 128,
}}'''
    chart = PictorialBar()

    chart.add_xaxis(list(data.keys()))
    chart.add_yaxis(
        "",
        list(data.values()),
        label_opts=opts.LabelOpts(is_show=False),
        symbol_size=18,
        symbol_repeat="fixed",
        symbol_offset=[0, 0],
        is_symbol_clip=True,
        symbol=SymbolType.ROUND_RECT,
    )

    chart.reversal_axis()
    chart.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        xaxis_opts=opts.AxisOpts(is_show=False),
        yaxis_opts=opts.AxisOpts(
            axistick_opts=opts.AxisTickOpts(is_show=False),
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(opacity=0)
            ),
        ),
    )

    st_pyecharts(
        chart=chart,
        height="600px"
    )
""", language="python")