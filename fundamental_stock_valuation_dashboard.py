#FUNDAMENTAL STOCK VALUATION DASHBOARD

#Objetivos:
#1. Obter os dados do site Fundamentus por meio de uma API: https://www.fundamentus.com.br/
#2. Separar as empresas (tikers) por setor e subsetor
#3. Criar a média por indicador, por subsetor
#4. Criar painel mostrando a comparação entre cada ticker e a média por setor
#5. Criar painel de avaliação de metas por indicador/ticker ~ ranking
#6. importante colocar a data em que estamos vendo o dash?
#7. Guardar histórico para criar métricas de evolução temporal?

#Readme:
#Instalar o fundamentus API: pip install fundamentus


#Import modules:
import pandas as pd
import fundamentus

# Obter um data frame com os indicadores por ticker:
df_kpis = fundamentus.get_resultado()
df_kpis['ticker'] = df_kpis.axes[0]

# Criar um data frame de ticker, nome, setor e subsetor por empresa:
ticker = []
empresa = []
setor = []
subsetor = []

for i in range(0,len(df_kpis.axes[0])):
    ticker_name = df_kpis.axes[0][i]
    ticker.append(ticker_name)
    empresa.append(fundamentus.get_papel(ticker_name)['Empresa'][0])
    setor.append(fundamentus.get_papel(ticker_name)['Setor'][0])
    subsetor.append(fundamentus.get_papel(ticker_name)['Subsetor'][0]) 

df_summary = pd.DataFrame(list(zip(ticker,empresa,setor,subsetor)),columns = ['ticker','empresa','setor','subsetor'])

# Juntar todas as informações em um único data frame:
df_result = pd.merge(df_kpis, df_summary, on='ticker')

df_result.groupby('subsetor')[['cotacao','pl','pvp']].mean()



