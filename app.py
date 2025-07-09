import streamlit as st
import pandas as pd
from data_loader import carregar_dados_vendas, aplicar_filtros
from utils import calcular_variacao_percentual, exibir_metrica
from charts import grafico_receita_mensal
from settings import CAMINHO_VENDAS, CAMINHO_CLIENTES, CAMINHO_PRODUTOS

st.set_page_config(layout='wide', page_title='TecnoPlus')
st.sidebar.title("Filtros")

fVendas, dClientes, dProdutos = carregar_dados_vendas(CAMINHO_VENDAS, CAMINHO_CLIENTES, CAMINHO_PRODUTOS)

dict_regiao = dClientes.set_index('Cliente_ID')['Regiao'].to_dict()
dict_produtos = dProdutos.set_index('Produto_ID')['Produto'].to_dict()

anos_disponiveis = sorted(fVendas['Ano'].unique(), reverse=True)
ano_selecionado = st.sidebar.selectbox("Selecione o Ano:", anos_disponiveis)

fVendas_filtrado = aplicar_filtros(fVendas, ano=ano_selecionado, dict_regiao=dict_regiao)

regioes_disponiveis = ['Todas'] + sorted(fVendas_filtrado['Regiao'].dropna().unique())
regiao_selecionada = st.sidebar.selectbox("Selecione a Região:", regioes_disponiveis)

fVendas_filtrado = aplicar_filtros(fVendas_filtrado, ano=ano_selecionado, regiao=regiao_selecionada)

st.title(f'Dashboard de Vendas - {ano_selecionado}')
if regiao_selecionada != 'Todas':
    st.subheader(f"Região: {regiao_selecionada}")

fVendas_anterior = fVendas[fVendas['Ano'] == (ano_selecionado - 1)].copy()

col1, col2, col3, col4, col5 = st.columns(5)

total_vendas = fVendas_filtrado['ID_Venda'].nunique()
vendas_ano_anterior = fVendas_anterior['ID_Venda'].nunique()
delta_vendas = calcular_variacao_percentual(total_vendas, vendas_ano_anterior)
exibir_metrica(col1, 'Total de Vendas', total_vendas, delta=delta_vendas)

faturamento_total = fVendas_filtrado['Receita'].sum()
faturamento_anterior = fVendas_anterior['Receita'].sum()
delta_faturamento = calcular_variacao_percentual(faturamento_total, faturamento_anterior)
exibir_metrica(col2, 'Faturamento Total', faturamento_total, prefixo='R$', delta=delta_faturamento)

ticket_medio = faturamento_total / total_vendas if total_vendas else 0
ticket_anterior = faturamento_anterior / vendas_ano_anterior if vendas_ano_anterior else 0
delta_ticket = calcular_variacao_percentual(ticket_medio, ticket_anterior)
exibir_metrica(col3, 'Ticket Médio', ticket_medio, prefixo='R$', delta=delta_ticket)

total_descontos = fVendas_filtrado['Desconto'].sum()
descontos_anterior = fVendas_anterior['Desconto'].sum()
delta_descontos = calcular_variacao_percentual(total_descontos, descontos_anterior)
exibir_metrica(col4, 'Total de Descontos', total_descontos, prefixo='R$', delta=delta_descontos)

total_clientes = fVendas_filtrado['Cliente_ID'].nunique()
clientes_anterior = fVendas_anterior['Cliente_ID'].nunique()
delta_clientes = calcular_variacao_percentual(total_clientes, clientes_anterior)
exibir_metrica(col5, 'Clientes Ativos', total_clientes, delta=delta_clientes)

# Gráficos
col_receita_mes, col_top_produtos = st.columns([6, 4])

with col_receita_mes:
    st.plotly_chart(grafico_receita_mensal(fVendas_filtrado), use_container_width=True)

with col_top_produtos:
    num_produtos = st.slider("Top Produtos", 5, 50, 20, step=5)
    df_freq = fVendas_filtrado['Produto_ID'].value_counts().reset_index()
    df_freq.columns = ['Produto_ID', 'Qtd Vendas']
    df_freq['Produto'] = df_freq['Produto_ID'].map(dict_produtos)
    df_top_n = df_freq[['Produto', 'Qtd Vendas']].head(num_produtos)
    st.dataframe(df_top_n, use_container_width=True, height=350)