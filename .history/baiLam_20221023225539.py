from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

import dash_bootstrap_components as dbc

# TẢI DỮ LIỆU TỪ FIRESTORE
cred = credentials.Certificate("./C:\Users\HP\Downloads\BÀI TH2\BÀI TH2\iuh-20025251-sales\iuh-20025251-933bd-firebase-adminsdk-j7n0e-5d3c9237a0.json")
app = firebase_admin.initialize_app(cred)
dbFireStore = firestore.client()

queryResults = list(dbFireStore.collection(u'tbl_20023851').stream())
listQueryResults = list(map(lambda x : x.to_dict(), queryResults))
df = pd.DataFrame(listQueryResults)



# doc file off
# df = pd.read_csv('orginal_sales_data_edit.csv',
#                  encoding="utf-8", header=0, decimal=',')

df["YEAR_ID"] = df["YEAR_ID"].astype("str")
df["QTR_ID"] = df["QTR_ID"].astype("str")
df["SALES"] = df["SALES"].astype("float")
df["QUANTITYORDERED"] = df["QUANTITYORDERED"].astype("float")
df["PRICEEACH"] = df["PRICEEACH"].astype("float")


df["LoiNhuan"] = df["SALES"] - (df["QUANTITYORDERED"] * df["PRICEEACH"])
dfGroup = df.groupby("YEAR_ID").sum()
dfGroup["YEAR_ID"] = dfGroup.index


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, '../assets/style.css'])
server = app.server
app.title = "Finance Data Analysis"

# Doanh số bán hàng theo năm
figDoanhSoBanHangTheoNam = px.bar(dfGroup, x='YEAR_ID', y="SALES",
                                  title='Doanh số bán hàng theo năm', color='YEAR_ID',
                                  labels={ 'SALES': 'Doanh số'})
# Lợi nhuận bán hàng theo năm
figLoiNhuanBanHangTheoNam = px.line(dfGroup, x='YEAR_ID', y="LoiNhuan",
                                    title='Lợi nhuận bán hàng theo năm',
                                    labels={
                                        'YEAR_ID':'Năm', 'LoiNhuan':'Lợi nhuận'
                                    }
                                    
                                    )

# Tỉ lệ đóng góp của doanh số theo từng danh mục trong từng năm
figTileDoanhSo = px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='SALES',
                             color='SALES',
                             labels={'parent': 'Năm', 'id': 'Year / month','SALES': 'Doanh số'},
                             title='Tỉ lệ đóng góp của doanh số theo từng danh mục trong từng năm')

# Tỉ lệ đóng góp của lợi nhuận theo từng danh mục trong từng năm
figTileLoiNhuan = px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='LoiNhuan',
                              color='LoiNhuan',
                              labels={'parent': 'Năm', 'id': 'Year / month', 'LoiNhuan': 'Lợi nhuận'},
                              title='Tỉ lệ đóng góp của lợi nhuận theo từng danh mục trong từng năm')

# Doanh số
doanhso = round(df["SALES"].sum(), 2) 
# Lợi nhuận
loinhuan = round(df['LoiNhuan'].sum(), 2)

# Top doanh số
topDoanhSo = df.groupby('CATEGORY').sum()['SALES'].max()

# Top lợi nhuận
topLoiNhuan =df.groupby('CATEGORY').sum()['LoiNhuan'].max()


app.layout = dbc.Container(
    children=[
        html.Div(
            className="row",
            children=[
                html.Nav(
                    className="col-12 title-table navbar navbar-light bg-info text-center mb-0",
                    children=html.H2(
                        children=["DANH MỤC SẢN PHẨM TIỀM NĂNG",

                                  html.Br(), html.H5(
                                      children="IUH - Nguyễn Duy Tài - 20023851"
                                  )
                                  ],
                        className="col-12 navbar-brand text-center mb-0"
                    )
                ),

                html.Div(
                    className="row g-2 p-0 m-0",
                    children=[
                        html.Div(
                            className=" col col-md-3 col-sm-12 shadow  bg-body rounded border border-width-2 p-2",
                            children=["Doanh số bán hàng",
                                      html.Br(), html.H3(
                                          children=[doanhso, "$"]
                                      )
                                      ]
                        ),
                        html.Div(
                            className=" col col-md-3 col-sm-12 shadow  bg-body rounded border border-width-2 p-2",
                            children=["Lợi nhuận thu được",
                                      html.Br(), html.H3(
                                          children=[loinhuan, "$"]
                                      )]
                        ),
                        html.Div(
                            className=" col col-md-3 col-sm-12 shadow  bg-body rounded border border-width-2 p-2",
                            children=["Top doanh số",
                                      html.Br(), html.H3(
                                          children=[topDoanhSo, "$"]
                                      )]
                        ),
                        html.Div(
                            className=" col col-md-3 col-sm-12 shadow  bg-body rounded border border-width-2 p-2",
                            children=["Top lợi nhuận",
                                      html.Br(), html.H3(
                                          children=[topLoiNhuan, "$"]
                                      )]
                        )
                    ]
                ),

                html.Div(
                    className="row gx-4 gy-2 p-0 m-0",
                    children=[
                        html.Div(
                            className="col-md-6 col-sm-12 shadow  bg-body rounded border border-width-2",
                            children=[
                                html.Div(
                                    children=dcc.Graph(
                                        id='figDoanhSoBanHangTheoNam-graph',
                                        figure=figDoanhSoBanHangTheoNam),
                                    className="mycard"
                                ),
                            ]
                        ),
                        html.Div(
                            className="col-md-6 col-sm-12 shadow  bg-body rounded border border-width-2",
                            children=[
                                html.Div(
                                    children=dcc.Graph(
                                        id='figTileDoanhSo-graph',
                                        figure=figTileDoanhSo),
                                    className="mycard"
                                ),
                            ]
                        ),
                        html.Div(
                            className="col-md-6 col-sm-12 shadow  bg-body rounded border border-width-2",
                            children=[
                                html.Div(
                                    children=dcc.Graph(
                                        id='figLoiNhuanBanHangTheoNam-graph',
                                        figure=figLoiNhuanBanHangTheoNam),
                                    className="mycard"
                                ),
                            ]
                        ),
                        html.Div(
                            className="col-md-6 col-sm-12 shadow  bg-body rounded border border-width-2",
                            children=[
                                html.Div(
                                    children=dcc.Graph(
                                        id='figTileLoiNhuan-graph',
                                        figure=figTileLoiNhuan),
                                    className="mycard"
                                )
                            ]

                        )
                    ]
                )

            ]
        )
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)
