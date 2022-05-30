import numpy as np
import pandas as pd
import re

DEFINICAO_AUTOMATO = {
    'completo' :{

        'estado_inicial':'Q0',

        'estados_finais' : {
            'QD1':'Variável', 
            'QB4': 'Comentário', 
            'QA2': 'Comentário', 
            'QC2': 'Comentário', 
            'QE1': 'Numérico Inteiro', 
            'QE3': 'Numérico Float'
            },
            
        'Q0' : {
            'mudanca_estado':['[A-Za-z]', '[(]', '[/]', '[{]', '[0-9/+/-]'],
            'prox_estado':['QD1', 'QB1', 'QA1', 'QC1', 'QE1']
        },
        'QA1' : {
            'mudanca_estado':['[/]'],
            'prox_estado':['QA2']
        },
        'QA2' : {
            'mudanca_estado':['[^\n]'],
            'prox_estado':['QA2']
        },
        'QB1': {
            'mudanca_estado':['[*]'],
            'prox_estado':['QB2']
        },
        'QB2': {
            'mudanca_estado':['[^\n\*]', '[*]'],
            'prox_estado':['QB2', 'QB3']
        },
        'QB3': {
            'mudanca_estado':['[^\n\)]', '[)]'],
            'prox_estado':['QB2', 'QB4']
        }        ,
        'QC1': {
            'mudanca_estado':['[^\n}]', '[}]'],
            'prox_estado':['QC1', 'QC2']
        },
        'QD1': {
            'mudanca_estado':['[A-Za-z0-9\_]'],
            'prox_estado':['QD1']
        },
        'QE1': {
            'mudanca_estado':['[0-9]', '[.]'],
            'prox_estado':['QE1', 'QE2']
        },
        'QE2': {
            'mudanca_estado':['[0-9]'],
            'prox_estado':['QE3']
        },
        'QE3': {
            'mudanca_estado':['[0-9]'],
            'prox_estado':['QE3']
        }

    }

}
NOME_COLUNAS = ['Estado Atual', 'Entrada Processada', 'Próximo Estado']

def imprime_mudaca_estado(estado_atual, entrada, proximo_estado):

    saida = 'Estado Atual: {}; Entrada: {}, Próximo Estado: {}'.format(estado_atual, entrada, proximo_estado)
    print(saida)

def processa_df(df, estado_atual, entrada, proximo_estado):

    df.loc[len(df.index)] = [estado_atual, entrada, proximo_estado] 

    return df

def processa_entrada(valor_entrada, automato = DEFINICAO_AUTOMATO['completo']):

    df = pd.DataFrame(columns=NOME_COLUNAS)
    retorno = ''

    valor_entrada = str(valor_entrada)
    estado_atual = automato['estado_inicial']

    try:
        for c in valor_entrada:
            mudancas_estado = automato[estado_atual].get('mudanca_estado')
            idx_mudanca_estado = 0
            for mudanca_estado in mudancas_estado:

                padrao = re.compile(mudanca_estado)

                if padrao.search(c):
                    proximos_estados = automato[estado_atual].get('prox_estado')
                    proximo_estado = proximos_estados[idx_mudanca_estado]

                    imprime_mudaca_estado(estado_atual, c,  proximo_estado)
                    df = processa_df(df, estado_atual, c,  proximo_estado)
                    estado_atual = proximo_estado
                    break

                idx_mudanca_estado += 1

                if idx_mudanca_estado >= len(mudancas_estado):
                    raise Exception("Entrada Inválida --> {}".format(c))
        
        classe = automato['estados_finais'].get(estado_atual)
        if classe:
            retorno = 'Entrada Aceita com Sucesso para a Classe {}'.format(classe)
        else:
            raise Exception("Entrada Inválida".format(c))
    except Exception as e:
        retorno = str(e)
    
    return retorno, df
