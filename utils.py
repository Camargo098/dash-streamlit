def formatar_valor_compact(valor):
    sinal = '-' if valor < 0 else ''
    abs_val = abs(valor)

    if abs_val < 1_000:
        return f"{valor:,}".replace(',', '.')
    elif abs_val < 1_000_000:
        return f"{sinal}{abs_val / 1_000:.1f}K".replace('.', ',')
    elif abs_val < 1_000_000_000:
        return f"{sinal}{abs_val / 1_000_000:.1f}M".replace('.', ',')
    elif abs_val < 1_000_000_000_000:
        return f"{sinal}{abs_val / 1_000_000_000:.1f}B".replace('.', ',')
    else:
        return f"{sinal}{abs_val / 1_000_000_000_000:.1f}T".replace('.', ',')


def calcular_variacao_percentual(atual, anterior):
    if anterior == 0:
        return 0
    return ((atual - anterior) / anterior) * 100


def exibir_metrica(coluna, label, valor, prefixo='', delta=None):
    valor_formatado = formatar_valor_compact(valor)
    delta_formatado = f"{delta:.1f}%" if delta is not None else None
    coluna.metric(label=label, value=f'{prefixo}{valor_formatado}', delta=delta_formatado)