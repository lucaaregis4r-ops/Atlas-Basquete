"""
Catalog of basketball statistical metrics and scientific citations.
Grounded in peer-reviewed basketball literature:
- Oliver (2004): Basketball on Paper
- Kubatko, Oliver, Pelton, Rosenbaum (2007): A Starting Point for Analyzing Basketball Statistics (JQAS)
- Goldsberry (2012, 2019): CourtVision & SprawlBall
- Cervone, D'Amour, Bornn, Goldsberry (2014, 2016): POINTWISE & Multiresolution Stochastic Process (JASA)
- Sandholtz & Bornn (2020): Markov Decision Processes and Shot Selection in Basketball
- Hollinger (2005) & FIBA Official Rules: Game Score & Performance Index Rating (PIR)
- Stern (1994) & Deshpande & Jensen (2016): In-game Win Probability & Leverage Index
"""
from typing import Dict, Any

METRIC_CATALOG: Dict[str, Dict[str, Any]] = {
    # ------------------ FOUR FACTORS & POSSESSION ------------------
    "possessions": {
        "name": "Posse de Bola Estimada (Poss)",
        "category": "Four Factors & Posse",
        "formula": "Poss ≈ FGA + 0.44 * FTA - ORB + TOV",
        "description": "Estimativa canônica do número de posses ofensivas concluídas por equipe.",
        "citation": "Oliver, D. (2004). Basketball on Paper; Kubatko et al. (2007).",
        "type": "modelado",
        "benchmark": "72 a 82 posses em jogos FIBA de 40 minutos",
    },
    "pace": {
        "name": "Ritmo de Jogo (Pace 40m)",
        "category": "Four Factors & Posse",
        "formula": "Pace = 40 * (Poss_A + Poss_B) / (2 * (MP / 5))",
        "description": "Ritmo padronizado para 40 minutos oficiais FIBA (ao contrário dos 48 min da NBA).",
        "citation": "Oliver, D. (2004); FIBA Official Statistics Standard.",
        "type": "modelado",
        "benchmark": "Média nacional: ~74.5 posses / 40 min",
    },
    "efg_pct": {
        "name": "Aproveitamento Efetivo de Arremessos (eFG%)",
        "category": "Four Factors (Peso 40%)",
        "formula": "eFG% = (FGM + 0.5 * 3PM) / FGA",
        "description": "Fator #1 de Oliver. Ajusta a eficiência considerando que arremessos de 3 pontos valem 50% mais que os de 2.",
        "citation": "Oliver, D. (2004). Basketball on Paper.",
        "type": "observado_ponderado",
        "benchmark": "Elite > 54.0%, Médio 50.0%, Fraco < 46.0%",
    },
    "tov_pct": {
        "name": "Taxa de Desperdício de Posse (TOV%)",
        "category": "Four Factors (Peso 25%)",
        "formula": "TOV% = TOV / (FGA + 0.44 * FTA + TOV)",
        "description": "Fator #2 de Oliver. Percentual de posses encerradas em erro não forçado ou perda de posse.",
        "citation": "Oliver, D. (2004); Kubatko et al. (2007).",
        "type": "modelado",
        "benchmark": "Elite < 12.5%, Médio 14.5%, Alto > 17.0%",
    },
    "orb_pct": {
        "name": "Taxa de Rebote Ofensivo (ORB%)",
        "category": "Four Factors (Peso 20%)",
        "formula": "ORB% = ORB / (ORB + Opp_DRB)",
        "description": "Fator #3 de Oliver. Percentual de rebotes de ataque capturados em relação ao total de oportunidades disponíveis.",
        "citation": "Oliver, D. (2004).",
        "type": "observado_relativo",
        "benchmark": "Elite > 30.0%, Médio 25.0%, Baixo < 20.0%",
    },
    "ftr": {
        "name": "Taxa de Lances Livres (FTR)",
        "category": "Four Factors (Peso 15%)",
        "formula": "FTR = FTA / FGA",
        "description": "Fator #4 de Oliver. Capacidade de agredir a cesta, forçar faltas e converter visitas à linha de lance livre.",
        "citation": "Oliver, D. (2004).",
        "type": "observado_relativo",
        "benchmark": "Alto > 0.28, Médio 0.22, Baixo < 0.17",
    },
    "ortg": {
        "name": "Eficiência Ofensiva (Offensive Rating / ORtg)",
        "category": "Eficiência Geral",
        "formula": "ORtg = 100 * (PTS / Poss)",
        "description": "Pontos produzidos a cada 100 posses de bola. Remove distorções de ritmo (Pace).",
        "citation": "Oliver, D. (2004); Kubatko et al. (2007).",
        "type": "modelado",
        "benchmark": "Elite > 112.0, Médio 104.0, Baixo < 96.0",
    },
    "drtg": {
        "name": "Eficiência Defensiva (Defensive Rating / DRtg)",
        "category": "Eficiência Geral",
        "formula": "DRtg = 100 * (Opp_PTS / Opp_Poss)",
        "description": "Pontos permitidos a cada 100 posses do adversário.",
        "citation": "Oliver, D. (2004); Kubatko et al. (2007).",
        "type": "modelado",
        "benchmark": "Elite < 98.0, Médio 104.0, Fraco > 112.0",
    },
    "net_rating": {
        "name": "Saldo de Eficiência Líquido (Net Rating)",
        "category": "Eficiência Geral",
        "formula": "NetRtg = ORtg - DRtg",
        "description": "Diferencial de pontos por 100 posses. O melhor preditor de qualidade global de uma equipe.",
        "citation": "Oliver, D. (2004).",
        "type": "modelado",
        "benchmark": "Campeão > +8.0, Playoff +1.5 a +6.0, Negativo < 0.0",
    },
    "pythagorean_win_pct": {
        "name": "Expectativa Pitagórica de Vitória (Pyth Win%)",
        "category": "Modelagem Preditiva",
        "formula": "ExpWin% = ORtg^13.91 / (ORtg^13.91 + DRtg^13.91)",
        "description": "Projeção do aproveitamento justo da equipe sem ruído de sorte em jogos fechados.",
        "citation": "Morey, D. (2004); Oliver, D. (2004).",
        "type": "modelado",
        "benchmark": "Correlação r > 0.93 com vitórias finais",
    },

    # ------------------ ATLETAS / ADVANCED INDIVIDUAL ------------------
    "ts_pct": {
        "name": "True Shooting Percentage (TS%)",
        "category": "Aproveitamento Individual",
        "formula": "TS% = PTS / (2 * (FGA + 0.44 * FTA))",
        "description": "Mede a eficiência pontuadora total do atleta ponderando arremessos de 2pts, 3pts e lances livres.",
        "citation": "Kubatko et al. (2007).",
        "type": "observado_ponderado",
        "benchmark": "Elite > 58.0%, Médio 52.0%, Baixo < 47.0%",
    },
    "usg_pct": {
        "name": "Taxa de Uso de Posse (USG%)",
        "category": "Volume & Carga",
        "formula": "USG% = 100 * ((FGA + 0.44*FTA + TOV) * (TmMP/5)) / (MP * (TmFGA + 0.44*TmFTA + TmTOV))",
        "description": "Percentual das posses de equipe finalizadas pelo atleta enquanto esteve em quadra.",
        "citation": "Kubatko et al. (2007).",
        "type": "modelado",
        "benchmark": "Principal opção ofensiva > 26%, Médio 18-22%, Coadjuvante < 15%",
    },
    "ast_pct": {
        "name": "Taxa de Assistências (AST%)",
        "category": "Criação de Jogadas",
        "formula": "AST% = 100 * AST / (((MP / (TmMP/5)) * TmFGM) - FGM)",
        "description": "Estimativa do percentual de cestas de quadra dos companheiros assistidas pelo atleta.",
        "citation": "Oliver, D. (2004); Kubatko et al. (2007).",
        "type": "modelado",
        "benchmark": "Armadores de elite > 32%, Alas criadores > 18%",
    },
    "fiba_pir": {
        "name": "Performance Index Rating FIBA (PIR / Eficiência)",
        "category": "Índices Compostos",
        "formula": "PIR = (PTS + REB + AST + STL + BLK + FR) - ((FGA - FGM) + (FTA - FTM) + TOV + FC)",
        "description": "Índice oficial de valorização FIBA adotado pela CBB e NBB em súmulas e premiações.",
        "citation": "FIBA Official Rules (2024); EuroLeague Official PIR.",
        "type": "observado_composto",
        "benchmark": "MVP > 19.0 / jogo, Sólido 12.0 - 16.0",
    },
    "game_score": {
        "name": "Game Score de Hollinger (GmSc)",
        "category": "Índices Compostos",
        "formula": "GmSc = PTS + 0.4*FGM - 0.7*FGA - 0.4*(FTA-FTM) + 0.7*ORB + 0.3*DRB + STL + 0.7*AST + 0.7*BLK - 0.4*FC - TOV",
        "description": "Métrica ponderada desenvolvida por John Hollinger calibrando o peso estatístico de cada ação individual.",
        "citation": "Hollinger, J. (2005). Pro Basketball Forecast.",
        "type": "modelado",
        "benchmark": "Excelente > 15.0, Médio 9.0, Ruim < 4.0",
    },
    "wilson_ci": {
        "name": "Intervalo de Confiança de Wilson & Shrinkage Bayesiano",
        "category": "Incerteza e Estabilidade Amostral",
        "formula": "(p + z^2/(2n) ± z*sqrt((p(1-p) + z^2/(4n))/n)) / (1 + z^2/n)",
        "description": "Corrige flutuações em atletas com baixa amostra de arremessos (ex: 3 de 4 bolas de 3pts = 75%), regredindo a média para o prior da liga.",
        "citation": "Wilson, E. B. (1927); Gelman et al. (2013) Bayesian Data Analysis.",
        "type": "modelado_probabilistico",
        "benchmark": "Intervalo a 95% de confiança",
    },

    # ------------------ MARKOV & ESPACIAL ------------------
    "markov_epv": {
        "name": "Expected Possession Value via Cadeia de Markov (EPV)",
        "category": "Cadeias de Markov",
        "formula": "v = (I - Q)^(-1) * R_reward",
        "description": "Valor esperado de pontos a partir de um estado estocástico (perímetro, infiltração, post-up, rebote ofensivo).",
        "citation": "Sandholtz & Bornn (2020); Cervone et al. (2016) JASA.",
        "type": "estocastico_absorvente",
        "benchmark": "Infiltração na pintura: ~1.18 pts/posse vs 3PT aberto: ~1.11 pts vs Mid-range contestado: ~0.78 pts",
    },
    "shot_efficiency_surplus": {
        "name": "Superávit de Eficiência Espacial (SES)",
        "category": "Eficiência Espacial (Goldsberry)",
        "formula": "SES = (FGM * PointValue) - (FGA * LeaguePPS_zone)",
        "description": "Pontos ganhos ou perdidos em uma zona da quadra em relação à média de arremesso da liga brasileira.",
        "citation": "Goldsberry, K. (2012). CourtVision; Goldsberry, K. (2019). SprawlBall.",
        "type": "espacial_relativo",
        "benchmark": "Zonas quentes SES > +0.15 pts/arr, Zonas frias SES < -0.15 pts/arr",
    },
    "win_probability": {
        "name": "Probabilidade de Vitória em Tempo Real (WP & WPA)",
        "category": "Modelagem Preditiva In-Game",
        "formula": "WP = Φ((Δpts + μ_pos) / (σ * sqrt(t_rem / 40)))",
        "description": "Curva contínua de probabilidade de vitória posse a posse baseada na diferença de placar e tempo restante.",
        "citation": "Stern, H. (1994); Deshpande & Jensen (2016).",
        "type": "modelado_probabilistico",
        "benchmark": "0.0% a 100.0%",
    },
}
