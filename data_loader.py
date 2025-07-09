import pandas as pd

def carregar_dados_vendas(caminho_vendas, caminho_clientes, caminho_produtos):
    fVendas = pd.read_csv(caminho_vendas)
    dClientes = pd.read_csv(caminho_clientes)
    dProdutos = pd.read_csv(caminho_produtos)

    fVendas['Data'] = pd.to_datetime(fVendas['Data_ID'].astype(str), format='%Y%m%d')
    fVendas['Ano'] = fVendas['Data'].dt.year
    fVendas['Mes'] = fVendas['Data'].dt.month

    return fVendas, dClientes, dProdutos

def aplicar_filtros(df, ano, regiao=None, dict_regiao=None):
    df_filtrado = df[df['Ano'] == ano].copy()
    if dict_regiao:
        df_filtrado['Regiao'] = df_filtrado['Cliente_ID'].map(dict_regiao)
    if regiao and regiao != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Regiao'] == regiao]
    return df_filtrado
