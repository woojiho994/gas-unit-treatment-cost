import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 页面配置
st.set_page_config(
    page_title="废气单位治理成本数据库",
    page_icon="🏭",
    layout="wide"
)

# 加载数据
@st.cache_data
def load_data():
    df = pd.read_excel('废气处理.xlsx')
    return df

# 主函数
def main():
    st.title("废气单位治理成本数据库")
    
    # 加载数据
    df = load_data()
    
    # 侧边栏筛选器
    st.sidebar.header("数据筛选")
    
    # 地区筛选
    regions = ["全部"] + list(df["地区"].unique())
    selected_region = st.sidebar.selectbox("选择地区", regions)
    
    # 行业筛选
    industries = ["全部"] + list(df["所属行业"].unique())
    selected_industry = st.sidebar.selectbox("选择行业", industries)
    
    # 污染物类型筛选
    pollutants = ["全部"] + list(df["污染物类型"].unique())
    selected_pollutant = st.sidebar.selectbox("选择污染物类型", pollutants)
    
    # 数据筛选
    filtered_df = df.copy()
    if selected_region != "全部":
        filtered_df = filtered_df[filtered_df["地区"] == selected_region]
    if selected_industry != "全部":
        filtered_df = filtered_df[filtered_df["所属行业"] == selected_industry]
    if selected_pollutant != "全部":
        filtered_df = filtered_df[filtered_df["污染物类型"] == selected_pollutant]
    
    # 数据概览
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("平均治理成本", f"¥{filtered_df['单位治理成本（元/吨）'].mean():,.2f}/吨")
    with col2:
        st.metric("最高治理成本", f"¥{filtered_df['单位治理成本（元/吨）'].max():,.2f}/吨")
    with col3:
        st.metric("最低治理成本", f"¥{filtered_df['单位治理成本（元/吨）'].min():,.2f}/吨")
    
    # 数据可视化
    st.header("数据分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 地区平均成本分布
        fig_region = px.bar(
            filtered_df.groupby("地区")["单位治理成本（元/吨）"].mean().reset_index(),
            x="地区",
            y="单位治理成本（元/吨）",
            title="各地区平均治理成本",
            color_discrete_sequence=['lightblue']  # 设置浅蓝色
        )
        st.plotly_chart(fig_region, use_container_width=True)
    
    with col2:
        # 行业平均成本分布
        fig_industry = px.bar(
            filtered_df.groupby("所属行业")["单位治理成本（元/吨）"].mean().reset_index(),
            x="所属行业",
            y="单位治理成本（元/吨）",
            title="各行业平均治理成本",
            color_discrete_sequence=['lightblue']  # 设置浅蓝色
        )
        st.plotly_chart(fig_industry, use_container_width=True)
    
    # 原始数据表格
    st.header("详细数据")
    st.dataframe(
        filtered_df,
        column_config={
            "单位治理成本（元/吨）": st.column_config.NumberColumn(
                "单位治理成本（元/吨）",
                format="¥%.2f"
            )
        },
        hide_index=True,
        use_container_width=True  # 设置表格宽度占满容器
    )
    
    # 数据下载
    csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="下载数据为CSV",
        data=csv,
        file_name="废气治理成本数据.csv",
        mime="text/csv"
    )
    
    # 成本估算功能
    # 成本估算功能
    st.header("成本估算")
    st.write("根据您的行业和污染物类型，deepseek帮你估算治理成本")
    
    # 创建两列布局
    est_col1, est_col2 = st.columns(2)
    
    with est_col1:
        industry_input = st.text_input("请输入行业类型", "")
    
    with est_col2:
        pollutant_input = st.selectbox("请选择污染物类型", options=df["污染物类型"].unique().tolist())
    
    if st.button("获取成本估算"):
        if industry_input and pollutant_input:
            try:
                with st.spinner("正在分析中..."):
                    # 创建成本估算器实例
                    from cost_estimation import CostEstimator
                    estimator = CostEstimator('废气处理.xlsx')
                    result = estimator.get_cost_estimation(industry_input, pollutant_input)
                    # 显示结果
                    st.success("分析完成！")
                    st.subheader("分析结果")
                    st.write(result)
            except Exception as e:
                st.error(f"发生错误: {e}")
        else:
            st.warning("请输入行业类型和污染物类型")

if __name__ == "__main__":
    main() 
