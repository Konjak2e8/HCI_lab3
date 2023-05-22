import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import plotly.offline as po
import plotly.graph_objects as pg

# 读取数据
df = pd.read_csv('dataset/black-friday/BlackFriday.csv')
# 按年龄排序，使得绘制的散点图x轴有序
df.sort_values(by=['Age'], inplace=True)

# 载入Dash官方提供的css格式文件
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# 创建Dash应用
app = dash.Dash(__name__, external_stylesheets=stylesheets)

# 用户特征可视化
user_gender_fig = px.pie(df, names='Gender', title='Gender Distribution')
user_city_category_fig = px.pie(df, names='City_Category', title='City Category Distribution')
user_age_fig = px.histogram(df, x='Age', title='Age Distribution')
user_occupation_fig = px.bar(df['Occupation'].value_counts(), title='Occupation Distribution')

# 根据年龄分组，并计算每个年龄段的purchase总额
age_purchase_total = df.groupby('Age')['Purchase'].sum().reset_index()
# 不同年龄段purchase总额的折线图
line_fig = pg.Figure(data=pg.Scatter(x=age_purchase_total['Age'], y=age_purchase_total['Purchase'], mode='lines'))
line_fig.update_layout(title='Purchase Total by Age',
                       xaxis_title='Age',
                       yaxis_title='Purchase Total')


# # 地域特征可视化
# city_category_fig = px.bar(df['City_Category'].value_counts(), title='City Category Distribution')
# city_map_fig = px.scatter_geo(df, locations='City_Category', locationmode='ISO-3', color='Purchase',
#                               hover_name='City_Category', projection='natural earth')

# 用户购买行为可视化
purchase_amount_fig = px.histogram(df, x='Purchase', title='Purchase Amount Distribution')

# 读取一部分数据
df_slice = pd.read_csv('dataset/black-friday/BlackFriday.csv', nrows=5000)
# 按居住年限排序，使得绘制的散点图x轴有序
df_slice.sort_values(by=['Occupation'], inplace=True)

# # 购物数据与居住年限数据的散点图
# scatter_fig = pg.Figure(data=pg.Scatter(x=df_slice['Occupation'], y=df_slice['Purchase'], mode='markers'))
# scatter_fig.update_layout(title=None,
#                           xaxis_title='Occupation',
#                           yaxis_title='Purchase')

# 布局设置
app.layout = html.Div(children=[
    html.H1(children='Black Friday Shopping Data Visualization', style={'textAlign': 'center'}),

    html.H2(children='User Features'),
    dcc.Graph(figure=user_gender_fig),
    dcc.Graph(figure=user_city_category_fig),
    dcc.Graph(figure=user_age_fig),
    dcc.Graph(figure=user_occupation_fig),

    # html.H2(children='Geographical Features'),
    # dcc.Graph(figure=city_category_fig),
    # dcc.Graph(figure=city_map_fig),

    html.H2(children='User Purchase Behavior'),
    dcc.Graph(figure=purchase_amount_fig),

    html.H2(children='Age distribution on Purchase Sum'),
    dcc.Graph(figure=line_fig),

    # html.H2(children='Purchase vs Occupation(first 1000 customers)'),
    # dcc.Graph(figure=scatter_fig),
])

if __name__ == '__main__':
    app.run_server(debug=False, port=8080)
