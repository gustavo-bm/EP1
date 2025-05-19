import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 1. Carregar os dados do Excel
file_path = 'Dados coletados - refactoring.xlsx'

# Ler as duas abas
df_coleta = pd.read_excel(file_path, sheet_name='coleta')
df_perfil = pd.read_excel(file_path, sheet_name='perfil dos participantes')

# Juntar os dois dataframes usando a coluna 'ID'
df = pd.merge(df_coleta, df_perfil, on='ID', how='inner')

# Remover colunas desnecessárias
df.drop(columns=['Unnamed: 6', 'Unnamed: 7'], inplace=True, errors='ignore')

print("Dados carregados com sucesso.")

# 2. Estatísticas Descritivas Gerais
desc_stats = df[['Tempo (h)', 'LOC Modificadas', 'Erros Funcionais', 'Problemas de Design']].describe()
print("\Estatísticas Descritivas Gerais:")
print(desc_stats)

# Agrupar por ferramenta
grouped = df.groupby('Ferramenta')[['Tempo (h)', 'LOC Modificadas', 'Erros Funcionais', 'Problemas de Design']].agg(['mean', 'std', 'median'])
print("\Média, Desvio Padrão e Mediana por Ferramenta:")
print(grouped)

# Gráfico Boxplot - Tempo
plt.figure(figsize=(10,6))
sns.boxplot(x='Ferramenta', y='Tempo (h)', data=df)
plt.title('Distribuição do Tempo por Ferramenta')
plt.grid(True)
plt.show()

# Gráfico Countplot - Erros Funcionais
plt.figure(figsize=(10,6))
sns.countplot(data=df, x='Ferramenta', hue='Erros Funcionais')
plt.title('Contagem de Erros Funcionais por Ferramenta')
plt.legend(title='Erros Funcionais')
plt.grid(True)
plt.show()

