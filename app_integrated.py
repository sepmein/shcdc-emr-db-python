import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import configparser
import base64
from io import StringIO, BytesIO
from sqlalchemy import create_engine


# Load configuration from database.ini
def get_config():
    config = configparser.ConfigParser()
    config.read("config/database.ini")
    return config


# Page config with custom theme
st.set_page_config(
    page_title="EMR数据分析平台",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "EMR数据分析平台 - 版本 1.0.0"},
)

# 使用Streamlit的原生主题设置
st.markdown(
    """
<style>
/* 隐藏Streamlit默认页脚 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
/* 按钮悬停效果 */
.stButton>button:hover {
    border-color: #3366cc !important;
    color: #3366cc !important;
}
/* 指标卡片边距 */
div[data-testid="metric-container"] {
    padding: 10px;
    border-radius: 5px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
    background-color: white;
    margin-bottom: 10px;
}
/* 图表容器样式 */
div[data-testid="stExpander"] {
    border-radius: 5px;
    overflow: hidden;
}
/* 增强表格可读性 */
div[data-testid="stTable"] {
    border-radius: 5px;
    overflow: hidden;
}
/* 数据帧容器 */
div[data-testid="stDataFrame"] {
    border-radius: 5px;
    overflow: hidden;
}
</style>
""",
    unsafe_allow_html=True,
)


# Get SQLAlchemy engine
def get_engine():
    config = get_config()
    db_user = config["postgresql"]["user"]
    db_password = config["postgresql"]["password"]
    db_host = config["postgresql"]["host"]
    db_port = config["postgresql"]["port"]
    db_name = config["postgresql"]["database"]
    engine = create_engine(
        f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    return engine


# Function to execute queries and return pandas dataframes
def execute_query(query):
    try:
        engine = get_engine()
        df = pd.read_sql_query(query, engine)
        return df
    except Exception as e:
        st.error(f"查询执行错误: {e}")
        return pd.DataFrame()


# Function to get downloadable link for dataframe
def get_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href


# Function to create a plotly chart with configured template
def create_chart(df, chart_type, x_col, y_col, title, color_col=None):
    fig = None
    if chart_type == "bar":
        fig = px.bar(df, x=x_col, y=y_col, title=title, color=color_col)
    elif chart_type == "pie":
        fig = px.pie(df, names=x_col, values=y_col, title=title)
    elif chart_type == "line":
        fig = px.line(df, x=x_col, y=y_col, title=title, color=color_col)

    if fig is not None:
        fig.update_layout(
            template="plotly_white",
            title={
                "y": 0.95,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
                "font": {"size": 20},
            },
            margin=dict(l=20, r=20, t=60, b=20),
        )
    return fig


# Header with a more modern design - 使用emoji代替外部图像
header_col1, header_col2 = st.columns([1, 5])
with header_col1:
    # 使用大号Emoji替代外部图像
    st.markdown(
        "<h1 style='text-align: center; font-size: 52px; margin: 0; padding: 0;'>📊</h1>",
        unsafe_allow_html=True,
    )
with header_col2:
    st.title("EMR数据分析平台")
    st.markdown(
        "<p style='font-size: 1.1em; color: #666;'>一站式电子病历数据分析工具，助力医疗数据质量管理</p>",
        unsafe_allow_html=True,
    )

# 主导航菜单
app_mode = st.radio(
    "选择应用模式:",
    ["患者信息质量", "医嘱与检验分析"],
    format_func=lambda x: f"👤 {x}" if x == "患者信息质量" else f"💊 {x}",
    horizontal=True,
)

# 患者信息质量分析模式
if app_mode == "患者信息质量":
    st.markdown("## 👤 患者基本信息数据质量分析")

    # 使用标签页组织内容
    quality_tab1, quality_tab2, quality_tab3 = st.tabs(
        ["📋 总体统计", "📊 必填字段分析", "🔍 建议字段分析"]
    )

    with quality_tab1:
        # 总记录数统计
        total_records_query = """
        SELECT COUNT(*) AS 总记录数 FROM emr_back.emr_patient_info;
        """

        # 必填字段统计
        mandatory_fields_query = """
        SELECT 
            SUM(CASE WHEN id IS NULL OR TRIM(id) = '' THEN 1 ELSE 0 END) AS id空值数,
            SUM(CASE WHEN patient_name IS NULL OR TRIM(patient_name) = '' THEN 1 ELSE 0 END) AS 患者姓名空值数,
            SUM(CASE WHEN id_card_type_code IS NULL OR TRIM(id_card_type_code) = '' THEN 1 ELSE 0 END) AS 身份证件类别代码空值数,
            SUM(CASE WHEN id_card_type_name IS NULL OR TRIM(id_card_type_name) = '' THEN 1 ELSE 0 END) AS 身份证件类别名称空值数,
            SUM(CASE WHEN id_card IS NULL OR TRIM(id_card) = '' THEN 1 ELSE 0 END) AS 身份证件号码空值数,
            SUM(CASE WHEN org_code IS NULL OR TRIM(org_code) = '' THEN 1 ELSE 0 END) AS 医疗机构代码空值数,
            SUM(CASE WHEN org_name IS NULL OR TRIM(org_name) = '' THEN 1 ELSE 0 END) AS 医疗机构名称空值数,
            SUM(CASE WHEN operation_time IS NULL THEN 1 ELSE 0 END) AS 操作时间空值数
        FROM emr_back.emr_patient_info;
        """

        # 建议字段统计 (选择最关键的几个)
        suggested_fields_query = """
        SELECT 
            SUM(CASE WHEN gender_code IS NULL OR TRIM(gender_code) = '' THEN 1 ELSE 0 END) AS 性别代码空值数,
            SUM(CASE WHEN birth_date IS NULL THEN 1 ELSE 0 END) AS 出生日期空值数,
            SUM(CASE WHEN tel IS NULL OR TRIM(tel) = '' THEN 1 ELSE 0 END) AS 患者电话空值数,
            SUM(CASE WHEN marital_status_code IS NULL OR TRIM(marital_status_code) = '' THEN 1 ELSE 0 END) AS 婚姻状况代码空值数,
            SUM(CASE WHEN current_addr_detail IS NULL OR TRIM(current_addr_detail) = '' THEN 1 ELSE 0 END) AS 现住详细地址空值数
        FROM emr_back.emr_patient_info;
        """

        # 执行查询
        with st.spinner("正在加载患者信息统计数据..."):
            total_df = execute_query(total_records_query)
            mandatory_df = execute_query(mandatory_fields_query)
            suggested_df = execute_query(suggested_fields_query)

            if not total_df.empty and not mandatory_df.empty and not suggested_df.empty:
                total_records = total_df.iloc[0, 0]

                # 显示总记录数
                st.metric("患者信息总记录数", f"{total_records:,}")

                # 转换为百分比并计算平均完整率
                mandatory_rates = {}
                for col in mandatory_df.columns:
                    field_name = col.replace("空值数", "")
                    empty_count = mandatory_df.iloc[0][col]
                    rate = 100 - (empty_count / total_records * 100)
                    mandatory_rates[field_name] = rate

                suggested_rates = {}
                for col in suggested_df.columns:
                    field_name = col.replace("空值数", "")
                    empty_count = suggested_df.iloc[0][col]
                    rate = 100 - (empty_count / total_records * 100)
                    suggested_rates[field_name] = rate

                # 计算平均完整率
                mandatory_avg = sum(mandatory_rates.values()) / len(mandatory_rates)
                suggested_avg = sum(suggested_rates.values()) / len(suggested_rates)
                overall_score = mandatory_avg * 0.7 + suggested_avg * 0.3

                # 显示整体质量评分
                score_cols = st.columns(3)
                score_cols[0].metric("必填字段平均完整率", f"{mandatory_avg:.2f}%")
                score_cols[1].metric("建议字段平均完整率", f"{suggested_avg:.2f}%")
                score_cols[2].metric("综合质量评分", f"{overall_score:.2f}%")

                # 创建完整率柱状图数据
                completeness_data = pd.DataFrame(
                    {
                        "字段类型": ["必填字段完整率", "建议字段完整率", "综合完整率"],
                        "完整率": [mandatory_avg, suggested_avg, overall_score],
                    }
                )

                # 显示柱状图
                st.subheader("数据完整率概览")
                fig = create_chart(
                    completeness_data, "bar", "字段类型", "完整率", "患者信息数据完整率"
                )
                fig.update_traces(marker_color=["#3366cc", "#109618", "#ff9900"])
                st.plotly_chart(fig, use_container_width=True)

                # 显示详细统计表格
                st.subheader("详细统计")

                # 准备数据表
                stats_data = []
                for field, rate in mandatory_rates.items():
                    stats_data.append(
                        {
                            "字段名称": field,
                            "类型": "必填",
                            "完整率": f"{rate:.2f}%",
                            "缺失数": int(total_records - (rate * total_records / 100)),
                        }
                    )

                for field, rate in suggested_rates.items():
                    stats_data.append(
                        {
                            "字段名称": field,
                            "类型": "建议",
                            "完整率": f"{rate:.2f}%",
                            "缺失数": int(total_records - (rate * total_records / 100)),
                        }
                    )

                stats_df = pd.DataFrame(stats_data)
                st.dataframe(stats_df, use_container_width=True)
            else:
                st.error("无法获取患者信息统计数据")

    with quality_tab2:
        st.subheader("必填字段完整率分析")

        # 按机构统计必填字段完整率
        mandatory_by_org_query = """
        SELECT
            org_name AS 医疗机构名称,
            COUNT(*) AS 记录总数,
            
            -- 必填字段缺失统计
            SUM(CASE WHEN id IS NULL OR TRIM(id) = '' THEN 1 ELSE 0 END) AS ID缺失数,
            ROUND(100.0 * SUM(CASE WHEN id IS NULL OR TRIM(id) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS ID缺失率,
            SUM(CASE WHEN patient_name IS NULL OR TRIM(patient_name) = '' THEN 1 ELSE 0 END) AS 患者姓名缺失数,
            ROUND(100.0 * SUM(CASE WHEN patient_name IS NULL OR TRIM(patient_name) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS 患者姓名缺失率,
            SUM(CASE WHEN id_card_type_code IS NULL OR TRIM(id_card_type_code) = '' THEN 1 ELSE 0 END) AS 证件类型代码缺失数,
            ROUND(100.0 * SUM(CASE WHEN id_card_type_code IS NULL OR TRIM(id_card_type_code) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS 证件类型代码缺失率,
            SUM(CASE WHEN id_card IS NULL OR TRIM(id_card) = '' THEN 1 ELSE 0 END) AS 证件号码缺失数,
            ROUND(100.0 * SUM(CASE WHEN id_card IS NULL OR TRIM(id_card) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS 证件号码缺失率,
            
            -- 综合质量评分（必填字段填写完整率）
            ROUND(100.0 - (
                100.0 * (
                    SUM(CASE WHEN id IS NULL OR TRIM(id) = '' THEN 1 ELSE 0 END) +
                    SUM(CASE WHEN patient_name IS NULL OR TRIM(patient_name) = '' THEN 1 ELSE 0 END) +
                    SUM(CASE WHEN id_card_type_code IS NULL OR TRIM(id_card_type_code) = '' THEN 1 ELSE 0 END) +
                    SUM(CASE WHEN id_card_type_name IS NULL OR TRIM(id_card_type_name) = '' THEN 1 ELSE 0 END) +
                    SUM(CASE WHEN id_card IS NULL OR TRIM(id_card) = '' THEN 1 ELSE 0 END) +
                    SUM(CASE WHEN org_code IS NULL OR TRIM(org_code) = '' THEN 1 ELSE 0 END) +
                    SUM(CASE WHEN operation_time IS NULL THEN 1 ELSE 0 END)
                ) / (COUNT(*) * 7)
            ), 2) AS 必填字段完整率
        FROM
            emr_back.emr_patient_info
        GROUP BY
            org_name
        ORDER BY
            必填字段完整率 DESC, 记录总数 DESC;
        """

        with st.spinner("正在加载机构必填字段统计..."):
            mandatory_org_df = execute_query(mandatory_by_org_query)

            if not mandatory_org_df.empty:
                # 分析视图标签页
                m_view1, m_view2 = st.tabs(["📊 图表分析", "📋 详细数据"])

                with m_view1:
                    # 只展示前10个机构的必填字段完整率
                    top_orgs = mandatory_org_df.head(10)

                    # 计算按完整率排序的数据
                    sorted_by_completeness = mandatory_org_df.sort_values(
                        "必填字段完整率"
                    ).head(10)

                    chart_col1, chart_col2 = st.columns(2)

                    with chart_col1:
                        st.subheader("必填字段完整率最高的医疗机构")
                        fig = px.bar(
                            top_orgs,
                            x="医疗机构名称",
                            y="必填字段完整率",
                            title="必填字段完整率最高的医疗机构",
                            color="必填字段完整率",
                            color_continuous_scale="Viridis",
                        )
                        fig.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig, use_container_width=True)

                    with chart_col2:
                        st.subheader("必填字段完整率最低的医疗机构")
                        fig = px.bar(
                            sorted_by_completeness,
                            x="医疗机构名称",
                            y="必填字段完整率",
                            title="必填字段完整率最低的医疗机构",
                            color="必填字段完整率",
                            color_continuous_scale="Viridis_r",
                        )
                        fig.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig, use_container_width=True)

                    # 散点图：记录总数与必填字段完整率的关系
                    st.subheader("记录总数与必填字段完整率的关系")
                    fig = px.scatter(
                        mandatory_org_df,
                        x="记录总数",
                        y="必填字段完整率",
                        size="记录总数",
                        color="必填字段完整率",
                        hover_name="医疗机构名称",
                        color_continuous_scale="Viridis",
                        title="各机构记录总数与必填字段完整率关系",
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with m_view2:
                    # 简化筛选和分页控件
                    filter_col1, filter_col2 = st.columns([3, 1])
                    with filter_col1:
                        search_term = st.text_input(
                            "按机构名称筛选:",
                            placeholder="输入机构名称关键词",
                            key="mandatory_search",
                        )
                    with filter_col2:
                        rows_per_page = st.selectbox(
                            "每页显示:", [10, 25, 50, 100], key="mandatory_rows"
                        )

                    # 应用筛选
                    if search_term:
                        filtered_data = mandatory_org_df[
                            mandatory_org_df["医疗机构名称"].str.contains(
                                search_term, case=False
                            )
                        ]
                    else:
                        filtered_data = mandatory_org_df

                    # 分页设置
                    total_pages = max(1, (len(filtered_data) - 1) // rows_per_page + 1)
                    page_num = 1

                    if total_pages > 1:
                        page_col1, page_col2 = st.columns([3, 1])
                        with page_col1:
                            page_num = st.slider(
                                "页码", 1, total_pages, 1, key="mandatory_page"
                            )
                        with page_col2:
                            st.text(f"共 {total_pages} 页")

                    # 数据显示范围
                    start_idx = (page_num - 1) * rows_per_page
                    end_idx = min(start_idx + rows_per_page, len(filtered_data))

                    # 显示表格数据
                    st.dataframe(filtered_data.iloc[start_idx:end_idx])
                    st.text(
                        f"显示 {start_idx+1}-{end_idx} 行，共 {len(filtered_data)} 行"
                    )

                    # 提供下载选项
                    st.download_button(
                        label="📥 下载必填字段完整率统计",
                        data=mandatory_org_df.to_csv(index=False).encode("utf-8"),
                        file_name="patient_info_mandatory_fields.csv",
                        mime="text/csv",
                    )
            else:
                st.error("无法获取机构必填字段统计数据")

    with quality_tab3:
        st.subheader("建议字段完整率分析")

        # 按机构统计建议字段完整率
        suggested_by_org_query = """
        SELECT
            org_name AS 医疗机构名称,
            COUNT(*) AS 记录总数,
            
            -- 核心建议填写字段统计
            SUM(CASE WHEN gender_code IS NULL OR TRIM(gender_code) = '' THEN 1 ELSE 0 END) AS 性别代码缺失数,
            ROUND(100.0 * SUM(CASE WHEN gender_code IS NULL OR TRIM(gender_code) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS 性别代码缺失率,
            
            SUM(CASE WHEN birth_date IS NULL THEN 1 ELSE 0 END) AS 出生日期缺失数,
            ROUND(100.0 * SUM(CASE WHEN birth_date IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS 出生日期缺失率,
            
            SUM(CASE WHEN tel IS NULL OR TRIM(tel) = '' THEN 1 ELSE 0 END) AS 电话号码缺失数,
            ROUND(100.0 * SUM(CASE WHEN tel IS NULL OR TRIM(tel) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS 电话号码缺失率,
            
            SUM(CASE WHEN marital_status_code IS NULL OR TRIM(marital_status_code) = '' THEN 1 ELSE 0 END) AS 婚姻状况缺失数,
            ROUND(100.0 * SUM(CASE WHEN marital_status_code IS NULL OR TRIM(marital_status_code) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS 婚姻状况缺失率,
            
            -- 建议填写字段综合完整率（选取10个重要的建议字段）
            ROUND(100.0 - (
                100.0 * (
                    SUM(CASE WHEN gender_code IS NULL OR TRIM(gender_code) = '' THEN 1 ELSE 0 END) +
                    SUM(CASE WHEN birth_date IS NULL THEN 1 ELSE 0 END) +
                    SUM(CASE WHEN nation_code IS NULL OR TRIM(nation_code) = '' THEN 1 ELSE 0 END) +
                    SUM(CASE WHEN current_addr_code IS NULL OR TRIM(current_addr_code) = '' THEN 1 ELSE 0 END) +
                    SUM(CASE WHEN current_addr_detail IS NULL OR TRIM(current_addr_detail) = '' THEN 1 ELSE 0 END) +
                    SUM(CASE WHEN marital_status_code IS NULL OR TRIM(marital_status_code) = '' THEN 1 ELSE 0 END) +
                    SUM(CASE WHEN education_code IS NULL OR TRIM(education_code) = '' THEN 1 ELSE 0 END) +
                    SUM(CASE WHEN tel IS NULL OR TRIM(tel) = '' THEN 1 ELSE 0 END) +
                    SUM(CASE WHEN contacts IS NULL OR TRIM(contacts) = '' THEN 1 ELSE 0 END) +
                    SUM(CASE WHEN contacts_tel IS NULL OR TRIM(contacts_tel) = '' THEN 1 ELSE 0 END)
                ) / (COUNT(*) * 10)
            ), 2) AS 建议字段完整率
        FROM
            emr_back.emr_patient_info
        GROUP BY
            org_name
        ORDER BY
            建议字段完整率 DESC, 记录总数 DESC;
        """

        with st.spinner("正在加载机构建议字段统计..."):
            suggested_org_df = execute_query(suggested_by_org_query)

            if not suggested_org_df.empty:
                # 分析视图标签页
                s_view1, s_view2 = st.tabs(["📊 图表分析", "📋 详细数据"])

                with s_view1:
                    # 只展示前10个机构的建议字段完整率
                    top_orgs = suggested_org_df.head(10)

                    # 计算按完整率排序的数据
                    sorted_by_completeness = suggested_org_df.sort_values(
                        "建议字段完整率"
                    ).head(10)

                    chart_col1, chart_col2 = st.columns(2)

                    with chart_col1:
                        st.subheader("建议字段完整率最高的医疗机构")
                        fig = px.bar(
                            top_orgs,
                            x="医疗机构名称",
                            y="建议字段完整率",
                            title="建议字段完整率最高的医疗机构",
                            color="建议字段完整率",
                            color_continuous_scale="Viridis",
                        )
                        fig.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig, use_container_width=True)

                    with chart_col2:
                        st.subheader("建议字段完整率最低的医疗机构")
                        fig = px.bar(
                            sorted_by_completeness,
                            x="医疗机构名称",
                            y="建议字段完整率",
                            title="建议字段完整率最低的医疗机构",
                            color="建议字段完整率",
                            color_continuous_scale="Viridis_r",
                        )
                        fig.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig, use_container_width=True)

                    # 核心指标对比图
                    st.subheader("核心建议字段缺失率对比")

                    # 准备核心指标数据
                    core_metric_data = []
                    for _, row in suggested_org_df.head(10).iterrows():
                        core_metric_data.extend(
                            [
                                {
                                    "机构名称": row["医疗机构名称"],
                                    "指标": "性别代码",
                                    "缺失率": row["性别代码缺失率"],
                                },
                                {
                                    "机构名称": row["医疗机构名称"],
                                    "指标": "出生日期",
                                    "缺失率": row["出生日期缺失率"],
                                },
                                {
                                    "机构名称": row["医疗机构名称"],
                                    "指标": "电话号码",
                                    "缺失率": row["电话号码缺失率"],
                                },
                                {
                                    "机构名称": row["医疗机构名称"],
                                    "指标": "婚姻状况",
                                    "缺失率": row["婚姻状况缺失率"],
                                },
                            ]
                        )

                    core_metrics_df = pd.DataFrame(core_metric_data)

                    # 创建分组柱状图
                    fig = px.bar(
                        core_metrics_df,
                        x="机构名称",
                        y="缺失率",
                        color="指标",
                        barmode="group",
                        title="核心建议字段缺失率对比（前10个机构）",
                    )
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)

                with s_view2:
                    # 简化筛选和分页控件
                    filter_col1, filter_col2 = st.columns([3, 1])
                    with filter_col1:
                        search_term = st.text_input(
                            "按机构名称筛选:",
                            placeholder="输入机构名称关键词",
                            key="suggested_search",
                        )
                    with filter_col2:
                        rows_per_page = st.selectbox(
                            "每页显示:", [10, 25, 50, 100], key="suggested_rows"
                        )

                    # 应用筛选
                    if search_term:
                        filtered_data = suggested_org_df[
                            suggested_org_df["医疗机构名称"].str.contains(
                                search_term, case=False
                            )
                        ]
                    else:
                        filtered_data = suggested_org_df

                    # 分页设置
                    total_pages = max(1, (len(filtered_data) - 1) // rows_per_page + 1)
                    page_num = 1

                    if total_pages > 1:
                        page_col1, page_col2 = st.columns([3, 1])
                        with page_col1:
                            page_num = st.slider(
                                "页码", 1, total_pages, 1, key="suggested_page"
                            )
                        with page_col2:
                            st.text(f"共 {total_pages} 页")

                    # 数据显示范围
                    start_idx = (page_num - 1) * rows_per_page
                    end_idx = min(start_idx + rows_per_page, len(filtered_data))

                    # 显示表格数据
                    st.dataframe(filtered_data.iloc[start_idx:end_idx])
                    st.text(
                        f"显示 {start_idx+1}-{end_idx} 行，共 {len(filtered_data)} 行"
                    )

                    # 提供下载选项
                    st.download_button(
                        label="📥 下载建议字段完整率统计",
                        data=suggested_org_df.to_csv(index=False).encode("utf-8"),
                        file_name="patient_info_suggested_fields.csv",
                        mime="text/csv",
                    )
            else:
                st.error("无法获取机构建议字段统计数据")

else:  # 医嘱与检验分析模式
    # Define data types
    DATA_TYPES = {
        "医嘱处方项": {
            "item_table": "emr_back.emr_order_item",
            "parent_table": "emr_back.emr_order",
            "join_field": "order_id",
            "icon": "💊",
        },
        "检验项目": {
            "item_table": "emr_back.emr_ex_lab_item",
            "parent_table": "emr_back.emr_ex_lab",
            "join_field": "ex_lab_id",
            "icon": "🧪",
        },
        "临床检验项目": {
            "item_table": "emr_back.emr_ex_clinical_item",
            "parent_table": "emr_back.emr_ex_clinical",
            "join_field": "ex_clinical_id",
            "icon": "🩺",
        },
    }

    # 使用原生Streamlit侧边栏组件
    with st.sidebar:
        st.markdown("### 📊 数据类型选择")
        data_type = st.radio(
            "选择要分析的数据:",
            list(DATA_TYPES.keys()),
            format_func=lambda x: f"{DATA_TYPES[x]['icon']} {x}",
        )

    # Get current data type configuration
    current_config = DATA_TYPES[data_type]
    item_table = current_config["item_table"]
    parent_table = current_config["parent_table"]
    join_field = current_config["join_field"]
    data_icon = current_config["icon"]

    # 根据数据类型设置父表名称
    if data_type == "医嘱处方项":
        parent_table_name = "医嘱处方"
    elif data_type == "检验项目":
        parent_table_name = "检验工作单"
    else:  # 临床检验项目
        parent_table_name = "临床检验单"

    # 使用原生Streamlit标签页
    st.markdown(f"## {data_icon} {data_type}分析")
    tab1, tab2, tab3 = st.tabs(["📊 数据概览", "🔍 数据探索", "📈 按机构统计"])

    # ---------- Overview Page ----------
    with tab1:
        with st.spinner("正在加载数据..."):
            # Get summary statistics
            total_items_query = f"""
            SELECT '{data_type}总数' as "Metric", COUNT(*) as "Count"
            FROM {item_table}
            """

            # 根据数据类型使用不同的父表名称显示
            parent_with_items_query = f"""
            SELECT '有{data_type}的{parent_table_name}' as "Metric", COUNT(*) as "Count"
            FROM {parent_table} p
            INNER JOIN {item_table} i ON p.id = i.{join_field}
            """

            parent_without_items_query = f"""
            SELECT '无{data_type}的{parent_table_name}' as "Metric", COUNT(*) as "Count"
            FROM {parent_table} p
            LEFT JOIN {item_table} i ON p.id = i.{join_field}
            WHERE i.id IS NULL
            """

            valid_items_query = f"""
            SELECT '有效{data_type}' as "Metric", COUNT(*) as "Count"
            FROM {item_table} i
            INNER JOIN {parent_table} p ON i.{join_field} = p.id
            """

            orphaned_items_query = f"""
            SELECT '孤立{data_type}' as "Metric", COUNT(*) as "Count"
            FROM {item_table} i
            LEFT JOIN {parent_table} p ON i.{join_field} = p.id
            WHERE p.id IS NULL
            """

            # 使用进度条提示数据加载
            progress_bar = st.progress(0)

            # 执行查询并更新进度
            result1 = execute_query(total_items_query)
            progress_bar.progress(20)

            result2 = execute_query(parent_with_items_query)
            progress_bar.progress(40)

            result3 = execute_query(parent_without_items_query)
            progress_bar.progress(60)

            result4 = execute_query(valid_items_query)
            progress_bar.progress(80)

            result5 = execute_query(orphaned_items_query)
            progress_bar.progress(100)

            # 移除进度条
            progress_bar.empty()

            # Combine all stats into one dataframe
            combined_stats = pd.concat([result1, result2, result3, result4, result5])
            metrics_df = combined_stats.set_index("Metric")

            # 使用原生Streamlit子标签页
            overview_tab1, overview_tab2 = st.tabs(["📊 关键指标", "📈 图表分析"])

            with overview_tab1:
                # 使用Streamlit原生指标组件显示数据
                st.subheader("关键数据指标")
                metric_cols = st.columns(len(metrics_df))

                for i, (metric, col) in enumerate(zip(metrics_df.index, metric_cols)):
                    col.metric(
                        label=metric, value=f"{metrics_df.loc[metric, 'Count']:,}"
                    )

            with overview_tab2:
                st.subheader("数据完整性分析")
                st.markdown("下面的图表展示了数据的完整性和关联性情况")

                # Prepare data for pie charts
                parent_data = pd.DataFrame(
                    {
                        "类别": [
                            f"有{data_type}的{parent_table_name}",
                            f"无{data_type}的{parent_table_name}",
                        ],
                        "数量": [
                            metrics_df.loc[
                                f"有{data_type}的{parent_table_name}", "Count"
                            ],
                            metrics_df.loc[
                                f"无{data_type}的{parent_table_name}", "Count"
                            ],
                        ],
                    }
                )

                items_data = pd.DataFrame(
                    {
                        "类别": [f"有效{data_type}", f"孤立{data_type}"],
                        "数量": [
                            metrics_df.loc[f"有效{data_type}", "Count"],
                            metrics_df.loc[f"孤立{data_type}", "Count"],
                        ],
                    }
                )

                # Display charts side by side with improved styling
                chart_col1, chart_col2 = st.columns(2)

                with chart_col1:
                    fig = create_chart(
                        parent_data, "pie", "类别", "数量", f"{parent_table_name}分布"
                    )
                    fig.update_traces(
                        marker=dict(colors=["#3366cc", "#dc3912"]),
                        textinfo="percent+label",
                        textfont_size=12,
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with chart_col2:
                    fig = create_chart(
                        items_data, "pie", "类别", "数量", f"{data_type}分布"
                    )
                    fig.update_traces(
                        marker=dict(colors=["#109618", "#ff9900"]),
                        textinfo="percent+label",
                        textfont_size=12,
                    )
                    st.plotly_chart(fig, use_container_width=True)

                # 使用Streamlit原生下载按钮
                st.download_button(
                    label="📥 下载概览统计数据",
                    data=combined_stats.to_csv(index=False).encode("utf-8"),
                    file_name=f"{data_type}_overview_stats.csv",
                    mime="text/csv",
                )

    # ---------- Data Explorer ----------
    with tab2:
        # 使用原生Streamlit子标签页
        explorer_tab1, explorer_tab2, explorer_tab3 = st.tabs(
            ["🔍 孤立数据查询", "❌ 缺失数据查询", "✏️ 自定义查询"]
        )

        with explorer_tab1:
            st.subheader(f"孤立{data_type}查询")
            st.markdown(
                f"查询无关联{parent_table_name}的{data_type}记录，最多显示1000条"
            )

            # 根据数据类型创建不同的查询
            if data_type == "医嘱处方项":
                query = f"""
                SELECT 
                    i.id AS 项目ID,
                    i.order_id AS 医嘱处方ID,
                    i.drug_code AS 药品代码,
                    i.drug_name AS 药品名称,
                    i.drug_specifications AS 药品规格,
                    i.drug_dosage_code AS 剂量代码,
                    i.drug_dosage_unit_code AS 剂量单位代码,
                    i.drug_dosage_unit_name AS 剂量单位名称,
                    i.drug_dosage_total AS 总剂量,
                    i.tcm_prescription AS 中药处方,
                    i.tcm_number AS 中药编号,
                    i.tcm_decoction_method AS 中药煎煮方法,
                    i.tcm_use_method AS 中药使用方法,
                    i.operator_id AS 操作员ID,
                    i.operation_time AS 操作时间,
                    i.invalid_flag AS 无效标志,
                    i.data_status AS 数据状态,
                    i.create_date AS 创建日期
                FROM {item_table} i
                LEFT JOIN {parent_table} p ON i.{join_field} = p.id
                WHERE p.id IS NULL
                LIMIT 1000
                """
            elif data_type == "检验项目":  # 检验项目
                query = f"""
                SELECT 
                    i.id AS 项目ID,
                    i.ex_lab_id AS 检验工作单ID,
                    i.lab_item_code AS 检验项目代码,
                    i.lab_item_name AS 检验项目名称,
                    i.item_result AS 检验结果,
                    i.item_unit AS 结果单位,
                    i.item_result_flag AS 结果标志,
                    i.reference_range AS 参考范围,
                    i.critical_value_flag AS 危急值标志,
                    i.operator_id AS 操作员ID,
                    i.operation_time AS 操作时间,
                    i.invalid_flag AS 无效标志,
                    i.data_status AS 数据状态,
                    i.create_date AS 创建日期
                FROM {item_table} i
                LEFT JOIN {parent_table} p ON i.{join_field} = p.id
                WHERE p.id IS NULL
                LIMIT 1000
                """
            else:  # 临床检验项目
                query = f"""
                SELECT 
                    i.id AS 项目ID,
                    i.ex_clinical_id AS 临床检验单ID,
                    i.clinical_item_code AS 检验项目代码,
                    i.clinical_item_name AS 临床检验项目名称,
                    i.item_result AS 检验结果值,
                    i.item_unit AS 检验单位,
                    i.item_method AS 检验方法,
                    i.item_device AS 检验设备,
                    i.item_result_flag AS 结果标志,
                    i.operator_id AS 操作员ID,
                    i.operation_time AS 操作时间,
                    i.invalid_flag AS 无效标志,
                    i.data_status AS 数据状态,
                    i.create_date AS 创建日期
                FROM {item_table} i
                LEFT JOIN {parent_table} p ON i.{join_field} = p.id
                WHERE p.id IS NULL
                LIMIT 1000
                """

            # 执行按钮
            query_button = st.button("执行孤立数据查询", key="orphaned_query")

            if query_button:
                with st.spinner("正在查询..."):
                    df = execute_query(query)

                    if not df.empty:
                        st.success(f"查询成功，共找到 {len(df)} 条记录")
                        st.dataframe(df)

                        # 提供下载选项
                        st.download_button(
                            label=f"📥 下载孤立{data_type}数据",
                            data=df.to_csv(index=False).encode("utf-8"),
                            file_name=f"orphaned_{data_type}.csv",
                            mime="text/csv",
                        )
                    else:
                        st.info("未找到孤立数据")

        with explorer_tab2:
            st.subheader(f"缺失{data_type}的{parent_table_name}查询")
            st.markdown(
                f"查询没有关联{data_type}的{parent_table_name}记录，最多显示1000条"
            )

            # 根据数据类型创建不同的查询
            if data_type == "医嘱处方项":
                query = f"""
                SELECT 
                    p.id AS 医嘱处方ID,
                    p.patient_id AS 患者ID,
                    p.patient_name AS 患者姓名,
                    p.activity_type_name AS 活动类型,
                    p.prescription_no AS 处方号,
                    p.prescription_type_code AS 处方类型,
                    p.prescription_issuance_date AS 处方开具日期,
                    p.org_code AS 机构代码,
                    p.org_name AS 机构名称,
                    p.dept_name AS 科室名称,
                    p.create_date AS 创建日期
                FROM {parent_table} p
                LEFT JOIN {item_table} i ON p.id = i.{join_field}
                WHERE i.id IS NULL
                LIMIT 1000
                """
            elif data_type == "检验项目":  # 检验项目
                query = f"""
                SELECT 
                    p.id AS 检验工作单ID,
                    p.patient_id AS 患者ID,
                    p.patient_name AS 患者姓名, 
                    p.apply_dept_name AS 申请科室,
                    p.sample_type_name AS 标本类型,
                    p.lab_apply_no AS 检验申请单号,
                    p.apply_time AS 申请时间,
                    p.report_time AS 报告时间,
                    p.org_code AS 机构代码,
                    p.org_name AS 机构名称,
                    p.create_date AS 创建日期
                FROM {parent_table} p
                LEFT JOIN {item_table} i ON p.id = i.{join_field}
                WHERE i.id IS NULL
                LIMIT 1000
                """
            else:  # 临床检验项目
                query = f"""
                SELECT 
                    p.id AS 临床检验单ID,
                    p.patient_id AS 患者ID,
                    p.patient_name AS 患者姓名,
                    p.clinical_type_name AS 检验类型,
                    p.application_date AS 申请日期,
                    p.clinical_apply_no AS 检验申请单号,
                    p.apply_dept_name AS 申请科室,
                    p.result_date AS 结果日期,
                    p.org_code AS 机构代码,
                    p.org_name AS 机构名称,
                    p.create_date AS 创建日期
                FROM {parent_table} p
                LEFT JOIN {item_table} i ON p.id = i.{join_field}
                WHERE i.id IS NULL
                LIMIT 1000
                """

            # 执行按钮
            query_button = st.button("执行缺失数据查询", key="missing_query")

            if query_button:
                with st.spinner("正在查询..."):
                    df = execute_query(query)

                    if not df.empty:
                        st.success(f"查询成功，共找到 {len(df)} 条记录")
                        st.dataframe(df)

                        # 提供下载选项
                        st.download_button(
                            label=f"📥 下载缺失{data_type}的{parent_table_name}数据",
                            data=df.to_csv(index=False).encode("utf-8"),
                            file_name=f"missing_{data_type}.csv",
                            mime="text/csv",
                        )
                    else:
                        st.info("未找到缺失数据")

        with explorer_tab3:
            st.subheader("自定义SQL查询")
            st.markdown("在下方编辑框中输入SQL查询语句，然后点击执行按钮")

            # Prepare default query with the selected data type
            if data_type == "医嘱处方项":
                default_query = f"""
                SELECT 
                    i.id AS 项目ID,
                    i.order_id AS 医嘱处方ID,
                    i.drug_name AS 药品名称,
                    p.patient_name AS 患者姓名,
                    p.org_name AS 机构名称
                FROM {item_table} i
                JOIN {parent_table} p ON i.{join_field} = p.id
                LIMIT 100
                """
            elif data_type == "检验项目":  # 检验项目
                default_query = f"""
                SELECT 
                    i.id AS 项目ID,
                    i.ex_lab_id AS 医嘱处方ID,
                    i.lab_item_name AS 检验项目名称,
                    p.patient_name AS 患者姓名,
                    p.org_name AS 机构名称
                FROM {item_table} i
                JOIN {parent_table} p ON i.{join_field} = p.id
                LIMIT 100
                """
            else:  # 临床检验项目
                default_query = f"""
                SELECT 
                    i.id AS 项目ID,
                    i.ex_clinical_id AS 临床检验单ID,
                    i.clinical_item_name AS 临床检验项目名称,
                    p.patient_name AS 患者姓名,
                    p.org_name AS 机构名称
                FROM {item_table} i
                JOIN {parent_table} p ON i.{join_field} = p.id
                LIMIT 100
                """

            query = st.text_area("SQL查询:", default_query, height=200)
            custom_query_button = st.button("执行自定义查询", key="custom_query")

            if custom_query_button:
                with st.spinner("正在执行查询..."):
                    df = execute_query(query)

                    if not df.empty:
                        st.success(f"查询成功，共返回 {len(df)} 条记录")
                        st.dataframe(df)

                        # Show stats for numerical columns with improved UI
                        numeric_cols = df.select_dtypes(include=["number"]).columns
                        if len(numeric_cols) > 0:
                            with st.expander("数值字段统计信息"):
                                st.dataframe(df[numeric_cols].describe())

                        # 提供下载选项
                        st.download_button(
                            label="📥 下载查询结果",
                            data=df.to_csv(index=False).encode("utf-8"),
                            file_name="custom_query_results.csv",
                            mime="text/csv",
                        )
                    else:
                        st.info("查询未返回任何结果")

    # ---------- Organization Analysis ----------
    with tab3:
        st.subheader(f"按机构统计{data_type}缺失情况")
        st.markdown("此页面展示各机构缺失的数据统计信息")

        # Get missing items by organization
        missing_by_org_query = f"""
        SELECT p.org_name as "机构名称", COUNT(*) as "缺失数量"
        FROM {parent_table} p
        LEFT JOIN {item_table} i ON p.id = i.{join_field}
        WHERE i.id IS NULL
        GROUP BY p.org_name
        ORDER BY "缺失数量" DESC
        """

        with st.spinner("正在加载数据..."):
            missing_by_org = execute_query(missing_by_org_query)

            if not missing_by_org.empty:
                # 显示摘要指标
                summary_col1, summary_col2, summary_col3 = st.columns(3)
                with summary_col1:
                    st.metric("存在缺失的机构数", f"{len(missing_by_org):,}")
                with summary_col2:
                    total_missing = missing_by_org["缺失数量"].sum()
                    st.metric("总缺失数量", f"{total_missing:,}")
                with summary_col3:
                    avg_missing = missing_by_org["缺失数量"].mean()
                    st.metric("平均每机构缺失", f"{avg_missing:.2f}")

                # 使用Streamlit原生标签页
                org_tab1, org_tab2 = st.tabs(["📊 图表分析", "📋 详细数据"])

                with org_tab1:
                    # Take top 10 for visualization
                    top_10_orgs = missing_by_org.head(10)

                    st.markdown(f"##### 缺失{data_type}最多的前10个机构")
                    fig = create_chart(
                        top_10_orgs,
                        "bar",
                        "机构名称",
                        "缺失数量",
                        f"缺失{data_type}最多的前10个机构",
                    )
                    # 使用主题色改进图表
                    fig.update_traces(marker_color="#3366cc")
                    fig.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        yaxis_gridcolor="rgba(211,211,211,0.3)",
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # 缺失数量分布直方图
                    st.markdown("##### 缺失数量分布")
                    hist_fig = px.histogram(
                        missing_by_org, x="缺失数量", nbins=20, title="机构缺失数量分布"
                    )
                    hist_fig.update_traces(marker_color="#6699cc")
                    hist_fig.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        xaxis_gridcolor="rgba(211,211,211,0.3)",
                        yaxis_gridcolor="rgba(211,211,211,0.3)",
                    )
                    st.plotly_chart(hist_fig, use_container_width=True)

                with org_tab2:
                    # 简化筛选和分页控件
                    filter_col1, filter_col2 = st.columns([3, 1])
                    with filter_col1:
                        search_term = st.text_input(
                            "按机构名称筛选:", placeholder="输入机构名称关键词"
                        )
                    with filter_col2:
                        rows_per_page = st.selectbox("每页显示:", [10, 25, 50, 100])

                    # 应用筛选
                    if search_term:
                        filtered_data = missing_by_org[
                            missing_by_org["机构名称"].str.contains(
                                search_term, case=False
                            )
                        ]
                    else:
                        filtered_data = missing_by_org

                    # 分页设置
                    total_pages = max(1, (len(filtered_data) - 1) // rows_per_page + 1)
                    page_num = 1

                    if total_pages > 1:
                        page_col1, page_col2 = st.columns([3, 1])
                        with page_col1:
                            page_num = st.slider("页码", 1, total_pages, 1)
                        with page_col2:
                            st.text(f"共 {total_pages} 页")

                    # 数据显示范围
                    start_idx = (page_num - 1) * rows_per_page
                    end_idx = min(start_idx + rows_per_page, len(filtered_data))

                    # 显示表格数据
                    st.dataframe(filtered_data.iloc[start_idx:end_idx])
                    st.text(
                        f"显示 {start_idx+1}-{end_idx} 行，共 {len(filtered_data)} 行"
                    )

                    # 提供下载选项
                    st.download_button(
                        label="📥 下载按机构统计的缺失项数据",
                        data=missing_by_org.to_csv(index=False).encode("utf-8"),
                        file_name=f"{data_type}_missing_by_organization.csv",
                        mime="text/csv",
                    )
            else:
                st.info(f"未找到{data_type}缺失数据")
