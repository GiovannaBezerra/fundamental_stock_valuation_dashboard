#FUNDAMENTAL STOCK VALUATION DASHBOARD

#Objetivos:
#1. Obter os dados do site Fundamentus por meio de uma API: https://www.fundamentus.com.br/
#2. Separar as empresas (tikers) por setor e subsetor
#3. Criar a média por indicador, por subsetor
#4. Criar painel mostrando a comparação entre cada ticker e a média por setor
#5. Criar painel de avaliação de metas por indicador/ticker ~ ranking
#6. importante colocar a data em que estamos vendo o dash?
#7. Guardar histórico para criar métricas de evolução temporal?


#tabela resumo usando o go.Table()
#callbacks linkando o input do usuário para setar metas por indicador e por setor


#Readme:
#Instalar o fundamentus API: pip install fundamentus
#Instalar o plotly
#Instalar o dash
#Instalar o dash_bootstrap_components

#Import modules:
import pandas as pd
import fundamentus
from dash import Dash, html, dcc, dash_table, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go


# Adding External CSS/JavaScript:

# external JavaScript files
external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]


app = Dash(__name__,external_scripts=external_scripts,external_stylesheets=external_stylesheets)


# Read table setor_table.xlsx:
df_setor = pd.read_excel('setor_table.xlsx')

# Obter um data frame com os indicadores por ticker:
df_kpis = fundamentus.get_resultado()
df_kpis['ticker'] = df_kpis.axes[0]

# Juntar todas as informações em um único data frame:
df = pd.merge(df_kpis, df_setor, on='ticker')

# Reordenando as colunas do data frame:
df = df[['ticker', 'empresa', 'setor','subsetor','cotacao', 'pl', 'pvp', 
         'psr', 'dy', 'pa', 'pcg', 'pebit', 'pacl','evebit', 'evebitda',
         'mrgebit', 'mrgliq', 'roic', 'roe', 'liqc',
         'liq2m', 'patrliq', 'divbpatr', 'c5y', ]]

# Padronizando o conteudoo do data frame para 4 casas decimais:
df = df.round(4)


# Funçao apoio para criar linha média no gráfico:
def line_mean(indicador,dataframe):
    x=[]
    for i in range(len(df)):
        x.append(dataframe[indicador].mean())
    return x

# Lista de subsetores:
subsetores = ["Todos os subsetores"]
lista_subsetores = df.subsetor.dropna().unique().tolist()
lista_subsetores.sort() 
for k in lista_subsetores:
    subsetores.append(k)

# Gráficos:
# Função para construir os gráficos por indicador:
def graph_build(dataframe,indicador):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe.ticker, y=dataframe[indicador], marker_color='LightBlue', marker_size=10, mode='markers', name='empresas'))
    fig.add_trace(go.Scatter(x=dataframe.ticker, y=line_mean(indicador,dataframe), line_color='salmon', line_dash="dot", mode='lines', name='média'))
    fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
    fig.update_layout(title=indicador,plot_bgcolor='lavender')
    return fig

# Gráficos por indicador
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

# Tabela resultado:
# Função para gerar a tabela:
#def table_build(dataframe):
    #fig = go.Figure(data=[go.Table(
       # header=dict(values=list(dataframe.columns),fill_color='grey',align='center'),
        #cells=dict(values=[dataframe.ticker, dataframe.empresa, dataframe.setor, dataframe.subsetor, dataframe.cotacao, dataframe.pl,
        #dataframe.pvp, dataframe.psr,dataframe.dy, dataframe.pa, dataframe.pcg, dataframe.pebit, dataframe.pacl, dataframe.evebit, 
        #dataframe.evebitda, dataframe.mrgebit,dataframe.mrgliq, dataframe.roic, dataframe.roe,dataframe.liqc, dataframe.liq2m, 
        #dataframe.patrliq, dataframe.divbpatr, dataframe.c5y],fill_color='lavender',align='center'),
        #columnwidth=[100])])
   # return fig

#table_summary = table_build(df)

# LAY OUT DASH:
app.layout = dbc.Container(html.Div(
    [
        dbc.Row(html.Div(html.Header('FUNDAMENTAL STOCK VALUATION DASHBOARD')),
                style={'color':'gray','fontSize':48,'marginTop':50,'marginBotton':150}
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(html.H1('Some comments')),style={'fontSize':22,'color':'LightGray'},width='auto'),#olhar https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/  
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(dcc.Dropdown(subsetores,value="Todos os subsetores",id='drop-subsetores',style={'backgroundColor':'LightBlue','fontSize':14})),width=8),
                dbc.Col(html.Div([
                    html.Button('Atualizar',id='button_atualizar', n_clicks=0,style={'backgroundColor':'LightBlue','fontSize':14}),
                    html.P('Atualizar tabela de setores e subsetores',style={'fontSize':12,'color':'Gray'}),
                    html.Div(id='output_atualizar')
                    ]),width=2),
                dbc.Col(html.Div([
                    html.Button('Exportar',id='button_exportar', n_clicks=0, style={'backgroundColor':'LightBlue','fontSize':14}),
                    html.P('Exportar arquivo excel (.xlsx)',style={'fontSize':12,'color':'Gray'}),
                    html.Div(id='output_exportar')
                    ]),width=2),
            ],class_name="g-0",style={'marginBottom':50, 'marginTop':50}
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
                style_cell={'fontSize':14,'textAlign':'center','height':'auto','minWidth': '140px', 'width': '140px', 'maxWidth': '140px','whiteSpace': 'normal'},
                style_header={'color':'gray','fontSize':16,'fontWeight':'bold','backgroundColor':'LightBlue','border':'1px solid white'},
                style_data={'backgroundColor':'lavender','border':'1px solid white'}
                )
            ]), style={'marginBottom':50, 'marginTop':50}
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([html.H4(children='Cotação',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),dcc.Graph(id='graph_cotacao', figure=fig_cotacao)])),
                dbc.Col(html.Div([html.H4(children='P/L',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),dcc.Graph(id='graph_pl', figure=fig_pl)]))
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([html.H4(children='P/VP',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),dcc.Graph(id='graph_pvp', figure=fig_pvp)])),
                dbc.Col(html.Div([html.H4(children='PSR',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),dcc.Graph(id='graph_psr', figure=fig_psr)]))
            ]
        ),       
        dbc.Row(
            [
                dbc.Col(html.Div([html.H4(children='Div. Yield',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),dcc.Graph(id='graph_dy', figure=fig_dy)])),
                dbc.Col(html.Div([html.H4(children='P/Ativo',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),dcc.Graph(id='graph_pa', figure=fig_pa)]))
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([html.H4(children='P/Cap. Giro',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),dcc.Graph(id='graph_pcg', figure=fig_pcg)])),
                dbc.Col(html.Div([html.H4(children='P/EBIT',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),dcc.Graph(id='graph_pebit', figure=fig_pebit)]))
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([html.H4(children='P/Ativo Circ. Liq.',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),dcc.Graph(id='graph_pacl', figure=fig_pacl)])),
                dbc.Col(html.Div([html.H4(children='EV/EBIT',style={'fontSize':22,'color':'Gray','textAlign': 'center'}),dcc.Graph(id='graph_evebit', figure=fig_evebit)]))
            ]
        ),


    ]
)
)

# DASH CALLBACKS:

# Chama a atualização do script de atualização da tabela de setores e subsetores:
@app.callback(
    Output('output_atualizar','children'),
    Input('button_atualizar','n_clicks')
)
def update_output(n_clicks):
    if  n_clicks == 1:
        exec(open('setor_update.py').read()) # Run script setor_update.py to update Setores e Subsetores Table by company

# Chama o export excel:
@app.callback(
    Output('output_exportar','children'),
    Input('button_exportar','n_clicks')
)
def update_output(n_clicks):
    if n_clicks == 1:
        file_name = 'table_export.xlsx'
        df.to_excel(file_name,index = False)


# Atualiza tabela de acordo com o subsetor:
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

# Atualiza gráficos:

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

    











if __name__ == '__main__':
    app.run_server(debug=True)

