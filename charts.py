import plotly.express as px
import pandas as pd


def grafico_receita_mensal(df):
    df['MesNumero'] = df['Data'].dt.month
    df['MesNome'] = df['Data'].dt.strftime('%b')
    df_mensal = df.groupby(['MesNumero', 'MesNome'])['Receita'].sum().reset_index()
    df_mensal = df_mensal.sort_values('MesNumero')

    fig = px.line(
        df_mensal, x='MesNome', y='Receita',
        title='Receita por Mês',
        labels={'MesNome': 'Mês', 'Receita': 'Receita Total'},
        markers=True
    )
    fig.update_layout(height=500)
    return fig

