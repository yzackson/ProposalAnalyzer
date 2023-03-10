from PyPDF2 import PdfReader
from pathlib import Path
import re

path = Path('./Propostas')
propostas_files = list(path.glob('*.pdf'))


lista_de_propostas = []

    # Trabalha proposta por proposta
for proposta_file in propostas_files:
    # leio o arquivo
    pdf = PdfReader(proposta_file)

    # extrai todo o texto do arquivo de proposta
    conteudo = pdf.pages[0].extract_text() 

    # Determina o ínicio e fim do texto a ser extraído
    inicio = conteudo.find("Quant.  Especificação    Preço")
    fim = conteudo.find("SERVIÇO S") if conteudo.find("SERVIÇO S") >= 0 else conteudo.find("OBS:.")

    proposta_det = {
        'NomeProposta': str(proposta_file),
        'Itens': conteudo[inicio:fim:]
    }

    lista_de_propostas.append(proposta_det)

filter_item = re.compile('^(\d\d\d\s\D\s.+)')
filter_value = re.compile('^(\d.*\D\d\d)')

with open('propostas.txt', 'w', encoding='utf-8') as f:
    for proposta in lista_de_propostas:
        prop = {
            'nome': '',
            'itens': [],
            'valor': 0.0
        }
        prop['nome'] = proposta['NomeProposta']
        f.write('\n\n-------------------------------------------\nNota: %s\n' % (proposta['NomeProposta']))
        linessplited = proposta['Itens'].splitlines()
        if linessplited != [] :
            i = 0
            proposta_list = []
            while i < len(linessplited):
                if linessplited[i].isspace():
                    linessplited.pop(i)
                else:
                    linessplited[i] = linessplited[i].strip()
                    prop_item = filter_item.findall(linessplited[i])
                    item_val = filter_value.findall(linessplited[i])
                    if prop_item != []:
                        prop['itens'].append({'qtd': int(prop_item[0].split(' – ')[0]), 'descricao': prop_item[0].split(' – ')[1]})
                        f.write('%s\n' % (prop_item[0].split(' – ')))
                    elif item_val != []:
                        prop['valor'] = float(item_val[0].replace('.','').replace(',','.'))
                        f.write('%s\n\n' % (item_val))
                    i += 1
        print(prop)