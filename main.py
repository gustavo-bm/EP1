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

# 3. Perfil dos Participantes
print("\n🎓 Distribuição por Formação:")
print(df['Formacao'].value_counts())

print("\nDistribuição por Experiência:")
print(df['Experiencia'].value_counts())

print("\n Distribuição por Conhecimento em Java:")
print(df['Conhecimento_Java'].value_counts())

print("\n Distribuição por Conhecimento em Refatoração:")
print(df['Conhecimento_Refatoracao'].value_counts())

# Gráfico de barras para formação
plt.figure(figsize=(10,6))
sns.countplot(y='Formacao', data=df, order=df['Formacao'].value_counts().index)
plt.title('Distribuição de Formações dos Participantes')
plt.xlabel('Quantidade')
plt.ylabel('Formação')
plt.grid(True)
plt.show()

# 4. Tempo de Conclusão das Tarefas
smart_time = df[df['Ferramenta'] == 'SmartRefactor']['Tempo (h)']
trad_time = df[df['Ferramenta'] == 'Tradicional']['Tempo (h)']

# Histograma do tempo por ferramenta
plt.figure(figsize=(10,6))
sns.histplot(data=df, x='Tempo (h)', hue='Ferramenta', bins=20, kde=True)
plt.title('Histograma do Tempo por Ferramenta')
plt.xlabel('Tempo (horas)')
plt.ylabel('Frequência')
plt.grid(True)
plt.show()

# Teste T-Student para Tempo
t_stat, p_val = stats.ttest_ind(smart_time, trad_time, equal_var=False)
print(f"\nTeste T-Student para Tempo:\nt = {t_stat:.4f}, p = {p_val:.4f}")
if p_val < 0.05:
    print("Resultado significativo: há diferença estatística no tempo entre as ferramentas.")
else:
    print("Resultado não significativo: não há diferença estatística no tempo entre as ferramentas.")

# 5. Teste de Hipótese para Erros Funcionais (Mann-Whitney U)
smart_erros = df[df['Ferramenta'] == 'SmartRefactor']['Erros Funcionais']
trad_erros = df[df['Ferramenta'] == 'Tradicional']['Erros Funcionais']

u_stat, u_pval = stats.mannwhitneyu(smart_erros, trad_erros, alternative='two-sided')
print(f"\nTeste Mann-Whitney U para Erros Funcionais:\nU = {u_stat:.2f}, p = {u_pval:.4f}")
if u_pval < 0.05:
    print("Resultado significativo: há diferença estatística no número de erros funcionais entre as ferramentas.")
else:
    print("Resultado não significativo: não há diferença estatística no número de erros funcionais entre as ferramentas.")

# 6. Influência do Perfil dos Participantes

# Mapear experiência para valores numéricos
df['Exp_Num'] = df['Experiencia'].map({
    '< 1 ano': 0.5,
    '1-2 anos': 1.5,
    '3-5 anos': 4,
    '6+ anos': 7
})

# Correlação entre experiência e erros funcionais
corr_erros = df['Exp_Num'].corr(df['Erros Funcionais'], method='spearman')
print(f"\nCorrelação de Spearman entre Experiência e Erros Funcionais: r = {corr_erros:.3f}")

# Boxplot de erros por nível de experiência
plt.figure(figsize=(10,6))
sns.boxplot(x='Experiencia', y='Erros Funcionais', data=df, order=['< 1 ano', '1-2 anos', '3-5 anos', '6+ anos'])
plt.title('Erros Funcionais por Nível de Experiência')
plt.xlabel('Experiência')
plt.ylabel('Erros Funcionais')
plt.grid(True)
plt.show()

# 7. Resumo das Métricas e Ferramentas Usadas
print("""
 Métricas Analisadas:
- Tempo de execução (horas)
- Linhas de Código modificadas (LOC)
- Erros Funcionais
- Problemas de Design

  Testes Estatísticos:
- T-Student (comparação de médias de tempo)
- Mann-Whitney U (comparação de erros funcionais)

Bibliotecas Utilizadas:
- Pandas: manipulação de dados
- Matplotlib / Seaborn: visualizações
- SciPy: testes estatísticos
""")