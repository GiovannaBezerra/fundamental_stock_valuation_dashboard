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
from dash import Dash, html, dcc, Input, Output
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

# Run script setor_update.py to update Setores e Subsetores Table by company:
trigger = False
if trigger is True:
    exec(open('setor_update.py').read())

# Read table setor_table.xlsx:
df_setor = pd.read_excel('setor_table.xlsx')

# Obter um data frame com os indicadores por ticker:
df_kpis = fundamentus.get_resultado()
df_kpis['ticker'] = df_kpis.axes[0]

# Juntar todas as informações em um único data frame:
df = pd.merge(df_kpis, df_setor, on='ticker')

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
    fig.add_trace(go.Scatter(x=dataframe.ticker, y=dataframe[indicador], marker_color='LightSkyBlue', mode='markers', name='empresas'))
    fig.add_trace(go.Scatter(x=dataframe.ticker, y=line_mean(indicador,dataframe), line_color='red', mode='lines', name='média'))
    fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
    fig.update_layout(title=indicador)
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

df_table = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')

def generate_table(dataframe, max_rows=5):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

# LAY OUT DASH:
app.layout = dbc.Container(html.Div(
    [
        dbc.Row(html.Div(html.Header('FUNDAMENTAL STOCK VALUATION DASHBOARD')),
                style={'color':'gray','fontSize':48,'marginTop':50,'marginBotton':150}
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(html.H1('Some comments'),),style={'color': 'black',"width":"100%"},width='auto',align='start'),#olhar https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/  
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(dcc.Dropdown(subsetores,value="Todos os subsetores",id='drop-subsetores')),width=9,align='start'),
                dbc.Col(html.Div([
                    html.Button('Atualizar tabelas',id='button_atualizar_tabelas', n_clicks=0),
                    html.P('Atualizar tabela de setores e subsetores')]),style={"width":"100%"},width=3,align='end')
            ],justify='between',style={'marginBottom':50, 'marginTop':50}
        ),
        dbc.Row(
            html.Div([
            html.H4(children='Tabela Resumo'),
            generate_table(df_table)
            ]), style={'marginBottom':50, 'marginTop':50}
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([html.H4(children='Cotação',style={'textAlign': 'center'}),dcc.RangeSlider(0,10,1, value=[1,2], id='slider_cotacao')])),
                dbc.Col(html.Div([html.H4(children='P/L',style={'textAlign': 'center'}),dcc.RangeSlider(0,10,1, value=[1,2], id='slider_pl')]))
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(dcc.Graph(id='graph_cotacao', figure=fig_cotacao))),
                dbc.Col(html.Div(dcc.Graph(id='graph_pl', figure=fig_pl)))

            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([html.H4(children='P/VP',style={'textAlign': 'center'}),dcc.RangeSlider(0,10,1, value=[1,2], id='slider_pvp')])),
                dbc.Col(html.Div([html.H4(children='PSR',style={'textAlign': 'center'}),dcc.RangeSlider(0,10,1, value=[1,2], id='slider_psr')]))
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(dcc.Graph(id='graph_pvp', figure=fig_pvp))),
                dbc.Col(html.Div(dcc.Graph(id='graph_psr', figure=fig_psr)))

            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div([html.H4(children='Div.Yield',style={'textAlign': 'center'}),dcc.RangeSlider(0,10,1, value=[1,2], id='slider_dy')])),
                dbc.Col(html.Div([html.H4(children='P/Ativo',style={'textAlign': 'center'}),dcc.RangeSlider(0,10,1, value=[1,2], id='slider_pa')]))
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(dcc.Graph(id='graph_dy', figure=fig_dy))),
                dbc.Col(html.Div(dcc.Graph(id='graph_pa', figure=fig_pa)))

            ]
        ),
    ]
)
)

# DASH CALLBACKS:
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





if __name__ == '__main__':
    app.run_server(debug=True)

