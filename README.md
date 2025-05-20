# Análise de Ferramentas de Refatoração de Código

Este projeto realiza uma análise estatística comparativa entre a ferramenta tradicional de refatoração do Eclipse IDE e a nova ferramenta **SmartRefactor**, desenvolvida pela Zaina DevTools Inc., com base em dados coletados de 120 desenvolvedores.

## 📊 Objetivo

Avaliar o impacto da ferramenta **SmartRefactor** em comparação com a refatoração tradicional, considerando métricas como:

* Tempo de execução
* Linhas de código modificadas
* Erros funcionais
* Problemas de design

## 📁 Estrutura

* **Script principal**: `main.py`
* **Entrada**: `Dados coletados - refactoring.xlsx`
* **Saída**: Gráficos salvos na pasta `graficos/` + resultados impressos no console
* **Análises**:

  * Estatísticas descritivas
  * Testes de hipótese (T-Student, Mann-Whitney)
  * Correlação entre perfil dos participantes e erros
  * Gráficos de distribuição e comparação

## 🧪 Ferramentas Estatísticas

* Python 3 com:

  * `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`
* Todos os testes estão descritos e implementados no script

## 💫 Referências

https://pandas.pydata.org/

https://seaborn.pydata.org/

https://www.scipy.org/

https://matplotlib.org/
