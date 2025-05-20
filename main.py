import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import statsmodels.formula.api as smf

# Salvar output em arquivo
output_file = 'resultados_output.txt'
sys.stdout = open(output_file, 'w', encoding='utf-8')

# Configurações iniciais
grafico_dir = 'graficos'
os.makedirs(grafico_dir, exist_ok=True)
sns.set(style="whitegrid")

# Carregar os dados
def carregar_dados(caminho):
    try:
        df_coleta = pd.read_excel(caminho, sheet_name='coleta')
        df_perfil = pd.read_excel(caminho, sheet_name='perfil dos participantes')
        df = pd.merge(df_coleta, df_perfil, on='ID', how='inner')
        df.drop(columns=['Unnamed: 6', 'Unnamed: 7'], inplace=True, errors='ignore')
        return df
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return None

def plot_boxplot(df, x, y, titulo, nome_arquivo):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=x, y=y, data=df)
    plt.title(titulo)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(True)
    plt.savefig(os.path.join(grafico_dir, nome_arquivo))
    plt.close()

def plot_countplot(df, x, hue, titulo, nome_arquivo):
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x=x, hue=hue)
    plt.title(titulo)
    plt.xlabel(x)
    plt.ylabel('Quantidade')
    plt.legend(title=hue)
    plt.grid(True)
    plt.savefig(os.path.join(grafico_dir, nome_arquivo))
    plt.close()

# Carrega os dados
df = carregar_dados('planilhas/Dados coletados - refactoring.xlsx')
if df is None:
    exit()

print("Dados carregados com sucesso!")

# Conversão de experiência para numérico
df['Exp_Num'] = df['Experiencia'].map({
    '< 1 ano': 0.5,
    '1-2 anos': 1.5,
    '3-5 anos': 4,
    '6+ anos': 7
})

# ANÁLISE DESCRITIVA
print("\nANÁLISE DESCRITIVA")
desc_stats = df[['Tempo (h)', 'LOC Modificadas', 'Erros Funcionais', 'Problemas de Design']].describe()
print(desc_stats)

grouped = df.groupby('Ferramenta')[['Tempo (h)', 'LOC Modificadas', 'Erros Funcionais', 'Problemas de Design']].agg(['mean', 'std', 'median'])
print("\nResumo por Ferramenta (média, desvio padrão, mediana):")
print(grouped)

print("\nDistribuições dos participantes:")
print("\nFormação:")
print(df['Formacao'].value_counts())
print("\nExperiência:")
print(df['Experiencia'].value_counts())
print("\nConhecimento em Java:")
print(df['Conhecimento_Java'].value_counts())
print("\nConhecimento em Refatoração:")
print(df['Conhecimento_Refatoracao'].value_counts())

# Gráficos descritivos
plot_boxplot(df, 'Ferramenta', 'Tempo (h)', 'Distribuição do Tempo por Ferramenta', 'tempo_por_ferramenta.png')
plot_boxplot(df, 'Ferramenta', 'LOC Modificadas', 'Distribuição de LOC Modificadas por Ferramenta', 'loc_por_ferramenta.png')
plot_boxplot(df, 'Ferramenta', 'Erros Funcionais', 'Distribuição de Erros Funcionais por Ferramenta', 'erros_por_ferramenta.png')
plot_boxplot(df, 'Ferramenta', 'Problemas de Design', 'Distribuição de Problemas de Design por Ferramenta', 'problemas_por_ferramenta.png')
plot_countplot(df, 'Ferramenta', 'Erros Funcionais', 'Contagem de Erros Funcionais por Ferramenta', 'contagem_erros_funcionais.png')

plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Tempo (h)', hue='Ferramenta', bins=20, kde=True)
plt.title('Histograma do Tempo por Ferramenta')
plt.xlabel('Tempo (horas)')
plt.ylabel('Frequência')
plt.grid(True)
plt.savefig(os.path.join(grafico_dir, 'histograma_tempo.png'))
plt.close()

# ANÁLISE INFERENCIAL (Testes de hipótese)
print("\nANÁLISE INFERENCIAL (Testes de Hipótese)")

def realizar_teste_t(coluna):
    smart = df[df['Ferramenta'] == 'SmartRefactor'][coluna]
    trad = df[df['Ferramenta'] == 'Tradicional'][coluna]
    t_stat, p_val = stats.ttest_ind(smart, trad, equal_var=False)
    print(f"\nTeste T-Student para {coluna}:")
    print(f"t = {t_stat:.4f}, p = {p_val:.4f}")
    if p_val < 0.05:
        print("Diferença estatística significativa entre as ferramentas.")
    else:
        print("Não há diferença estatística significativa entre as ferramentas.")

def realizar_teste_mannwhitney(coluna):
    smart = df[df['Ferramenta'] == 'SmartRefactor'][coluna]
    trad = df[df['Ferramenta'] == 'Tradicional'][coluna]
    u_stat, p_val = stats.mannwhitneyu(smart, trad, alternative='two-sided')
    print(f"\nTeste Mann-Whitney U para {coluna}:")
    print(f"U = {u_stat:.2f}, p = {p_val:.4f}")
    if p_val < 0.05:
        print("Diferença estatística significativa entre as ferramentas.")
    else:
        print("Não há diferença estatística significativa entre as ferramentas.")

# Testes
realizar_teste_t('Tempo (h)')
realizar_teste_t('Problemas de Design')
realizar_teste_t('LOC Modificadas')
realizar_teste_mannwhitney('Erros Funcionais')

# ANÁLISE ADICIONAL (Correlação e Regressão)
print("\nANÁLISE ADICIONAL (Correlação e Regressão)")

# Correlação entre experiência e erros
corr_erros = df['Exp_Num'].corr(df['Erros Funcionais'], method='spearman')
print(f"\nCorrelação de Spearman entre Experiência e Erros Funcionais: r = {corr_erros:.3f}")
if abs(corr_erros) > 0.3:
    print("Correlação moderada detectada.")
else:
    print("Correlação fraca ou nula.")

# Boxplot erros x experiencia
plt.figure(figsize=(10, 6))
sns.boxplot(x='Experiencia', y='Erros Funcionais', data=df, order=['< 1 ano', '1-2 anos', '3-5 anos', '6+ anos'])
plt.title('Erros Funcionais por Nível de Experiência')
plt.xlabel('Experiência')
plt.ylabel('Erros Funcionais')
plt.grid(True)
plt.savefig(os.path.join(grafico_dir, 'erros_por_experiencia.png'))
plt.close()

# Regressão linear com interação
modelo_interacao = smf.ols('Q("Erros Funcionais") ~ C(Ferramenta) * Exp_Num', data=df).fit()
print("\nRegressão Linear com Interação entre Ferramenta e Experiência:")
print(modelo_interacao.summary())

sns.lmplot(data=df, x='Exp_Num', y='Erros Funcionais', hue='Ferramenta', aspect=1.5, height=6, ci=None)
plt.title('Relação entre Experiência e Erros Funcionais por Ferramenta')
plt.xlabel('Experiência (anos aproximados)')
plt.ylabel('Erros Funcionais')
plt.grid(True)
plt.savefig(os.path.join(grafico_dir, 'interacao_experiencia_ferramenta.png'))
plt.close()

# Comparação por grupo de experiência
df['Grupo_Exp'] = pd.cut(df['Exp_Num'], bins=[0, 1, 4, np.inf], labels=['Baixa', 'Média', 'Alta'])

for grupo in df['Grupo_Exp'].unique():
    subset = df[df['Grupo_Exp'] == grupo]
    print(f"\nAnálise para grupo de experiência: {grupo}")
    smart = subset[subset['Ferramenta'] == 'SmartRefactor']['Erros Funcionais']
    trad = subset[subset['Ferramenta'] == 'Tradicional']['Erros Funcionais']
    if len(smart) > 0 and len(trad) > 0:
        u_stat, p_val = stats.mannwhitneyu(smart, trad, alternative='two-sided')
        print(f"U = {u_stat:.2f}, p = {p_val:.4f}")
        if p_val < 0.05:
            print("Diferença significativa entre ferramentas nesse grupo.")
        else:
            print("Sem diferença significativa nesse grupo.")
    else:
        print("Dados insuficientes para esse grupo.")

# Gráfico final com valores ajustados
exp_media = df['Exp_Num'].mean()
ferramentas = df['Ferramenta'].unique()
ajustes = pd.DataFrame({'Ferramenta': ferramentas, 'Exp_Num': exp_media})
ajustes['Erros_Previstos'] = modelo_interacao.predict(ajustes)

plt.figure(figsize=(8, 6))
sns.barplot(data=ajustes, x='Ferramenta', y='Erros_Previstos', palette='Set2')
plt.ylabel('Erros Funcionais (ajustado pela experiência)')
plt.title('Erros Funcionais Ajustados por Ferramenta (com controle de experiência)')
plt.grid(True)
plt.savefig(os.path.join(grafico_dir, 'erros_ajustados_por_ferramenta.png'))
plt.close()

sys.stdout.close()