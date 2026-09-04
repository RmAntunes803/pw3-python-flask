# app.py
# Aplicação Flask que consome a API pública do iNaturalist (api.inaturalist.org)
# e monta um catálogo de peixes de pesca esportiva.

from flask import Flask, render_template
import urllib.request  # envia requisições para uma URL (endereço online)
import urllib.error     # para identificar o motivo exato quando a API recusa a requisição
import urllib.parse     # para codificar espaços e acentos corretamente na URL
import json             # converte dados de JSON para dicionário e vice-versa
import re                # usado só para limpar tags HTML do resumo da Wikipédia
import time              # usado para dar uma pequena pausa entre as requisições

app = Flask(__name__)

# Lista de peixes bem conhecidos entre os pescadores no Brasil.
# A chave é o nome popular (usado na tela) e o valor é o nome científico
# (usado na busca, porque é único e a API sempre encontra exatamente esse peixe;
# buscar pelo nome popular em português é ambíguo e às vezes não acha nada).
PEIXES_PESCA = {
    "Tucunaré": "Cichla",
    "Dourado": "Salminus brasiliensis",
    "Tilápia": "Oreochromis",
    "Traíra": "Hoplias malabaricus",
    "Pintado": "Pseudoplatystoma corruscans",
    "Pacu": "Piaractus mesopotamicus",
    "Corvina": "Micropogonias furnieri",
    "Robalo": "Centropomus undecimalis",
    "Tainha": "Mugil liza",
    "Pirarucu": "Arapaima gigas",
}


def consulta_api(url):
    """Faz a requisição para a API e devolve os dados já convertidos em dicionário."""
    # Alguns servidores bloqueiam requisições sem um User-Agent, então enviamos um
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resposta = urllib.request.urlopen(req)
    dados = resposta.read()  # lendo a resposta da requisição
    return json.loads(dados)  # convertendo de JSON para dicionário


def limpa_html(texto):
    """Remove tags HTML simples que às vezes vêm no resumo da Wikipédia."""
    if not texto:
        return None
    return re.sub('<[^<]+?>', '', texto)


def busca_peixe(nome_cientifico):
    """
    Busca um peixe pelo nome científico (único, então a busca é exata e sempre encontra).
    Ainda assim confere se o resultado é mesmo um peixe (iconic_taxon_name == Actinopterygii),
    por segurança.
    """
    url = f'https://api.inaturalist.org/v1/taxa?q={urllib.parse.quote(nome_cientifico)}&per_page=5&locale=pt-BR'
    dados = consulta_api(url)
    for candidato in dados.get('results', []):
        if candidato.get('iconic_taxon_name') == 'Actinopterygii':
            return candidato
    return None  # nenhum peixe encontrado para esse nome


# Guarda o catálogo já montado, pra não precisar bater na API de novo
# toda vez que alguém recarrega a página (e assim evitar o bloqueio por excesso
# de requisições). Pra atualizar, basta reiniciar o servidor.
_cache_catalogo = None


def monta_catalogo():
    catalogo = []

    for nome_popular, nome_cientifico in PEIXES_PESCA.items():
        try:
            peixe = busca_peixe(nome_cientifico)
            if peixe:
                foto = peixe.get('default_photo')
                catalogo.append({
                    'id': peixe['id'],
                    # usamos o nosso nome popular em português (mais confiável
                    # do que confiar que a API sempre tem esse nome cadastrado)
                    'nome_comum': nome_popular,
                    'nome_cientifico': peixe['name'],
                    'foto': foto['medium_url'] if foto else None,
                })
            else:
                print(f'Nenhum peixe encontrado para "{nome_popular}" ({nome_cientifico})')
        except urllib.error.HTTPError as erro:
            # a API costuma recusar (erro 429) se mandarmos requisições rápido
            # demais, uma atrás da outra
            print(f'Erro HTTP ao buscar "{nome_popular}": {erro.code} {erro.reason}')
        except Exception as erro:
            # se um peixe falhar na busca, não derruba a página inteira
            print(f'Erro ao buscar "{nome_popular}": {erro}')

        time.sleep(1)  # pequena pausa pra não estourar o limite de requisições da API

    return catalogo


# ROTA PRINCIPAL: consome a API e gera o catálogo (lista) de peixes
@app.route('/')
def index():
    global _cache_catalogo
    if _cache_catalogo is None:
        _cache_catalogo = monta_catalogo()

    return render_template('peixes.html', catalogo=_cache_catalogo)


# ROTA SECUNDÁRIA: exibe os dados individuais e detalhados de um peixe específico
# o identificador do peixe é passado via parâmetro de rota (ex: /peixe/48533)
@app.route('/peixe/<int:taxon_id>')
def detalhe(taxon_id):
    url = f'https://api.inaturalist.org/v1/taxa/{taxon_id}?locale=pt-BR'
    dados = consulta_api(url)
    peixe = dados['results'][0]

    foto = peixe.get('default_photo')
    status = peixe.get('conservation_status')

    peixe_info = {
        'id': peixe['id'],
        'nome_comum': peixe.get('preferred_common_name') or peixe['name'],
        'nome_cientifico': peixe['name'],
        'foto': foto['medium_url'] if foto else None,
        'resumo': limpa_html(peixe.get('wikipedia_summary')),
        'wikipedia_url': peixe.get('wikipedia_url'),
        'status_conservacao': status.get('status_name') if status else 'Não avaliado',
        'observacoes': peixe.get('observations_count'),
    }

    return render_template('peixe.html', peixe=peixe_info)


if __name__ == '__main__':
    # iniciando o servidor
    app.run(debug=True)
