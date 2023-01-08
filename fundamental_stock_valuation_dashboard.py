#FUNDAMENTAL STOCK VALUATION DASHBOARD

# The program build a dashboard using dash e plotly to analyze fundamental financial data informations by companies listed
# in Brazilian stock market, source: https://www.fundamentus.com.br/).
# The dashboard shows companies by each indicator and the correspondent average. In addition, it's possible downloading to excel file and 
# updating sector and subsector data by demand.

#Import modules:
import pandas as pd
import fundamentus
from dash import Dash, html, dcc, dash_table, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go


# Adding External CSS/JavaScript to customize layout:
# external JavaScript files:
external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }]

# external CSS stylesheets:
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }]


# App Create:
app = Dash(__name__,external_scripts=external_scripts,external_stylesheets=external_stylesheets)


# Get and process data:

# Read table setor_table.xlsx:
df_setor = pd.read_excel('setor_table.xlsx')

# Get data frame indicators by ticker:
df_kpis = fundamentus.get_resultado()
df_kpis['ticker'] = df_kpis.axes[0]

# Combine infos in a data frame: 
df = pd.merge(df_kpis, df_setor, on='ticker')

# Reorder data frame columns:
df = df[['ticker', 'empresa', 'setor','subsetor','cotacao', 'pl', 'pvp', 
         'psr', 'dy', 'pa', 'pcg', 'pebit', 'pacl','evebit', 'evebitda',
         'mrgebit', 'mrgliq', 'roic', 'roe', 'liqc',
         'liq2m', 'patrliq', 'divbpatr', 'c5y', ]]

# Standardize for 4 decimal plates:
df = df.round(4)

# Function to create mean line in visualization graph:
def line_mean(indicador,dataframe):
    x=[]
    for i in range(len(df)):
        x.append(dataframe[indicador].mean())
    return x

# Create subsetores list:
subsetores = ["Todos os subsetores"]
lista_subsetores = df.subsetor.dropna().unique().tolist()
lista_subsetores.sort() 
for k in lista_subsetores:
    subsetores.append(k)

# Graphs:
# Function to build graph by indicator:
def graph_build(dataframe,indicador):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe.ticker, y=dataframe[indicador], marker_color='LightBlue', marker_size=10, mode='markers', name='empresas'))
    fig.add_trace(go.Scatter(x=dataframe.ticker, y=line_mean(indicador,dataframe), line_color='salmon', line_dash="dot", mode='lines', name='média'))
    fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
    fig.update_layout(plot_bgcolor='lavender')
    return fig

# Graphs by indicator:
fig_cotacao = graph_build(df,'cotacao')
fig_pl = graph_build(df,'pl')
fig_pvp = graph_build(df,'pvp')
fig_psr = graph_build(df,'psr')
fig_dy = graph_build(df,'dy')
fig_pa = graph_build(df,'pa')
fig_pcg = graph_build(df,'pcg')
fig_pebit = graph_build(df,'pebit')
fig_pacl = graph_build(df,'pacl')
fig_evebit = graph_build(df,'evebit')
fig_evebitda = graph_build(df,'evebitda')
fig_mrgebit = graph_build(df,'mrgebit')
fig_mrgliq = graph_build(df,'mrgliq')
fig_roic = graph_build(df,'roic')
fig_roe = graph_build(df,'roe')
fig_liqc = graph_build(df,'liqc')
fig_liq2m = graph_build(df,'liq2m')
fig_patrliq = graph_build(df,'patrliq')
fig_divbpatr = graph_build(df,'divbpatr')
fig_c5y = graph_build(df,'c5y')


# Lay out Create:
app.layout = dbc.Container(html.Div(
    [
        dbc.Row(html.Div(html.Header('FUNDAMENTAL STOCK VALUATION DASHBOARD')),
                style={'color':'gray','fontSize':48,'marginTop':50,'marginBotton':100}
        ),
        dbc.Row(
            [
                dcc.Markdown('''
                >
                >## Dashboard para analisar dados de informações financeiras e fundamentalistas das empresas listadas na Bovespa 
                >## disponíveis no site Fundamentos (https://www.fundamentus.com.br/).
                >
                ''')
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(dcc.Dropdown(subsetores,value="Todos os subsetores",id='drop-subsetores',
                    style={'backgroundColor':'LightBlue','fontSize':14})),width=8),
                dbc.Col(html.Div([
                    html.Button('Atualizar',id='button_atualizar', n_clicks=0,
                        style={'backgroundColor':'LightBlue','fontSize':14}),
                    html.P('Atualizar tabela de setores e subsetores',
                        style={'fontSize':12,'color':'Gray'}),
                    html.Div(id='output_atualizar')
                    ]),width=2),
                dbc.Col(html.Div([
                    html.Button('Exportar',id='button_exportar', n_clicks=0, 
                        style={'backgroundColor':'LightBlue','fontSize':14}),
                    html.P('Exportar arquivo excel (.xlsx)',
                        style={'fontSize':12,'color':'Gray'}),
                    html.Div(id='output_exportar')
                    ]),width=2),
            ],class_name="g-1",style={'marginTop':50}
        ),
        dbc.Row(
            html.Div([
            html.H4(children='Tabela Resumo',style={'fontSize':22,'color':'Gray'}),
            dash_table.DataTable(
                data=df.to_dict('records'),columns=[{'name': i, 'id': i} for i in df.columns],
                id='table-summary',
                fixed_rows={'headers':True},
                fixed_columns={'headers': True, 'data': 2},
                style_table={'minWidth': 1100,'maxHeight': 400,'overflowX':'auto','overflowY':'auto'},
                style_cell={'fontSize':14,'textAlign':'center','height':'auto',
                            'minWidth': '140px', 'width': '140px', 'maxWidth': '140px','whiteSpace': 'normal'},
                style_header={'color':'gray','fontSize':16,'fontWeight':'bold','backgroundColor':'LightBlue',
                            'border':'1px solid white'},
                style_data={'backgroundColor':'lavender','border':'1px solid white'}
                )
            ])
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([html.H4(children='Cotação',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),
                dcc.Graph(id='graph_cotacao', figure=fig_cotacao)])),
                dbc.Col(html.Div([html.H4(children='P/L',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),
                dcc.Graph(id='graph_pl', figure=fig_pl)]))
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([html.H4(children='P/VP',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),
                dcc.Graph(id='graph_pvp', figure=fig_pvp)])),
                dbc.Col(html.Div([html.H4(children='PSR',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),
                dcc.Graph(id='graph_psr', figure=fig_psr)]))
            ]
        ),       
        dbc.Row(
            [
                dbc.Col(html.Div([html.H4(children='Div. Yield',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),
                dcc.Graph(id='graph_dy', figure=fig_dy)])),
                dbc.Col(html.Div([html.H4(children='P/Ativo',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),
                dcc.Graph(id='graph_pa', figure=fig_pa)]))
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([html.H4(children='P/Cap. Giro',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),
                dcc.Graph(id='graph_pcg', figure=fig_pcg)])),
                dbc.Col(html.Div([html.H4(children='P/EBIT',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),
                dcc.Graph(id='graph_pebit', figure=fig_pebit)]))
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([html.H4(children='P/Ativo Circ. Liq.',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),
                dcc.Graph(id='graph_pacl', figure=fig_pacl)])),
                dbc.Col(html.Div([html.H4(children='EV/EBIT',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),
                dcc.Graph(id='graph_evebit', figure=fig_evebit)]))
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([html.H4(children='EV/EBITDA',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),
                dcc.Graph(id='graph_evebitda', figure=fig_evebitda)])),
                dbc.Col(html.Div([html.H4(children='Mrg Ebit',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),
                dcc.Graph(id='graph_mrgebit', figure=fig_mrgebit)]))
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([html.H4(children='Mrg Líq',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),
                dcc.Graph(id='graph_mrgliq', figure=fig_mrgliq)])),
                dbc.Col(html.Div([html.H4(children='ROIC',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),
                dcc.Graph(id='graph_roic', figure=fig_roic)]))
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([html.H4(children='ROE',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),
                dcc.Graph(id='graph_roe', figure=fig_roe)])),
                dbc.Col(html.Div([html.H4(children='Líq Corr',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),
                dcc.Graph(id='graph_liqc', figure=fig_liqc)]))
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([html.H4(children='Líq 2 meses',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),
                dcc.Graph(id='graph_liq2m', figure=fig_liq2m)])),
                dbc.Col(html.Div([html.H4(children='Patrim Líq',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),
                dcc.Graph(id='graph_patrliq', figure=fig_patrliq)]))
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([html.H4(children='Dív Brut/Patrim',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),
                dcc.Graph(id='graph_divbpatr', figure=fig_divbpatr)])),
                dbc.Col(html.Div([html.H4(children='Cresc Rec 5a',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),
                dcc.Graph(id='graph_c5y', figure=fig_c5y)]))
            ]
        ),
    ]
)
)

# Dash Callbacks:

# Callback to update Tabela de setores e subsetores:
@app.callback(
    Output('output_atualizar','children'),
    Input('button_atualizar','n_clicks')
)
def update_output(n_clicks):
    if  n_clicks == 1:
        exec(open('setor_update.py').read()) # Run script setor_update.py to update Setores e Subsetores Table by company

# Callback to export excel:
@app.callback(
    Output('output_exportar','children'),
    Input('button_exportar','n_clicks')
)
def update_output(n_clicks):
    if n_clicks == 1:
        file_name = 'table_export.xlsx'
        df.to_excel(file_name,index = False)

# Callback to update table by setor:
@app.callback(
    Output('table-summary','data'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        data=df.to_dict('records')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        data=df_subsetor.to_dict('records')
    return data

# Update graphs by indicator and setor:
@app.callback(
    Output('graph_cotacao','figure'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        fig_cotacao = graph_build(df,'cotacao')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        fig_cotacao = graph_build(df_subsetor,'cotacao')
    return fig_cotacao 

@app.callback(
    Output('graph_pl','figure'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        fig_pl = graph_build(df,'pl')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        fig_pl = graph_build(df_subsetor,'pl')
    return fig_pl 

@app.callback(
    Output('graph_pvp','figure'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        fig_pvp = graph_build(df,'pvp')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        fig_pvp = graph_build(df_subsetor,'pvp')
    return fig_pvp

@app.callback(
    Output('graph_psr','figure'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        fig_psr = graph_build(df,'psr')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        fig_psr = graph_build(df_subsetor,'psr')
    return fig_psr

@app.callback(
    Output('graph_dy','figure'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        fig_dy = graph_build(df,'dy')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        fig_dy = graph_build(df_subsetor,'dy')
    return fig_dy

@app.callback(
    Output('graph_pa','figure'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        fig_pa = graph_build(df,'pa')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        fig_pa = graph_build(df_subsetor,'pa')
    return fig_pa

@app.callback(
    Output('graph_pcg','figure'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        fig_pcg = graph_build(df,'pcg')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        fig_pcg = graph_build(df_subsetor,'pcg')
    return fig_pcg

@app.callback(
    Output('graph_pebit','figure'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        fig_pebit = graph_build(df,'pebit')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        fig_pebit = graph_build(df_subsetor,'pebit')
    return fig_pebit

@app.callback(
    Output('graph_pacl','figure'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        fig_pacl = graph_build(df,'pacl')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        fig_pacl = graph_build(df_subsetor,'pacl')
    return fig_pacl

@app.callback(
    Output('graph_evebit','figure'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        fig_evebit = graph_build(df,'evebit')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        fig_evebit = graph_build(df_subsetor,'evebit')
    return fig_evebit

@app.callback(
    Output('graph_evebitda','figure'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        fig_evebitda = graph_build(df,'evebitda')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        fig_evebitda = graph_build(df_subsetor,'evebitda')
    return fig_evebitda

@app.callback(
    Output('graph_mrgebit','figure'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        fig_mrgebit = graph_build(df,'mrgebit')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        fig_mrgebit = graph_build(df_subsetor,'mrgebit')
    return fig_mrgebit

@app.callback(
    Output('graph_mrgliq','figure'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        fig_mrgliq = graph_build(df,'mrgliq')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        fig_mrgliq = graph_build(df_subsetor,'mrgliq')
    return fig_mrgliq

@app.callback(
    Output('graph_roic','figure'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        fig_roic = graph_build(df,'roic')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        fig_roic = graph_build(df_subsetor,'roic')
    return fig_roic

@app.callback(
    Output('graph_roe','figure'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        fig_roe = graph_build(df,'roe')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        fig_roe = graph_build(df_subsetor,'roe')
    return fig_roe

@app.callback(
    Output('graph_liqc','figure'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        fig_liqc = graph_build(df,'liqc')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        fig_liqc = graph_build(df_subsetor,'liqc')
    return fig_liqc

@app.callback(
    Output('graph_liq2m','figure'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        fig_liq2m = graph_build(df,'liq2m')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        fig_liq2m = graph_build(df_subsetor,'liq2m')
    return fig_liq2m

@app.callback(
    Output('graph_patrliq','figure'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        fig_patrliq = graph_build(df,'patrliq')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        fig_patrliq = graph_build(df_subsetor,'patrliq')
    return fig_patrliq

@app.callback(
    Output('graph_divbpatr','figure'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        fig_divbpatr = graph_build(df,'divbpatr')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        fig_divbpatr = graph_build(df_subsetor,'divbpatr')
    return fig_divbpatr

@app.callback(
    Output('graph_c5y','figure'),
    Input('drop-subsetores','value')
)
def update_output(value):
    if value == 'Todos os subsetores':
        fig_c5y = graph_build(df,'c5y')
    else:
        df_subsetor = df.loc[df['subsetor']==value,:]
        fig_c5y = graph_build(df_subsetor,'c5y')
    return fig_c5y

if __name__ == '__main__':
    app.run_server(debug=True)

