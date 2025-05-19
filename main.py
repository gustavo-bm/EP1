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
