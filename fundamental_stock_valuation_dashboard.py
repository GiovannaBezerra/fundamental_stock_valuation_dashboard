#FUNDAMENTAL STOCK VALUATION DASHBOARD

#Objetivos:
#1. Obter os dados do site Fundamentus por meio de uma API: https://www.fundamentus.com.br/
#2. Separar as empresas (tikers) por setor e subsetor
#3. Criar a média por indicador, por subsetor
#4. Criar painel mostrando a comparação entre cada ticker e a média por setor
#5. Criar painel de avaliação de metas por indicador/ticker ~ ranking
#6. importante colocar a data em que estamos vendo o dash?
#7. Guardar histórico para criar métricas de evolução temporal?

#Filtro de subsetor
#Filtro por empresa (ou ticker)
#Botao de atualizar tabela de subsetor

#1 gráfico por indicador com o comparativo com a média por subsetor
#tabela resumo usando o go.Table()
#input do usuário para setar metas por indicador e por setor


#Readme:
#Instalar o fundamentus API: pip install fundamentus
#Instalar o plotly
#Instalar o dash


#Import modules:
import pandas as pd
import fundamentus

# Run script setor_update.py to update Setores e Subsetores Table by company:
trigger = False
if trigger is True:
    exec(open('setor_update.py').read())

# Read table setor_table.xlsx:
df_setor = pd.read_excel('setor_table.xlsx')

print(df_setor.head())

# Obter um data frame com os indicadores por ticker:
df_kpis = fundamentus.get_resultado()
df_kpis['ticker'] = df_kpis.axes[0]

# Juntar todas as informações em um único data frame:
df_result = pd.merge(df_kpis, df_setor, on='ticker')

# Create indicators mean data frame:
df_mean = df_result.groupby('subsetor')[['cotacao', 'pl', 'pvp', 'psr', 'dy', 'pa', 'pcg', 'pebit', 'pacl',
       'evebit', 'evebitda', 'mrgebit', 'mrgliq', 'roic', 'roe', 'liqc',
       'liq2m', 'patrliq', 'divbpatr', 'c5y', 'ticker']].mean()

print(df_mean.head())

print(df_mean.loc[df_mean.axes[0] == "Acessórios"])


#https://www.delftstack.com/pt/howto/python/python-run-another-python-script/
#https://www.youtube.com/watch?v=aS64PvDqCbU
#https://andersonmdcanteli.github.io/Dashboards-com-Plotly-Express-Parte-2/


