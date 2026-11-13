# Atlas do Basquete

[**Abrir o Atlas**](https://lucaaregis4r-ops.github.io/Atlas-Basquete/)

Scouting de basquete brasileiro organizado por competição, equipe, atletas e jogos. A interface usa dados observados dos relatórios públicos da LNB e das competições CBB/Go Champs. A navegação foi inspirada na organização do Atlas do Voleibol, com linguagem visual própria do basquete.

## Cobertura e interpretação

- **NBB e LDB:** os resultados são descobertos nas tabelas oficiais da LNB e reunidos em `docs/exports/nbb_observed.json`, organizados por competição e temporada. Relatórios são coletados progressivamente. Os arremessos identificados podem ser filtrados por período e tipo; jogos sem dados de arremesso são contados na campanha, mas não no perfil de finalizações. A cobertura dos relatórios e as falhas de coleta são registradas; partidas e temporadas não reconhecidas pela fonte não são inventadas.
- **CBI:** calendários e placares publicados pela Go Champs/CBB. A interface só oferece competições com pelo menos um resultado final. Equipes são identificadas a partir dos jogos finalizados disponíveis.
- **Súmulas CBI:** a coleta percorre gradualmente partidas finalizadas. Uma súmula individual só é incluída quando os totais de pontos de ambos os lados e a soma dos pontos dos atletas coincidem com o placar final. Dados anteriormente conferidos são preservados se o placar não mudou. Falhas permanecem disponíveis para nova tentativa.
- **Arremessos CBI:** 2 pontos, 3 pontos e lances livres são usados para validar a pontuação individual. As tentativas e conversões de quadra só entram nos gráficos quando os campos existem, são não negativos, os acertos não superam as tentativas e a soma das cestas explica os pontos do atleta. A cobertura de súmulas é mostrada por equipe e pode ser parcial.

Dados ausentes não representam zero. Resultados e indicadores são descritivos da amostra e não são uma previsão de vitória. A fonte de cada partida está acessível no site.

## Atualizar e gerar o site

```bash
python -m cbb.extractors.lnb_observed --all-seasons --max-reports 80
python -m cbb.extractors.cbi_observed
python -m cbb export
```

O coletor LNB descobre os jogos finalizados nas tabelas de NBB e LDB, preserva os registros existentes e consulta até 80 relatórios por execução, com até três conexões simultâneas; `--all-seasons` descobre o histórico de temporadas. Os resultados são persistidos a cada lote de 20 relatórios. O coletor CBI descobre as competições e fases publicadas, reúne os resultados e tenta até 40 súmulas adicionais por execução, em até três consultas simultâneas, distribuindo as tentativas entre competições. Resultados conferidos são armazenados em `docs/exports/cbi_observed.json`; a coleta é incremental. O comando `python -m cbb sync` atualiza as duas fontes. O GitHub Actions executa a sincronização quatro vezes ao dia (a cada seis horas), sem sobrepor execuções, e regenera os arquivos estáticos. As médias oficiais dos atletas por temporada são coletadas separadamente; elas não dependem dos filtros de período ou dos relatórios individuais.

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
python -m cbb export
```

A exportação gera `index.html` e `docs/index.html` com os dados incorporados. Para executar as verificações de desenvolvimento, instale `pytest` e rode `python -m pytest -q`.

## Análises disponíveis

Na aba **Análises**, os mesmos filtros de competição e equipe alimentam eFG%, frequência de 3 pontos, FTR e TS% quando os dados necessários existem. A distribuição por atleta mostra fatias observadas e, para períodos NBB/LDB com pelo menos 20 tentativas em três jogos e referência nos outros períodos, um ajuste com 20 tentativas equivalentes. O mapa NBB utiliza coordenadas relativas do relatório da LNB; a base CBI ainda não tem coordenadas. Comparações mostram o tamanho das amostras e confrontos realmente registrados.

O modelo de Markov anterior está disponível como **exemplo didático com parâmetros hipotéticos**, sem atribuir suas probabilidades à equipe selecionada. Ratings por posse, perdas, rebotes e probabilidades de vitória ao longo do jogo dependem de dados adicionais e não são apresentados como fatos quando a cobertura é insuficiente.

O mapa NBB usa um desenho esquemático com a mesma orientação e proporção 623 × 345 do gráfico dos relatórios LNB, mantendo as coordenadas percentuais como publicadas, sem espelhamento. Círculos representam acertos e cruzes representam erros; o controle permite filtrar o resultado. O desenho não deve ser usado como medição de distância ou classificação automática de zonas. Os gráficos adicionais mostram escolhas de 2 e 3 pontos por atleta, eFG% por jogo, aproveitamento por quarto e comparação de eficiência entre equipes; cada gráfico informa a escala e o tamanho da amostra quando aplicável.

Para as súmulas CBI, os pontos individuais e cestas convertidas são usados quando a soma confere com o placar. Os campos de tentativas da fonte não comprovam a inclusão dos erros e não são usados para calcular aproveitamento, eFG%, FTR ou TS%. A aba Análises mostra a distribuição dos pontos, a contribuição dos maiores pontuadores e a origem da pontuação identificada. Com ao menos seis súmulas da equipe, a participação dos atletas nas três mais recentes é ajustada pelo perfil anterior, com peso equivalente a três jogos médios; é uma descrição exploratória da pontuação, não uma previsão de arremessos.
