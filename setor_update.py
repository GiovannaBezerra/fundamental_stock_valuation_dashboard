# Script to update Setores e Subsetores Table by company:

# Import modules:
import pandas as pd
import fundamentus

# Get data frame with indicators by ticker:
df_kpis = fundamentus.get_resultado()
df_kpis['ticker'] = df_kpis.axes[0]

# Create data frame with ticker, nome, setor e subsetor by company:
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

df_setor = pd.DataFrame(list(zip(ticker,empresa,setor,subsetor)),
                        columns = ['ticker','empresa','setor','subsetor'])

# Save the table on excel file:
file_name = 'setor_table.xlsx'
df_setor.to_excel(file_name,index = False)

# Print successful execution:
print('setor_update.py run successful')