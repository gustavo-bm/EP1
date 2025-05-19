import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

# Configurações iniciais
grafico_dir = 'graficos'
os.makedirs(grafico_dir, exist_ok=True)
sns.set(style="whitegrid")

# Carregar os dados
def carregar_dados(caminho):
    try:
        df_coleta = pd.read_excel(caminho, sheet_name='coleta')
        df_perfil = pd.read_excel(caminho, sheet_name='perfil dos participantes')

        df = pd.merge(df_coleta, df_perfil, on='ID', how='inner') # transforma para uma tabela só

        df.drop(columns=['Unnamed: 6', 'Unnamed: 7'], inplace=True, errors='ignore') # trata colunas indenvidas
        return df
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return None

# boxplot de variáveis independentes
def plot_boxplot(df, x, y, titulo, nome_arquivo):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=x, y=y, data=df)
    plt.title(titulo)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(True)
    caminho = os.path.join(grafico_dir, nome_arquivo)
    plt.savefig(caminho)
    plt.close()

# contagem  de variáveis independentes
def plot_countplot(df, x, hue, titulo, nome_arquivo):
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x=x, hue=hue)
    plt.title(titulo)
    plt.xlabel(x)
    plt.ylabel('Quantidade')
    plt.legend(title=hue)
    plt.grid(True)
    caminho = os.path.join(grafico_dir, nome_arquivo)

    plt.savefig(caminho)
    plt.close()

# carrega os dados
df = carregar_dados('planilhas/Dados coletados - refactoring.xlsx')
if df is None:
    exit()

print("Dados carregados com sucesso!")

# variaveis independentes
desc_stats = df[['Tempo (h)', 'LOC Modificadas', 'Erros Funcionais', 'Problemas de Design']].describe() # analise descritiva
print("\nEstatísticas Descritivas Gerais:")
print(desc_stats)

# comparação por ferramenta (tradicional vs SmartRefactor); media, dp e mediana
grouped = df.groupby('Ferramenta')[['Tempo (h)', 'LOC Modificadas', 'Erros Funcionais', 'Problemas de Design']].agg(['mean', 'std', 'median'])
print("\nMédia, Desvio Padrão e Mediana por Ferramenta:")
print(grouped)

# chamadas as funcoes de graficos para cada variavel
plot_boxplot(df, 'Ferramenta', 'Tempo (h)', 'Distribuição do Tempo por Ferramenta', 'tempo_por_ferramenta.png')
plot_boxplot(df, 'Ferramenta', 'LOC Modificadas', 'Distribuição de LOC Modificadas por Ferramenta', 'loc_por_ferramenta.png')
plot_boxplot(df, 'Ferramenta', 'Erros Funcionais', 'Distribuição de Erros Funcionais por Ferramenta', 'erros_por_ferramenta.png')
plot_boxplot(df, 'Ferramenta', 'Problemas de Design', 'Distribuição de Problemas de Design por Ferramenta', 'problemas_por_ferramenta.png')

# conta erros funcionais
plot_countplot(df, 'Ferramenta', 'Erros Funcionais', 'Contagem de Erros Funcionais por Ferramenta', 'contagem_erros_funcionais.png')

# distribuicao por Formação, Experiência, Conhecimento
print("\nDistribuição por Formação:")
print(df['Formacao'].value_counts())

print("\nDistribuição por Experiência:")
print(df['Experiencia'].value_counts())

print("\nDistribuição por Conhecimento em Java:")
print(df['Conhecimento_Java'].value_counts())

print("\nDistribuição por Conhecimento em Refatoração:")
print(df['Conhecimento_Refatoracao'].value_counts())

# extra: histograma do tempo por ferramenta
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Tempo (h)', hue='Ferramenta', bins=20, kde=True)
plt.title('Histograma do Tempo por Ferramenta')
plt.xlabel('Tempo (horas)')
plt.ylabel('Frequência')
plt.grid(True)
plt.savefig(os.path.join(grafico_dir, 'histograma_tempo.png'))
plt.close()

# testes estatisticos pedidos
def realizar_teste_t(coluna):
    smart = df[df['Ferramenta'] == 'SmartRefactor'][coluna]
    trad = df[df['Ferramenta'] == 'Tradicional'][coluna]
    t_stat, p_val = stats.ttest_ind(smart, trad, equal_var=False)
    print(f"\nTeste T-Student para {coluna}:")
    print(f"t = {t_stat:.4f}, p = {p_val:.4f}")
    if p_val < 0.05:
        print("Resultado significativo: há diferença estatística entre as ferramentas.")
    else:
        print("Resultado não significativo: não há diferença estatística entre as ferramentas.")

def realizar_teste_mannwhitney(coluna):
    smart = df[df['Ferramenta'] == 'SmartRefactor'][coluna]
    trad = df[df['Ferramenta'] == 'Tradicional'][coluna]
    u_stat, p_val = stats.mannwhitneyu(smart, trad, alternative='two-sided')
    print(f"\nTeste Mann-Whitney U para {coluna}:")
    print(f"U = {u_stat:.2f}, p = {p_val:.4f}")
    if p_val < 0.05:
        print("Resultado significativo: há diferença estatística entre as ferramentas.")
    else:
        print("Resultado não significativo: não há diferença estatística entre as ferramentas.")

# testes
realizar_teste_t('Tempo (h)')
realizar_teste_t('Problemas de Design')
realizar_teste_t('LOC Modificadas')
realizar_teste_mannwhitney('Erros Funcionais')

# relacao entre experiencia e erros funcionais (analise de perfil)
df['Exp_Num'] = df['Experiencia'].map({
    '< 1 ano': 0.5,
    '1-2 anos': 1.5,
    '3-5 anos': 4,
    '6+ anos': 7
})

corr_erros = df['Exp_Num'].corr(df['Erros Funcionais'], method='spearman')
print(f"\nCorrelação de Spearman entre Experiência e Erros Funcionais: r = {corr_erros:.3f}")

# bplotagem  de erros por nível de experiencia
plt.figure(figsize=(10, 6))
sns.boxplot(x='Experiencia', y='Erros Funcionais', data=df, order=['< 1 ano', '1-2 anos', '3-5 anos', '6+ anos'])
plt.title('Erros Funcionais por Nível de Experiência')
plt.xlabel('Experiência')
plt.ylabel('Erros Funcionais')
plt.grid(True)
plt.savefig(os.path.join(grafico_dir, 'erros_por_experiencia.png'))
plt.close()
