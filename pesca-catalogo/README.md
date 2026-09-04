# Catálogo de Peixes de Pesca 🎣

Aplicação Flask que consome a API pública do **iNaturalist** (https://api.inaturalist.org/v1)
e monta um catálogo de peixes populares na pesca esportiva no Brasil.

## API escolhida
- **iNaturalist API v1** — banco de dados aberto de biodiversidade, sem necessidade de chave/token.
- Endpoint de busca: `GET /v1/taxa?q=<nome>&rank=species`
- Endpoint de detalhe: `GET /v1/taxa/<id>`

## Estrutura das rotas
- **Rota principal (`/`)**: para cada peixe de uma lista pré-definida (Tucunaré, Dourado,
  Tilápia, etc.), consulta a API e monta o catálogo com nome, nome científico e foto.
  A busca pede vários resultados (`per_page=10`) e filtra pelo campo `iconic_taxon_name`
  para garantir que só entrem peixes de verdade no catálogo (e não outros bichos que
  também combinam com o nome digitado).
- **Rota secundária (`/peixe/<id>`)**: recebe o ID do peixe pela URL, consulta a API
  novamente para trazer os dados completos (resumo, status de conservação, número de
  registros de observação) e exibe a página de detalhes.

## Como rodar
```bash
pip install -r requirements.txt
python app.py
```
Depois acesse http://127.0.0.1:5000 no navegador.

## Observação
Como a aplicação depende da API externa, é necessário estar conectado à internet.
