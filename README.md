# Basquete BR — Atlas Tático

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![DuckDB](https://img.shields.io/badge/database-DuckDB-yellow.svg)](https://duckdb.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> **Consultar a publicação online:** [https://lucaaregis4r-ops.github.io/Atlas-Basquete/](https://lucaaregis4r-ops.github.io/Atlas-Basquete/)

Scouting tático do basquetebol brasileiro, com um piloto de dados observados do NBB e módulos de demonstração de Four Factors, Markov e eficiência espacial.

## CBI Super 15 (Sub-15) 2026 — clubes verificados

O Atlas inclui uma tela **CBI Super 15 · Clubes oficiais** com duas competições
separadas: **masculino** (16 classificados para a fase final de 6 a 14 de dezembro)
e **feminino** (26 participantes da etapa única, com posições finais oficiais).
O cadastro fica em `cbb/data/cbi_sub15_2026.json`, com a fonte de cada recorte,
e é incorporado ao HTML autossuficiente durante `python -m cbb export`.

- Masculino: [Grêmio Náutico União, lista das 16 equipes classificadas em setembro/2026](https://www.gnu.com.br/site/noticias/gnu-vai-disputar-a-etapa-final-do-cbi-super-15-de-basquete).
- Feminino: [CBC, classificação oficial de agosto/2026](https://www.cbclubes.org.br/evento/cbi/cbir-de-basquetebol-sub-15-etapa-unica-feminino-2026).

**Importante:** os nomes de clubes não significam que box scores, estatísticas
individuais, partidas ou play-by-play tenham sido importados. O antigo bloco com
dois perfis fictícios (Pinheiros/Thalia) foi removido da demonstração do CBI;
o Atlas **não atribui números simulados a clubes reais** nessa competição.
O comando `python -m cbb sync` consulta o CBB Archive, mas não constitui um
importador de súmulas verificadas por partida do CBI. Para publicar novas métricas
é necessário acrescentar um extrator de relatórios com verificação de origem,
amostras e integridade.

## NBB observado

O piloto separa temporadas e informa a cobertura de cada partida. Em 2026–2027, acompanha uma amostra de jogos de Minas e Cruzeiro, com seus adversários. A final de 2025–2026 oferece um recorte histórico separado. Cada partida aponta para o relatório original da LNB.

A distribuição experimental calcula a participação de cada atleta nas tentativas de quadra observadas da equipe, com filtros de período e tipo de arremesso. A fatia ajustada aplica 20 tentativas equivalentes a partir dos outros períodos para recortes com ao menos 20 tentativas em três jogos. As coordenadas estão em porcentagem do gráfico da LNB. A cobertura do jogada a jogada exige os quatro quartos e placar final compatível com a tabela oficial. Os arremessos são conferidos por equipe e tipo contra a súmula.

O conjunto observado está em `docs/exports/nbb_observed.json`. Para atualizar os relatórios da amostra declarada em `data/nbb_pilot_sources.json`, execute `python -m cbb.extractors.lnb_observed` e depois `python -m cbb export`. O comando de sincronização do acervo CBB não amplia a amostra da LNB.

---

## 1. Fundamentação Científica & Literatura Citada

O **Atlas do Basquete** fundamenta suas análises nos principais artigos e obras canônicas de *Sports Analytics*:

1. **Dean Oliver (2004) — *Basketball on Paper***:
   - **Os Quatro Fatores de Sucesso**:
     1. *Aproveitamento Efetivo* ($eFG\% = \frac{FGM + 0.5 \times 3PM}{FGA}$) — Peso $\approx 40\%$
     2. *Taxa de Desperdício* ($TOV\% = \frac{TOV}{FGA + 0.44 \times FTA + TOV}$) — Peso $\approx 25\%$
     3. *Rebote Ofensivo* ($ORB\% = \frac{ORB}{ORB + OppDRB}$) — Peso $\approx 20\%$
     4. *Taxa de Lances Livres* ($FTR = \frac{FTA}{FGA}$) — Peso $\approx 15\%$
   - **Ritmo de Jogo Padronizado FIBA 40m**: $Pace = 40 \times \frac{Poss}{Min}$.
   - **Expectativa Pitagórica de Vitórias**: $ExpWin\% = \frac{ORtg^{13.91}}{ORtg^{13.91} + DRtg^{13.91}}$ (Exponente de Daryl Morey / Dean Oliver).

2. **Sandholtz & Bornn (2020) & Cervone et al. (2016, JASA)**:
   - **Cadeias de Markov Absorventes de Posse**:
     Espaço de estados transitórios $Q$ (Início da posse, circulação perimetral, infiltração no garrafão, post-up, arremesso 3PT, arremesso mid-range, arremesso na pintura, rebote ofensivo) e absorventes $R$ (cesta 2PT, cesta 3PT, lance livre, turnover, rebote defensivo do adversário).
   - **Matriz Fundamental**: $N = (I - Q)^{-1}$
   - **Probabilidades de Absorção**: $B = N \cdot R$
   - **Expected Possession Value (EPV)**: $v = B \cdot \vec{r}_{\text{recompensas}}$

3. **Kirk Goldsberry (2012, 2019) — *CourtVision* & *SprawlBall***:
   - Eficiência espacial na quadra regulamentar FIBA ($28.0\text{m} \times 15.0\text{m}$).
   - Mapeamento em 10 zonas canônicas (Restricted Area $<1.25\text{m}$, Garrafão não-restrito, Meia distância esquerda/centro/direita, Corner 3 esquerda/direita, 3PT acima da cabeça esquerda/centro/direita).
   - **Superávit de Eficiência Espacial (SES)**: $SES = PPS_{\text{zona}} - PPS_{\text{liga}}$.

4. **Kubatko, Oliver, Pelton, Rosenbaum (2007) & FIBA Official Rules**:
   - **True Shooting**: $TS\% = \frac{PTS}{2 \times (FGA + 0.44 \times FTA)}$
   - **Taxa de Uso de Posse**: $USG\%$
   - **Valorização Oficial FIBA**: $PIR = (PTS + REB + AST + STL + BLK + FR) - ((FGA - FGM) + (FTA - FTM) + TOV + FC)$
   - **Intervalo de Confiança de Wilson (95%)** e **Shrinkage Bayesiano (Empirical Bayes)** para estabilização de pequenas amostras de arremesso.

---

## 2. Estrutura do Projeto

```
atlas basquete/
├── cbb/
│   ├── analysis/
│   │   ├── four_factors.py       # Quatro fatores, Pace 40m, Ratings, Expectativa Pitagórica
│   │   ├── markov_possession.py  # Cadeias de Markov absorventes, N = (I - Q)^-1, EPV
│   │   ├── player_advanced.py    # TS%, USG%, AST%, PIR FIBA, GmSc, Intervalo de Wilson
│   │   ├── shot_efficiency.py    # Goldsberry SES, PPS e mapeamento de zonas FIBA
│   │   └── win_probability.py    # Win Probability contínua e Leverage Index
│   ├── database/
│   │   ├── repository.py         # Repositório DuckDB com controle de hash e auditoria
│   │   └── schema.sql            # Esquema relacional
│   ├── extractors/
│   │   ├── cbb_archive.py        # Coletor REST do cbbarchive.online (times, rankings, lendas)
│   │   ├── lnb_boxscore.py       # Parser de súmulas oficiais e box scores FIBA
│   │   └── fallback_data.py      # Sementes calibradas das principais equipes brasileiras
│   ├── export/
│   │   ├── html_dashboard.py     # Compilador HTML autossuficiente e gerador de JSONs
│   │   └── templates/
│   │       └── dashboard.html    # Interface tática moderna, quadra vetorial e lab de Markov
│   ├── cli.py                    # Comandos CLI (export, sync, server)
│   ├── config.py                 # Dimensões da quadra FIBA e constantes
│   └── server.py                 # Backend opcional FastAPI
├── docs/                         # GitHub Pages build
│   ├── index.html                # Aplicação completa para navegação web
│   ├── .nojekyll                 # Ignora processador Jekyll do GitHub Pages
│   └── exports/                  # Cargas JSON desacopladas
├── index.html                    # Build estático local
├── tests/                        # Bateria de testes unitários automatizados
├── pyproject.toml
└── requirements.txt
```

---

## 3. Como Executar

### Ambiente e Dependências
```bash
# Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
pip install -e .
```

### Comandos Disponíveis
```bash
# Compilar e atualizar os arquivos estáticos (index.html e docs/index.html)
python -m cbb export

# Sincronizar com os dados da CBB e atualizar banco DuckDB
python -m cbb sync

# Iniciar servidor interativo local FastAPI
python -m cbb server --port 8000

# Executar bateria de testes unitários
pytest -v
```

---

## 4. Navegação do Atlas

**NBB observado** é a tela inicial. As abas abaixo usam números ilustrativos, incluindo as partidas e os mapas de arremessos.

- **Visão Geral**: Matriz dos Quatro Fatores da Liga, ranking de Net Rating, Pace vs Eficiência.
- **Equipes**: Dossiê individual de cada clube, gráficos comparativos e elenco com métricas avançadas.
- **Quadra & Shot Charts**: Quadra oficial FIBA vetorial com cálculo de SES (Goldsberry), filtro por tipo de arremesso e tooltips dinâmicos.
- **Cadeias de Markov**: Laboratório interativo de posse de bola. Visualização de estados, matriz fundamental e controle dinâmico para simular o ganho de pontos ao aumentar infiltrações no garrafão.
- **Confrontos H2H**: Simulador de partidas diretas, projeção de ritmo e margem de vitória.
- **Partidas**: Análise detalhada de jogos, súmulas e curva in-game de Win Probability (WP).
- **Atletas & Rankings**: Tabela ordenável e pesquisável de atletas com TS%, USG%, PIR FIBA, Game Score e intervalo de confiança a 95% de Wilson para bolas de 3pts.
- **Lendas CBB**: Hall da Fama oficial do basquete brasileiro (Oscar Schmidt, Hortência, Magic Paula, Janeth, Wlamir Marques, Tiago Splitter, etc.).
- **Metodologia**: Fórmulas matemáticas e catálogo de citações científicas.

---

## 5. Licença e Aviso Legal

Projeto independente de ciência de dados e scouting esportivo desenvolvido por **Lucas Regis**.
Os dados observados vêm dos relatórios oficiais da **LNB (Liga Nacional de Basquete)**. As exportações analíticas legadas correspondem à demonstração.
Distribuído sob licença MIT.
