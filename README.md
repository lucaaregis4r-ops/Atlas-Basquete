# Atlas do Basquete

[**Abrir o Atlas**](https://lucaaregis4r-ops.github.io/Atlas-Basquete/)

Scouting de basquete brasileiro organizado por competição, equipe, atletas e jogos. A interface usa dados observados dos relatórios públicos da LNB e das competições CBB/Go Champs. A navegação foi inspirada na organização do Atlas do Voleibol, com linguagem visual própria do basquete.

## Cobertura e interpretação

- **NBB:** amostra de relatórios da LNB incluídos em `docs/exports/nbb_observed.json`. Os arremessos identificados podem ser filtrados por período e tipo; jogos sem dados de arremesso são contados na campanha, mas não no perfil de finalizações. Não é uma base completa da liga.
- **CBI:** calendários e placares publicados pela Go Champs/CBB. A interface só oferece competições com pelo menos um resultado final. Equipes são identificadas a partir dos jogos finalizados disponíveis.
- **Súmulas CBI:** a coleta percorre gradualmente partidas finalizadas. Uma súmula individual só é incluída quando os totais de pontos de ambos os lados e a soma dos pontos dos atletas coincidem com o placar final. Dados anteriormente conferidos são preservados se o placar não mudou. Falhas permanecem disponíveis para nova tentativa.
- **Arremessos CBI:** 2 pontos, 3 pontos e lances livres são usados para validar a pontuação individual. As tentativas e conversões de quadra só entram nos gráficos quando os campos existem, são não negativos, os acertos não superam as tentativas e a soma das cestas explica os pontos do atleta. A cobertura de súmulas é mostrada por equipe e pode ser parcial.

Dados ausentes não representam zero. Resultados e indicadores são descritivos da amostra e não são uma previsão de vitória. A fonte de cada partida está acessível no site.

## Atualizar e gerar o site

```bash
python -m cbb.extractors.cbi_observed
python -m cbb export
```

O coletor descobre as competições e fases publicadas, reúne os resultados e tenta até 40 súmulas adicionais por execução, em até três consultas simultâneas, distribuindo as tentativas entre competições. Resultados conferidos são armazenados em `docs/exports/cbi_observed.json`; a coleta é incremental. O comando `python -m cbb sync` também aciona esta atualização. O GitHub Actions do projeto executa a sincronização programada e regenera os arquivos estáticos.

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
python -m cbb export
```

A exportação gera `index.html` e `docs/index.html` com os dados incorporados. Para executar as verificações de desenvolvimento, instale `pytest` e rode `python -m pytest -q`.

## Análises disponíveis

Na aba **Análises**, os mesmos filtros de competição e equipe alimentam eFG%, frequência de 3 pontos, FTR e TS% quando os dados necessários existem. A distribuição por atleta mostra fatias observadas e, para períodos NBB com pelo menos 20 tentativas em três jogos e referência nos outros períodos, um ajuste com 20 tentativas equivalentes. O mapa NBB utiliza coordenadas relativas do relatório da LNB; a base CBI ainda não tem coordenadas. Comparações mostram o tamanho das amostras e confrontos realmente registrados.

O modelo de Markov anterior está disponível como **exemplo didático com parâmetros hipotéticos**, sem atribuir suas probabilidades à equipe selecionada. Ratings por posse, perdas, rebotes e probabilidades de vitória ao longo do jogo dependem de dados adicionais e não são apresentados como fatos quando a cobertura é insuficiente.
