"""
Comprehensive Multi-Competition & Multi-Season Dataset for Brazilian Basketball.
Covers:
- Temporadas: 2026–2027 (Atual), 2025–2026 (Transição), 2024–2025 (Histórico/Tricampeonato Franca)
- NBB Caixa & Copa Super 8 (Elite Adulta)
- CBI Sub-19 Masculino & Feminino (Campeonato Brasileiro Interclubes)
- CBI Sub-17 Masculino & Feminino (Campeonato Brasileiro Interclubes)
- CBI Super 15 (Sub-15) Masculino & Feminino (Campeonato Brasileiro Interclubes)
- Brasileirão CBB Adulto (Campeonato Brasileiro de Clubes CBB)
- LDB Sub-22 (Liga de Desenvolvimento de Basquete)
- Seleções Brasileiras CBB
"""
from typing import Dict, List, Any
import hashlib
import random
import math
from cbb.analysis.four_factors import compute_four_factors
from cbb.analysis.player_advanced import compute_player_advanced_metrics
from cbb.analysis.shot_efficiency import classify_shot_zone, compute_zone_efficiency
from cbb.court.generator import compute_hexbin_analytics

AVAILABLE_SEASONS: List[Dict[str, Any]] = [
    {
        "id": "2026-2027",
        "name": "2026–2027",
        "label": "2026–2027 (Atual)",
        "year_short": "26/27",
        "is_current": True,
        "description": "Temporada vigente: renovação tática, consolidação de jovens talentos da LDB e transição rápida."
    },
    {
        "id": "2025-2026",
        "name": "2025–2026",
        "label": "2025–2026",
        "year_short": "25/26",
        "is_current": False,
        "description": "Temporada de transição: ascensão de Nathan Mariano e Paulo Zu, transferência de Márcio Santos para a Liga ACB (Espanha) e aceleração de arremessos precoces."
    },
    {
        "id": "2024-2025",
        "name": "2024–2025",
        "label": "2024–2025",
        "year_short": "24/25",
        "is_current": False,
        "description": "Temporada histórica: Sesi Franca tricampeão com domínio físico no garrafão (Márcio Santos + Lucas Dias MVP) e jogo cadenciado de meia quadra."
    }
]

COMPETITIONS_DATA: List[Dict[str, Any]] = [
    # ---------------- 1. NBB CAIXA & COPA SUPER 8 (2026–2027) ----------------
    {
        "id": "nbb",
        "base_id": "nbb",
        "season": "2026–2027",
        "season_id": "2026-2027",
        "name": "NBB Caixa 2026–2027",
        "category": "Elite Profissional Masculina",
        "organizer": "LNB / CBB",
        "teams": [
            {
                "name": "Flamengo",
                "short_name": "FLA",
                "city": "Rio de Janeiro, RJ",
                "coach": "Gustavo De Conti",
                "ortg_base": 114.2, "drtg_base": 98.4, "pace_base": 76.8,
                "color": "#c5221f", "accent": "#000000",
                "clutch": {"win_pct": 0.727, "pts": 8.4, "efg_pct": 0.545, "ft_pct": 0.820, "tov_rate": 0.098},
                "shot_clock": {"early_0_6s": {"freq": 0.22, "efg": 0.590}, "middle_7_18s": {"freq": 0.61, "efg": 0.535}, "late_19_24s": {"freq": 0.17, "efg": 0.420}},
                "splits": {"catch_shoot_3p": 0.395, "pullup_3p": 0.340, "open_fg": 0.560, "contested_fg": 0.435, "rim_fg": 0.645, "short_mid_fg": 0.425, "long_mid_fg": 0.390, "corner3_fg": 0.410, "above3_fg": 0.365},
                "playmaking": {"ast_tov_ratio": 1.78, "potential_ast": 32.5, "secondary_ast": 6.8},
                "defense": {"rim_def_fg": 0.520, "stl_pct": 8.5, "blk_pct": 4.2, "pf_per_40": 17.5, "fd_per_40": 19.8},
                "roster": [
                    {"name": "Franco Baralle", "num": "3", "pos": "Armador", "pts": 14.2, "reb": 3.8, "ast": 6.5, "fg3_pct": 0.382, "fg2_pct": 0.510, "ft_pct": 0.840, "mp": 28.5},
                    {"name": "Gui Deodato", "num": "1", "pos": "Ala", "pts": 15.8, "reb": 4.5, "ast": 2.8, "fg3_pct": 0.405, "fg2_pct": 0.545, "ft_pct": 0.825, "mp": 29.2},
                    {"name": "Alexey Borges", "num": "4", "pos": "Armador", "pts": 12.4, "reb": 3.1, "ast": 5.8, "fg3_pct": 0.365, "fg2_pct": 0.490, "ft_pct": 0.790, "mp": 24.0},
                    {"name": "Kayo Gonçalves", "num": "10", "pos": "Ala-Pivô", "pts": 11.5, "reb": 6.8, "ast": 1.4, "fg3_pct": 0.390, "fg2_pct": 0.560, "ft_pct": 0.760, "mp": 25.5},
                    {"name": "Shaq Johnson", "num": "11", "pos": "Ala-Armador", "pts": 13.9, "reb": 4.2, "ast": 3.1, "fg3_pct": 0.355, "fg2_pct": 0.525, "ft_pct": 0.810, "mp": 26.8},
                    {"name": "Lucas Siewert", "num": "9", "pos": "Ala-Pivô", "pts": 9.8, "reb": 4.9, "ast": 1.1, "fg3_pct": 0.412, "fg2_pct": 0.530, "ft_pct": 0.850, "mp": 20.0},
                    {"name": "Taya Gallizzi", "num": "83", "pos": "Pivô", "pts": 10.4, "reb": 7.2, "ast": 1.0, "fg3_pct": 0.000, "fg2_pct": 0.635, "ft_pct": 0.680, "mp": 22.0},
                ]
            },
            {
                "name": "Sesi Franca",
                "short_name": "FRA",
                "city": "Franca, SP",
                "coach": "Helinho Garcia",
                "ortg_base": 115.8, "drtg_base": 99.8, "pace_base": 74.5,
                "color": "#1a4731", "accent": "#d4af37",
                "clutch": {"win_pct": 0.769, "pts": 9.2, "efg_pct": 0.560, "ft_pct": 0.845, "tov_rate": 0.089},
                "shot_clock": {"early_0_6s": {"freq": 0.19, "efg": 0.595}, "middle_7_18s": {"freq": 0.66, "efg": 0.550}, "late_19_24s": {"freq": 0.15, "efg": 0.445}},
                "splits": {"catch_shoot_3p": 0.415, "pullup_3p": 0.370, "open_fg": 0.575, "contested_fg": 0.450, "rim_fg": 0.655, "short_mid_fg": 0.440, "long_mid_fg": 0.415, "corner3_fg": 0.430, "above3_fg": 0.380},
                "playmaking": {"ast_tov_ratio": 1.95, "potential_ast": 35.0, "secondary_ast": 8.2},
                "defense": {"rim_def_fg": 0.510, "stl_pct": 7.8, "blk_pct": 4.8, "pf_per_40": 16.8, "fd_per_40": 20.2},
                "roster": [
                    {"name": "Lucas Dias", "num": "9", "pos": "Ala-Pivô", "pts": 19.5, "reb": 7.8, "ast": 2.9, "fg3_pct": 0.418, "fg2_pct": 0.565, "ft_pct": 0.865, "mp": 32.0},
                    {"name": "Georginho de Paula", "num": "32", "pos": "Armador", "pts": 16.4, "reb": 8.2, "ast": 7.4, "fg3_pct": 0.360, "fg2_pct": 0.535, "ft_pct": 0.780, "mp": 33.5},
                    {"name": "David Jackson", "num": "7", "pos": "Ala-Armador", "pts": 14.1, "reb": 3.9, "ast": 3.5, "fg3_pct": 0.435, "fg2_pct": 0.540, "ft_pct": 0.915, "mp": 27.8},
                    {"name": "Didi Louzada", "num": "0", "pos": "Ala", "pts": 13.8, "reb": 4.6, "ast": 2.3, "fg3_pct": 0.375, "fg2_pct": 0.520, "ft_pct": 0.770, "mp": 26.5},
                    {"name": "Márcio Santos", "num": "3", "pos": "Pivô", "pts": 11.2, "reb": 6.5, "ast": 1.2, "fg3_pct": 0.280, "fg2_pct": 0.640, "ft_pct": 0.720, "mp": 21.0},
                    {"name": "Santiago Scala", "num": "6", "pos": "Armador", "pts": 8.9, "reb": 2.1, "ast": 4.1, "fg3_pct": 0.395, "fg2_pct": 0.460, "ft_pct": 0.880, "mp": 18.5},
                ]
            },
            {
                "name": "Minas Tênis Clube",
                "short_name": "MTC",
                "city": "Belo Horizonte, MG",
                "coach": "Léo Costa",
                "ortg_base": 113.5, "drtg_base": 100.2, "pace_base": 75.2,
                "color": "#002d62", "accent": "#ffffff",
                "clutch": {"win_pct": 0.688, "pts": 7.8, "efg_pct": 0.530, "ft_pct": 0.810, "tov_rate": 0.105},
                "shot_clock": {"early_0_6s": {"freq": 0.21, "efg": 0.580}, "middle_7_18s": {"freq": 0.62, "efg": 0.530}, "late_19_24s": {"freq": 0.17, "efg": 0.415}},
                "splits": {"catch_shoot_3p": 0.390, "pullup_3p": 0.335, "open_fg": 0.550, "contested_fg": 0.430, "rim_fg": 0.635, "short_mid_fg": 0.415, "long_mid_fg": 0.385, "corner3_fg": 0.405, "above3_fg": 0.360},
                "playmaking": {"ast_tov_ratio": 1.72, "potential_ast": 31.8, "secondary_ast": 6.4},
                "defense": {"rim_def_fg": 0.525, "stl_pct": 8.1, "blk_pct": 4.4, "pf_per_40": 18.0, "fd_per_40": 19.5},
                "roster": [
                    {"name": "Franco Baralle", "num": "5", "pos": "Armador", "pts": 13.6, "reb": 3.4, "ast": 5.9, "fg3_pct": 0.370, "fg2_pct": 0.495, "ft_pct": 0.830, "mp": 27.5},
                    {"name": "Danilo Fuzaro", "num": "24", "pos": "Ala", "pts": 14.8, "reb": 4.7, "ast": 2.6, "fg3_pct": 0.380, "fg2_pct": 0.530, "ft_pct": 0.790, "mp": 28.0},
                    {"name": "Paranhos", "num": "13", "pos": "Pivô", "pts": 12.0, "reb": 8.5, "ast": 1.3, "fg3_pct": 0.000, "fg2_pct": 0.615, "ft_pct": 0.690, "mp": 24.5},
                    {"name": "Chuzito González", "num": "8", "pos": "Ala-Armador", "pts": 15.2, "reb": 3.0, "ast": 2.7, "fg3_pct": 0.420, "fg2_pct": 0.505, "ft_pct": 0.870, "mp": 26.0},
                    {"name": "Renan Lenz", "num": "17", "pos": "Ala-Pivô", "pts": 9.4, "reb": 5.1, "ast": 1.5, "fg3_pct": 0.365, "fg2_pct": 0.520, "ft_pct": 0.750, "mp": 21.0},
                ]
            },
            {
                "name": "São Paulo FC",
                "short_name": "SPFC",
                "city": "São Paulo, SP",
                "coach": "Guerrinha",
                "ortg_base": 109.8, "drtg_base": 104.5, "pace_base": 74.0,
                "color": "#da251c", "accent": "#000000",
                "clutch": {"win_pct": 0.583, "pts": 7.1, "efg_pct": 0.510, "ft_pct": 0.815, "tov_rate": 0.112},
                "shot_clock": {"early_0_6s": {"freq": 0.18, "efg": 0.565}, "middle_7_18s": {"freq": 0.64, "efg": 0.510}, "late_19_24s": {"freq": 0.18, "efg": 0.395}},
                "splits": {"catch_shoot_3p": 0.375, "pullup_3p": 0.330, "open_fg": 0.540, "contested_fg": 0.415, "rim_fg": 0.620, "short_mid_fg": 0.405, "long_mid_fg": 0.380, "corner3_fg": 0.395, "above3_fg": 0.350},
                "playmaking": {"ast_tov_ratio": 1.58, "potential_ast": 29.5, "secondary_ast": 5.5},
                "defense": {"rim_def_fg": 0.545, "stl_pct": 7.5, "blk_pct": 3.9, "pf_per_40": 19.2, "fd_per_40": 18.8},
                "roster": [
                    {"name": "Ricardo Fischer", "num": "5", "pos": "Armador", "pts": 14.5, "reb": 3.2, "ast": 6.8, "fg3_pct": 0.375, "fg2_pct": 0.485, "ft_pct": 0.860, "mp": 29.0},
                    {"name": "Betinho", "num": "3", "pos": "Ala", "pts": 13.9, "reb": 4.1, "ast": 2.4, "fg3_pct": 0.395, "fg2_pct": 0.510, "ft_pct": 0.835, "mp": 27.5},
                    {"name": "Miller", "num": "33", "pos": "Ala-Armador", "pts": 15.6, "reb": 3.8, "ast": 2.9, "fg3_pct": 0.350, "fg2_pct": 0.530, "ft_pct": 0.810, "mp": 28.5},
                    {"name": "Tyrone Curnell", "num": "0", "pos": "Ala-Pivô", "pts": 12.8, "reb": 6.4, "ast": 2.1, "fg3_pct": 0.360, "fg2_pct": 0.540, "ft_pct": 0.770, "mp": 26.0},
                    {"name": "Vitor Faverani", "num": "13", "pos": "Pivô", "pts": 10.5, "reb": 7.0, "ast": 1.2, "fg3_pct": 0.250, "fg2_pct": 0.590, "ft_pct": 0.710, "mp": 20.5},
                ]
            }
        ]
    },

    # ---------------- 2. CBI SUB-19 (CAMPEONATO BRASILEIRO INTERCLUBES 2026) ----------------
    {
        "id": "cbi-sub19",
        "base_id": "cbi-sub19",
        "season": "2026–2027",
        "season_id": "2026-2027",
        "name": "CBI Sub-19 2026 (Safra 2007/08)",
        "category": "Campeonato Brasileiro Interclubes de Base (CBB / CBC)",
        "organizer": "CBB & CBC",
        "teams": [
            {
                "name": "Paulistano Sub-19",
                "short_name": "CAP-19",
                "city": "São Paulo, SP",
                "coach": "Demétrius / Beto",
                "ortg_base": 112.4, "drtg_base": 94.2, "pace_base": 78.5,
                "color": "#c8102e", "accent": "#ffffff",
                "clutch": {"win_pct": 0.833, "pts": 8.8, "efg_pct": 0.550, "ft_pct": 0.790, "tov_rate": 0.115},
                "shot_clock": {"early_0_6s": {"freq": 0.26, "efg": 0.610}, "middle_7_18s": {"freq": 0.58, "efg": 0.525}, "late_19_24s": {"freq": 0.16, "efg": 0.390}},
                "splits": {"catch_shoot_3p": 0.380, "pullup_3p": 0.320, "open_fg": 0.555, "contested_fg": 0.420, "rim_fg": 0.630, "short_mid_fg": 0.410, "long_mid_fg": 0.370, "corner3_fg": 0.390, "above3_fg": 0.345},
                "playmaking": {"ast_tov_ratio": 1.62, "potential_ast": 33.0, "secondary_ast": 7.0},
                "defense": {"rim_def_fg": 0.490, "stl_pct": 9.8, "blk_pct": 5.2, "pf_per_40": 19.0, "fd_per_40": 21.0},
                "roster": [
                    {"name": "Vitinho Silva", "num": "7", "pos": "Armador", "pts": 17.5, "reb": 4.8, "ast": 7.8, "fg3_pct": 0.385, "fg2_pct": 0.520, "ft_pct": 0.810, "mp": 31.0},
                    {"name": "Gabriel Landeira", "num": "11", "pos": "Ala-Armador", "pts": 16.2, "reb": 5.1, "ast": 3.4, "fg3_pct": 0.395, "fg2_pct": 0.535, "ft_pct": 0.830, "mp": 29.5},
                    {"name": "Breno Silva", "num": "15", "pos": "Pivô", "pts": 13.8, "reb": 10.2, "ast": 1.4, "fg3_pct": 0.000, "fg2_pct": 0.640, "ft_pct": 0.690, "mp": 27.0},
                    {"name": "Murilo Brandão", "num": "8", "pos": "Ala", "pts": 12.4, "reb": 5.5, "ast": 2.2, "fg3_pct": 0.360, "fg2_pct": 0.505, "ft_pct": 0.770, "mp": 25.0},
                ]
            },
            {
                "name": "Pinheiros Sub-19",
                "short_name": "ECP-19",
                "city": "São Paulo, SP",
                "coach": "David Pelosini",
                "ortg_base": 111.0, "drtg_base": 96.5, "pace_base": 79.2,
                "color": "#00205b", "accent": "#0080ff",
                "clutch": {"win_pct": 0.750, "pts": 8.0, "efg_pct": 0.535, "ft_pct": 0.775, "tov_rate": 0.120},
                "shot_clock": {"early_0_6s": {"freq": 0.28, "efg": 0.615}, "middle_7_18s": {"freq": 0.56, "efg": 0.515}, "late_19_24s": {"freq": 0.16, "efg": 0.385}},
                "splits": {"catch_shoot_3p": 0.375, "pullup_3p": 0.325, "open_fg": 0.545, "contested_fg": 0.410, "rim_fg": 0.625, "short_mid_fg": 0.400, "long_mid_fg": 0.365, "corner3_fg": 0.385, "above3_fg": 0.340},
                "playmaking": {"ast_tov_ratio": 1.55, "potential_ast": 31.5, "secondary_ast": 6.5},
                "defense": {"rim_def_fg": 0.505, "stl_pct": 9.4, "blk_pct": 5.0, "pf_per_40": 19.5, "fd_per_40": 20.5},
                "roster": [
                    {"name": "Enrico Borio", "num": "10", "pos": "Ala-Pivô", "pts": 18.2, "reb": 8.9, "ast": 2.8, "fg3_pct": 0.360, "fg2_pct": 0.550, "ft_pct": 0.790, "mp": 30.5},
                    {"name": "Tiago Faria", "num": "5", "pos": "Armador", "pts": 14.8, "reb": 3.5, "ast": 7.2, "fg3_pct": 0.370, "fg2_pct": 0.490, "ft_pct": 0.825, "mp": 28.0},
                    {"name": "Agapy Santos", "num": "23", "pos": "Pivô", "pts": 12.5, "reb": 9.8, "ast": 1.1, "fg3_pct": 0.000, "fg2_pct": 0.620, "ft_pct": 0.660, "mp": 26.0},
                ]
            },
            {
                "name": "Minas TC Sub-19",
                "short_name": "MTC-19",
                "city": "Belo Horizonte, MG",
                "coach": "Flávio Davis",
                "ortg_base": 109.5, "drtg_base": 98.0, "pace_base": 77.0,
                "color": "#002d62", "accent": "#ffffff",
                "clutch": {"win_pct": 0.667, "pts": 7.5, "efg_pct": 0.520, "ft_pct": 0.760, "tov_rate": 0.125},
                "shot_clock": {"early_0_6s": {"freq": 0.24, "efg": 0.590}, "middle_7_18s": {"freq": 0.59, "efg": 0.510}, "late_19_24s": {"freq": 0.17, "efg": 0.380}},
                "splits": {"catch_shoot_3p": 0.365, "pullup_3p": 0.315, "open_fg": 0.535, "contested_fg": 0.405, "rim_fg": 0.615, "short_mid_fg": 0.395, "long_mid_fg": 0.360, "corner3_fg": 0.375, "above3_fg": 0.335},
                "playmaking": {"ast_tov_ratio": 1.48, "potential_ast": 30.0, "secondary_ast": 6.0},
                "defense": {"rim_def_fg": 0.515, "stl_pct": 9.0, "blk_pct": 4.6, "pf_per_40": 20.0, "fd_per_40": 20.0},
                "roster": [
                    {"name": "Danilo Gomes", "num": "6", "pos": "Ala", "pts": 16.5, "reb": 6.2, "ast": 3.1, "fg3_pct": 0.380, "fg2_pct": 0.515, "ft_pct": 0.785, "mp": 29.0},
                    {"name": "Lucas Rodriguez", "num": "4", "pos": "Armador", "pts": 13.0, "reb": 3.2, "ast": 6.4, "fg3_pct": 0.355, "fg2_pct": 0.480, "ft_pct": 0.810, "mp": 27.5},
                    {"name": "Winicius Braga", "num": "14", "pos": "Pivô", "pts": 11.8, "reb": 8.5, "ast": 1.2, "fg3_pct": 0.000, "fg2_pct": 0.610, "ft_pct": 0.670, "mp": 25.0},
                ]
            },
            {
                "name": "Tijuca TC Sub-19",
                "short_name": "TIJ-19",
                "city": "Rio de Janeiro, RJ",
                "coach": "Léo Figueiró",
                "ortg_base": 108.0, "drtg_base": 97.5, "pace_base": 78.0,
                "color": "#b91c1c", "accent": "#ffffff",
                "clutch": {"win_pct": 0.625, "pts": 7.2, "efg_pct": 0.510, "ft_pct": 0.760, "tov_rate": 0.125},
                "shot_clock": {"early_0_6s": {"freq": 0.25, "efg": 0.585}, "middle_7_18s": {"freq": 0.58, "efg": 0.510}, "late_19_24s": {"freq": 0.17, "efg": 0.380}},
                "splits": {"catch_shoot_3p": 0.365, "pullup_3p": 0.315, "open_fg": 0.530, "contested_fg": 0.400, "rim_fg": 0.615, "short_mid_fg": 0.395, "long_mid_fg": 0.360, "corner3_fg": 0.375, "above3_fg": 0.335},
                "playmaking": {"ast_tov_ratio": 1.45, "potential_ast": 29.5, "secondary_ast": 5.8},
                "defense": {"rim_def_fg": 0.510, "stl_pct": 9.2, "blk_pct": 4.5, "pf_per_40": 20.0, "fd_per_40": 19.5},
                "roster": [
                    {"name": "Bernardo Calado", "num": "10", "pos": "Ala-Armador", "pts": 15.8, "reb": 4.9, "ast": 3.5, "fg3_pct": 0.370, "fg2_pct": 0.510, "ft_pct": 0.790, "mp": 29.5},
                    {"name": "Caio Veríssimo", "num": "8", "pos": "Armador", "pts": 13.2, "reb": 3.4, "ast": 6.8, "fg3_pct": 0.350, "fg2_pct": 0.475, "ft_pct": 0.820, "mp": 28.0},
                ]
            },
            {
                "name": "Foz Basquete Sub-19 (Fem)",
                "short_name": "FOZ-19",
                "city": "Foz do Iguaçu, PR",
                "coach": "Claudio Lisboa",
                "ortg_base": 109.2, "drtg_base": 95.8, "pace_base": 79.5,
                "color": "#0d9488", "accent": "#ffffff",
                "clutch": {"win_pct": 0.714, "pts": 8.2, "efg_pct": 0.525, "ft_pct": 0.780, "tov_rate": 0.118},
                "shot_clock": {"early_0_6s": {"freq": 0.27, "efg": 0.600}, "middle_7_18s": {"freq": 0.57, "efg": 0.515}, "late_19_24s": {"freq": 0.16, "efg": 0.385}},
                "splits": {"catch_shoot_3p": 0.375, "pullup_3p": 0.320, "open_fg": 0.540, "contested_fg": 0.410, "rim_fg": 0.620, "short_mid_fg": 0.405, "long_mid_fg": 0.365, "corner3_fg": 0.385, "above3_fg": 0.340},
                "playmaking": {"ast_tov_ratio": 1.50, "potential_ast": 31.0, "secondary_ast": 6.2},
                "defense": {"rim_def_fg": 0.495, "stl_pct": 10.2, "blk_pct": 4.8, "pf_per_40": 18.8, "fd_per_40": 20.8},
                "roster": [
                    {"name": "Maria Paula", "num": "9", "pos": "Ala", "pts": 18.5, "reb": 7.4, "ast": 4.2, "fg3_pct": 0.390, "fg2_pct": 0.525, "ft_pct": 0.830, "mp": 31.0},
                    {"name": "Larissa Silva", "num": "4", "pos": "Armadora", "pts": 14.1, "reb": 3.8, "ast": 7.5, "fg3_pct": 0.365, "fg2_pct": 0.485, "ft_pct": 0.800, "mp": 29.0},
                ]
            }
        ]
    },

    # ---------------- 3. CBI SUB-17 (CAMPEONATO BRASILEIRO INTERCLUBES 2026) ----------------
    {
        "id": "cbi-sub17",
        "base_id": "cbi-sub17",
        "season": "2026–2027",
        "season_id": "2026-2027",
        "name": "CBI Sub-17 2026 (Safra 2009/10)",
        "category": "Campeonato Brasileiro Interclubes de Base (CBB / CBC)",
        "organizer": "CBB & CBC",
        "teams": [
            {
                "name": "Paulistano Sub-17 (Campeão Invicto)",
                "short_name": "CAP-17",
                "city": "São Paulo, SP",
                "coach": "Roberto Jayme",
                "ortg_base": 114.5, "drtg_base": 88.5, "pace_base": 82.0,
                "color": "#c8102e", "accent": "#ffffff",
                "clutch": {"win_pct": 1.000, "pts": 9.5, "efg_pct": 0.580, "ft_pct": 0.810, "tov_rate": 0.100},
                "shot_clock": {"early_0_6s": {"freq": 0.32, "efg": 0.640}, "middle_7_18s": {"freq": 0.54, "efg": 0.540}, "late_19_24s": {"freq": 0.14, "efg": 0.410}},
                "splits": {"catch_shoot_3p": 0.395, "pullup_3p": 0.340, "open_fg": 0.575, "contested_fg": 0.440, "rim_fg": 0.660, "short_mid_fg": 0.430, "long_mid_fg": 0.390, "corner3_fg": 0.410, "above3_fg": 0.360},
                "playmaking": {"ast_tov_ratio": 1.82, "potential_ast": 36.0, "secondary_ast": 8.5},
                "defense": {"rim_def_fg": 0.450, "stl_pct": 11.5, "blk_pct": 6.2, "pf_per_40": 18.2, "fd_per_40": 22.4},
                "roster": [
                    {"name": "Eduardo Klafke", "num": "9", "pos": "Ala-Armador", "pts": 21.4, "reb": 6.5, "ast": 4.8, "fg3_pct": 0.420, "fg2_pct": 0.560, "ft_pct": 0.860, "mp": 32.0},
                    {"name": "Lucas Abreu", "num": "7", "pos": "Armador", "pts": 15.6, "reb": 4.1, "ast": 8.5, "fg3_pct": 0.375, "fg2_pct": 0.510, "ft_pct": 0.820, "mp": 30.0},
                    {"name": "Arthur Buerger", "num": "13", "pos": "Ala-Pivô", "pts": 14.8, "reb": 9.2, "ast": 2.1, "fg3_pct": 0.350, "fg2_pct": 0.580, "ft_pct": 0.780, "mp": 28.5},
                ]
            },
            {
                "name": "Instituto MF Feminino (Campeão Sub-17)",
                "short_name": "IMF-17",
                "city": "Joinville, SC",
                "coach": "Camila Silva",
                "ortg_base": 110.8, "drtg_base": 91.0, "pace_base": 80.5,
                "color": "#6b21a8", "accent": "#ffd700",
                "clutch": {"win_pct": 0.875, "pts": 9.0, "efg_pct": 0.540, "ft_pct": 0.825, "tov_rate": 0.108},
                "shot_clock": {"early_0_6s": {"freq": 0.30, "efg": 0.620}, "middle_7_18s": {"freq": 0.56, "efg": 0.520}, "late_19_24s": {"freq": 0.14, "efg": 0.395}},
                "splits": {"catch_shoot_3p": 0.390, "pullup_3p": 0.335, "open_fg": 0.560, "contested_fg": 0.425, "rim_fg": 0.640, "short_mid_fg": 0.415, "long_mid_fg": 0.380, "corner3_fg": 0.400, "above3_fg": 0.355},
                "playmaking": {"ast_tov_ratio": 1.70, "potential_ast": 34.0, "secondary_ast": 7.8},
                "defense": {"rim_def_fg": 0.470, "stl_pct": 10.8, "blk_pct": 5.5, "pf_per_40": 17.8, "fd_per_40": 21.8},
                "roster": [
                    {"name": "Julia Preis (Bola de Ouro Molten)", "num": "10", "pos": "Ala", "pts": 22.8, "reb": 8.4, "ast": 5.2, "fg3_pct": 0.415, "fg2_pct": 0.550, "ft_pct": 0.875, "mp": 33.0},
                    {"name": "Isabela Rocha", "num": "5", "pos": "Armadora", "pts": 14.5, "reb": 4.2, "ast": 8.0, "fg3_pct": 0.380, "fg2_pct": 0.495, "ft_pct": 0.810, "mp": 29.5},
                    {"name": "Marcella Viana", "num": "14", "pos": "Pivô", "pts": 13.2, "reb": 11.5, "ast": 1.8, "fg3_pct": 0.000, "fg2_pct": 0.615, "ft_pct": 0.720, "mp": 28.0},
                ]
            },
            {
                "name": "Corinthians Sub-17",
                "short_name": "COR-17",
                "city": "São Paulo, SP",
                "coach": "Rosana Lopes",
                "ortg_base": 108.5, "drtg_base": 95.0, "pace_base": 81.0,
                "color": "#000000", "accent": "#ffffff",
                "clutch": {"win_pct": 0.667, "pts": 7.6, "efg_pct": 0.515, "ft_pct": 0.770, "tov_rate": 0.122},
                "shot_clock": {"early_0_6s": {"freq": 0.29, "efg": 0.595}, "middle_7_18s": {"freq": 0.56, "efg": 0.505}, "late_19_24s": {"freq": 0.15, "efg": 0.375}},
                "splits": {"catch_shoot_3p": 0.360, "pullup_3p": 0.310, "open_fg": 0.530, "contested_fg": 0.400, "rim_fg": 0.610, "short_mid_fg": 0.390, "long_mid_fg": 0.355, "corner3_fg": 0.370, "above3_fg": 0.330},
                "playmaking": {"ast_tov_ratio": 1.45, "potential_ast": 30.5, "secondary_ast": 6.1},
                "defense": {"rim_def_fg": 0.500, "stl_pct": 9.8, "blk_pct": 4.8, "pf_per_40": 19.5, "fd_per_40": 20.8},
                "roster": [
                    {"name": "Matheus Teles", "num": "8", "pos": "Ala-Armador", "pts": 17.1, "reb": 5.4, "ast": 3.8, "fg3_pct": 0.375, "fg2_pct": 0.520, "ft_pct": 0.795, "mp": 30.0},
                    {"name": "Kauã Santos", "num": "4", "pos": "Armador", "pts": 13.5, "reb": 3.6, "ast": 6.8, "fg3_pct": 0.350, "fg2_pct": 0.485, "ft_pct": 0.815, "mp": 28.0},
                ]
            },
            {
                "name": "Flamengo Sub-17",
                "short_name": "FLA-17",
                "city": "Rio de Janeiro, RJ",
                "coach": "Leonardo Dutra",
                "ortg_base": 111.2, "drtg_base": 93.0, "pace_base": 81.5,
                "color": "#c5221f", "accent": "#000000",
                "clutch": {"win_pct": 0.778, "pts": 8.5, "efg_pct": 0.535, "ft_pct": 0.800, "tov_rate": 0.110},
                "shot_clock": {"early_0_6s": {"freq": 0.31, "efg": 0.625}, "middle_7_18s": {"freq": 0.55, "efg": 0.525}, "late_19_24s": {"freq": 0.14, "efg": 0.400}},
                "splits": {"catch_shoot_3p": 0.385, "pullup_3p": 0.330, "open_fg": 0.555, "contested_fg": 0.420, "rim_fg": 0.635, "short_mid_fg": 0.410, "long_mid_fg": 0.375, "corner3_fg": 0.395, "above3_fg": 0.350},
                "playmaking": {"ast_tov_ratio": 1.60, "potential_ast": 33.5, "secondary_ast": 7.2},
                "defense": {"rim_def_fg": 0.480, "stl_pct": 10.5, "blk_pct": 5.4, "pf_per_40": 18.5, "fd_per_40": 21.5},
                "roster": [
                    {"name": "Yan Djalo", "num": "11", "pos": "Ala-Armador", "pts": 19.4, "reb": 6.8, "ast": 4.5, "fg3_pct": 0.395, "fg2_pct": 0.540, "ft_pct": 0.835, "mp": 31.0},
                    {"name": "Davi Ramos", "num": "5", "pos": "Armador", "pts": 14.2, "reb": 3.8, "ast": 7.6, "fg3_pct": 0.365, "fg2_pct": 0.490, "ft_pct": 0.810, "mp": 29.0},
                ]
            },
            {
                "name": "Bauru Basket Sub-17",
                "short_name": "BAU-17",
                "city": "Bauru, SP",
                "coach": "Hudson Previdelo",
                "ortg_base": 109.0, "drtg_base": 96.5, "pace_base": 79.0,
                "color": "#1e3a8a", "accent": "#f59e0b",
                "clutch": {"win_pct": 0.625, "pts": 7.5, "efg_pct": 0.510, "ft_pct": 0.775, "tov_rate": 0.120},
                "shot_clock": {"early_0_6s": {"freq": 0.27, "efg": 0.590}, "middle_7_18s": {"freq": 0.57, "efg": 0.510}, "late_19_24s": {"freq": 0.16, "efg": 0.380}},
                "splits": {"catch_shoot_3p": 0.370, "pullup_3p": 0.315, "open_fg": 0.535, "contested_fg": 0.405, "rim_fg": 0.615, "short_mid_fg": 0.395, "long_mid_fg": 0.360, "corner3_fg": 0.380, "above3_fg": 0.335},
                "playmaking": {"ast_tov_ratio": 1.48, "potential_ast": 30.0, "secondary_ast": 6.0},
                "defense": {"rim_def_fg": 0.510, "stl_pct": 9.5, "blk_pct": 4.6, "pf_per_40": 19.8, "fd_per_40": 20.0},
                "roster": [
                    {"name": "Gustavo Guimarães", "num": "7", "pos": "Ala", "pts": 17.8, "reb": 6.5, "ast": 3.4, "fg3_pct": 0.380, "fg2_pct": 0.525, "ft_pct": 0.810, "mp": 30.5},
                    {"name": "Otávio Bauru", "num": "4", "pos": "Armador", "pts": 13.0, "reb": 3.4, "ast": 6.5, "fg3_pct": 0.355, "fg2_pct": 0.480, "ft_pct": 0.795, "mp": 27.5},
                ]
            }
        ]
    },

    # ---------------- 4. CBI SUPER 15 (SUB-15 2026) ----------------
    {
        "id": "cbi-sub15",
        "base_id": "cbi-sub15",
        "season": "2026–2027",
        "season_id": "2026-2027",
        "name": "CBI Super 15 (Sub-15) 2026 CBB/CBC",
        "category": "Campeonato Brasileiro Interclubes de Base (CBB / CBC)",
        "organizer": "CBB & CBC",
        "teams": [
            {
                "name": "Pinheiros Sub-15 (Campeão)",
                "short_name": "ECP-15",
                "city": "São Paulo, SP",
                "coach": "Vinicius Ribeiro",
                "ortg_base": 113.0, "drtg_base": 87.0, "pace_base": 84.0,
                "color": "#00205b", "accent": "#0080ff",
                "clutch": {"win_pct": 0.889, "pts": 9.2, "efg_pct": 0.565, "ft_pct": 0.790, "tov_rate": 0.115},
                "shot_clock": {"early_0_6s": {"freq": 0.35, "efg": 0.650}, "middle_7_18s": {"freq": 0.52, "efg": 0.530}, "late_19_24s": {"freq": 0.13, "efg": 0.400}},
                "splits": {"catch_shoot_3p": 0.385, "pullup_3p": 0.325, "open_fg": 0.570, "contested_fg": 0.430, "rim_fg": 0.650, "short_mid_fg": 0.420, "long_mid_fg": 0.370, "corner3_fg": 0.395, "above3_fg": 0.350},
                "playmaking": {"ast_tov_ratio": 1.70, "potential_ast": 35.0, "secondary_ast": 8.0},
                "defense": {"rim_def_fg": 0.440, "stl_pct": 12.5, "blk_pct": 6.8, "pf_per_40": 18.0, "fd_per_40": 23.0},
                "roster": [
                    {"name": "Arthur Mendes", "num": "10", "pos": "Armador", "pts": 20.5, "reb": 5.2, "ast": 8.8, "fg3_pct": 0.395, "fg2_pct": 0.535, "ft_pct": 0.835, "mp": 31.0},
                    {"name": "Felipe Nogueira", "num": "15", "pos": "Pivô", "pts": 16.2, "reb": 12.4, "ast": 2.0, "fg3_pct": 0.000, "fg2_pct": 0.640, "ft_pct": 0.720, "mp": 29.0},
                ]
            },
            {
                "name": "Sociedade Thalia Sub-15",
                "short_name": "THA-15",
                "city": "Curitiba, PR",
                "coach": "Rafael Rossi",
                "ortg_base": 109.5, "drtg_base": 93.5, "pace_base": 82.5,
                "color": "#15803d", "accent": "#ffffff",
                "clutch": {"win_pct": 0.750, "pts": 8.1, "efg_pct": 0.525, "ft_pct": 0.770, "tov_rate": 0.125},
                "shot_clock": {"early_0_6s": {"freq": 0.32, "efg": 0.610}, "middle_7_18s": {"freq": 0.54, "efg": 0.515}, "late_19_24s": {"freq": 0.14, "efg": 0.385}},
                "splits": {"catch_shoot_3p": 0.370, "pullup_3p": 0.315, "open_fg": 0.540, "contested_fg": 0.410, "rim_fg": 0.625, "short_mid_fg": 0.400, "long_mid_fg": 0.360, "corner3_fg": 0.380, "above3_fg": 0.340},
                "playmaking": {"ast_tov_ratio": 1.50, "potential_ast": 31.5, "secondary_ast": 6.8},
                "defense": {"rim_def_fg": 0.485, "stl_pct": 11.0, "blk_pct": 5.2, "pf_per_40": 19.0, "fd_per_40": 21.5},
                "roster": [
                    {"name": "Leonardo Thalia", "num": "7", "pos": "Ala", "pts": 18.0, "reb": 7.5, "ast": 4.0, "fg3_pct": 0.375, "fg2_pct": 0.520, "ft_pct": 0.800, "mp": 30.0},
                    {"name": "Bernardo Silva", "num": "4", "pos": "Armador", "pts": 14.5, "reb": 3.8, "ast": 7.2, "fg3_pct": 0.360, "fg2_pct": 0.485, "ft_pct": 0.810, "mp": 28.5},
                ]
            }
        ]
    },

    # ---------------- 5. LDB SUB-22 (LIGA DE DESENVOLVIMENTO 2026) ----------------
    {
        "id": "ldb-sub22",
        "base_id": "ldb-sub22",
        "season": "2026–2027",
        "season_id": "2026-2027",
        "name": "LDB Sub-22 (Edição 2026)",
        "category": "Principal Liga de Formação Profissional do Brasil",
        "organizer": "LNB & CBB",
        "teams": [
            {
                "name": "Paulistano Sub-22",
                "short_name": "CAP-22",
                "city": "São Paulo, SP",
                "coach": "Beto",
                "ortg_base": 113.8, "drtg_base": 96.0, "pace_base": 78.0,
                "color": "#c8102e", "accent": "#ffffff",
                "clutch": {"win_pct": 0.818, "pts": 8.8, "efg_pct": 0.555, "ft_pct": 0.820, "tov_rate": 0.105},
                "shot_clock": {"early_0_6s": {"freq": 0.25, "efg": 0.615}, "middle_7_18s": {"freq": 0.59, "efg": 0.535}, "late_19_24s": {"freq": 0.16, "efg": 0.410}},
                "splits": {"catch_shoot_3p": 0.395, "pullup_3p": 0.345, "open_fg": 0.565, "contested_fg": 0.435, "rim_fg": 0.645, "short_mid_fg": 0.425, "long_mid_fg": 0.385, "corner3_fg": 0.410, "above3_fg": 0.365},
                "playmaking": {"ast_tov_ratio": 1.75, "potential_ast": 34.0, "secondary_ast": 7.5},
                "defense": {"rim_def_fg": 0.485, "stl_pct": 9.2, "blk_pct": 5.1, "pf_per_40": 18.0, "fd_per_40": 21.0},
                "roster": [
                    {"name": "Kauan Raymundo", "num": "12", "pos": "Ala-Pivô", "pts": 18.6, "reb": 9.2, "ast": 2.5, "fg3_pct": 0.360, "fg2_pct": 0.580, "ft_pct": 0.795, "mp": 31.0},
                    {"name": "Vitinho Silva", "num": "7", "pos": "Armador", "pts": 16.0, "reb": 4.2, "ast": 7.4, "fg3_pct": 0.380, "fg2_pct": 0.510, "ft_pct": 0.840, "mp": 29.5},
                    {"name": "Brunão", "num": "15", "pos": "Pivô", "pts": 13.5, "reb": 10.0, "ast": 1.5, "fg3_pct": 0.000, "fg2_pct": 0.630, "ft_pct": 0.710, "mp": 27.0},
                ]
            },
            {
                "name": "Sesi Franca Sub-22",
                "short_name": "FRA-22",
                "city": "Franca, SP",
                "coach": "Pablo Costa",
                "ortg_base": 114.2, "drtg_base": 97.8, "pace_base": 76.5,
                "color": "#1a4731", "accent": "#d4af37",
                "clutch": {"win_pct": 0.750, "pts": 8.5, "efg_pct": 0.545, "ft_pct": 0.830, "tov_rate": 0.098},
                "shot_clock": {"early_0_6s": {"freq": 0.22, "efg": 0.605}, "middle_7_18s": {"freq": 0.63, "efg": 0.540}, "late_19_24s": {"freq": 0.15, "efg": 0.425}},
                "splits": {"catch_shoot_3p": 0.405, "pullup_3p": 0.355, "open_fg": 0.570, "contested_fg": 0.440, "rim_fg": 0.650, "short_mid_fg": 0.430, "long_mid_fg": 0.400, "corner3_fg": 0.420, "above3_fg": 0.370},
                "playmaking": {"ast_tov_ratio": 1.82, "potential_ast": 34.5, "secondary_ast": 7.8},
                "defense": {"rim_def_fg": 0.505, "stl_pct": 8.2, "blk_pct": 4.8, "pf_per_40": 17.5, "fd_per_40": 20.5},
                "roster": [
                    {"name": "Nathan Mariano", "num": "11", "pos": "Ala-Armador", "pts": 18.2, "reb": 5.5, "ast": 4.2, "fg3_pct": 0.410, "fg2_pct": 0.540, "ft_pct": 0.850, "mp": 30.5},
                    {"name": "Vinicius", "num": "9", "pos": "Ala-Pivô", "pts": 15.1, "reb": 8.4, "ast": 2.2, "fg3_pct": 0.350, "fg2_pct": 0.575, "ft_pct": 0.785, "mp": 28.0},
                ]
            },
            {
                "name": "São José Sub-22",
                "short_name": "SJE-22",
                "city": "São José dos Campos, SP",
                "coach": "Cristiano Ahmed",
                "ortg_base": 109.8, "drtg_base": 100.5, "pace_base": 77.2,
                "color": "#1e40af", "accent": "#facc15",
                "clutch": {"win_pct": 0.600, "pts": 7.3, "efg_pct": 0.515, "ft_pct": 0.780, "tov_rate": 0.115},
                "shot_clock": {"early_0_6s": {"freq": 0.23, "efg": 0.585}, "middle_7_18s": {"freq": 0.60, "efg": 0.515}, "late_19_24s": {"freq": 0.17, "efg": 0.395}},
                "splits": {"catch_shoot_3p": 0.370, "pullup_3p": 0.325, "open_fg": 0.540, "contested_fg": 0.410, "rim_fg": 0.620, "short_mid_fg": 0.405, "long_mid_fg": 0.370, "corner3_fg": 0.385, "above3_fg": 0.345},
                "playmaking": {"ast_tov_ratio": 1.52, "potential_ast": 30.5, "secondary_ast": 6.1},
                "defense": {"rim_def_fg": 0.525, "stl_pct": 8.5, "blk_pct": 4.2, "pf_per_40": 19.0, "fd_per_40": 19.5},
                "roster": [
                    {"name": "Felipe Gregate", "num": "8", "pos": "Ala-Armador", "pts": 16.5, "reb": 4.8, "ast": 3.9, "fg3_pct": 0.375, "fg2_pct": 0.510, "ft_pct": 0.815, "mp": 29.5},
                    {"name": "Gabriel Caldeira", "num": "5", "pos": "Armador", "pts": 13.8, "reb": 3.4, "ast": 6.8, "fg3_pct": 0.360, "fg2_pct": 0.485, "ft_pct": 0.830, "mp": 28.0},
                ]
            }
        ]
    },

    # ---------------- 6. BRASILEIRÃO CBB ADULTO 2026 ----------------
    {
        "id": "brasileirao-cbb",
        "base_id": "brasileirao-cbb",
        "season": "2026–2027",
        "season_id": "2026-2027",
        "name": "Brasileirão CBB Adulto 2026",
        "category": "Campeonato Brasileiro de Clubes Adulto (CBB)",
        "organizer": "Confederação Brasileira de Basketball (CBB)",
        "teams": [
            {
                "name": "Cruzeiro Basquete",
                "short_name": "CRU",
                "city": "Belo Horizonte, MG",
                "coach": "Tiago Perez",
                "ortg_base": 111.5, "drtg_base": 97.2, "pace_base": 76.4,
                "color": "#005ca9", "accent": "#ffffff",
                "clutch": {"win_pct": 0.778, "pts": 8.6, "efg_pct": 0.540, "ft_pct": 0.815, "tov_rate": 0.095},
                "shot_clock": {"early_0_6s": {"freq": 0.23, "efg": 0.590}, "middle_7_18s": {"freq": 0.61, "efg": 0.530}, "late_19_24s": {"freq": 0.16, "efg": 0.415}},
                "splits": {"catch_shoot_3p": 0.390, "pullup_3p": 0.345, "open_fg": 0.560, "contested_fg": 0.430, "rim_fg": 0.635, "short_mid_fg": 0.420, "long_mid_fg": 0.385, "corner3_fg": 0.405, "above3_fg": 0.360},
                "playmaking": {"ast_tov_ratio": 1.75, "potential_ast": 32.0, "secondary_ast": 6.7},
                "defense": {"rim_def_fg": 0.515, "stl_pct": 8.4, "blk_pct": 4.5, "pf_per_40": 17.8, "fd_per_40": 20.0},
                "roster": [
                    {"name": "Pedro Teruel", "num": "10", "pos": "Ala-Armador", "pts": 16.8, "reb": 4.5, "ast": 4.1, "fg3_pct": 0.395, "fg2_pct": 0.530, "ft_pct": 0.840, "mp": 29.5},
                    {"name": "Derick", "num": "15", "pos": "Pivô", "pts": 14.2, "reb": 9.4, "ast": 1.5, "fg3_pct": 0.000, "fg2_pct": 0.635, "ft_pct": 0.710, "mp": 28.0},
                    {"name": "Matheus Leoni", "num": "5", "pos": "Armador", "pts": 12.5, "reb": 3.2, "ast": 6.8, "fg3_pct": 0.365, "fg2_pct": 0.490, "ft_pct": 0.815, "mp": 26.5},
                ]
            },
            {
                "name": "Basquete Santos / Fupes",
                "short_name": "SAN",
                "city": "Santos, SP",
                "coach": "Daniel Leque",
                "ortg_base": 109.8, "drtg_base": 99.5, "pace_base": 75.0,
                "color": "#000000", "accent": "#ffffff",
                "clutch": {"win_pct": 0.625, "pts": 7.4, "efg_pct": 0.515, "ft_pct": 0.785, "tov_rate": 0.110},
                "shot_clock": {"early_0_6s": {"freq": 0.20, "efg": 0.575}, "middle_7_18s": {"freq": 0.63, "efg": 0.515}, "late_19_24s": {"freq": 0.17, "efg": 0.400}},
                "splits": {"catch_shoot_3p": 0.375, "pullup_3p": 0.330, "open_fg": 0.540, "contested_fg": 0.415, "rim_fg": 0.620, "short_mid_fg": 0.405, "long_mid_fg": 0.375, "corner3_fg": 0.390, "above3_fg": 0.345},
                "playmaking": {"ast_tov_ratio": 1.60, "potential_ast": 29.8, "secondary_ast": 5.8},
                "defense": {"rim_def_fg": 0.530, "stl_pct": 7.9, "blk_pct": 4.1, "pf_per_40": 18.5, "fd_per_40": 19.2},
                "roster": [
                    {"name": "Guga Ceccato", "num": "7", "pos": "Armador", "pts": 15.0, "reb": 3.8, "ast": 7.2, "fg3_pct": 0.380, "fg2_pct": 0.505, "ft_pct": 0.835, "mp": 30.0},
                    {"name": "Gabriel", "num": "11", "pos": "Ala", "pts": 14.1, "reb": 5.8, "ast": 2.5, "fg3_pct": 0.365, "fg2_pct": 0.520, "ft_pct": 0.790, "mp": 28.0},
                ]
            },
            {
                "name": "Liga Sorocabana (LSB)",
                "short_name": "LSB",
                "city": "Sorocaba, SP",
                "coach": "Rinaldo Rodrigues",
                "ortg_base": 108.2, "drtg_base": 101.0, "pace_base": 74.2,
                "color": "#e05338", "accent": "#000000",
                "clutch": {"win_pct": 0.556, "pts": 7.0, "efg_pct": 0.505, "ft_pct": 0.770, "tov_rate": 0.118},
                "shot_clock": {"early_0_6s": {"freq": 0.19, "efg": 0.560}, "middle_7_18s": {"freq": 0.64, "efg": 0.505}, "late_19_24s": {"freq": 0.17, "efg": 0.390}},
                "splits": {"catch_shoot_3p": 0.365, "pullup_3p": 0.320, "open_fg": 0.530, "contested_fg": 0.405, "rim_fg": 0.610, "short_mid_fg": 0.395, "long_mid_fg": 0.365, "corner3_fg": 0.380, "above3_fg": 0.340},
                "playmaking": {"ast_tov_ratio": 1.50, "potential_ast": 28.5, "secondary_ast": 5.2},
                "defense": {"rim_def_fg": 0.540, "stl_pct": 7.6, "blk_pct": 3.8, "pf_per_40": 19.0, "fd_per_40": 18.5},
                "roster": [
                    {"name": "Adler", "num": "9", "pos": "Armador", "pts": 16.2, "reb": 4.1, "ast": 6.5, "fg3_pct": 0.370, "fg2_pct": 0.495, "ft_pct": 0.825, "mp": 29.5},
                    {"name": "Lucas Faggiano", "num": "13", "pos": "Pivô", "pts": 13.5, "reb": 8.8, "ast": 1.2, "fg3_pct": 0.000, "fg2_pct": 0.615, "ft_pct": 0.680, "mp": 27.0},
                ]
            },
            {
                "name": "Basquete Blumenau",
                "short_name": "BLU",
                "city": "Blumenau, SC",
                "coach": "André Germano",
                "ortg_base": 108.9, "drtg_base": 99.8, "pace_base": 75.5,
                "color": "#16a34a", "accent": "#ffffff",
                "clutch": {"win_pct": 0.600, "pts": 7.6, "efg_pct": 0.518, "ft_pct": 0.795, "tov_rate": 0.112},
                "shot_clock": {"early_0_6s": {"freq": 0.21, "efg": 0.580}, "middle_7_18s": {"freq": 0.62, "efg": 0.520}, "late_19_24s": {"freq": 0.17, "efg": 0.405}},
                "splits": {"catch_shoot_3p": 0.380, "pullup_3p": 0.335, "open_fg": 0.545, "contested_fg": 0.418, "rim_fg": 0.625, "short_mid_fg": 0.410, "long_mid_fg": 0.380, "corner3_fg": 0.395, "above3_fg": 0.350},
                "playmaking": {"ast_tov_ratio": 1.58, "potential_ast": 30.2, "secondary_ast": 5.9},
                "defense": {"rim_def_fg": 0.525, "stl_pct": 8.1, "blk_pct": 4.2, "pf_per_40": 18.2, "fd_per_40": 19.5},
                "roster": [
                    {"name": "Lucas Gabriel", "num": "8", "pos": "Ala", "pts": 16.4, "reb": 5.2, "ast": 3.2, "fg3_pct": 0.385, "fg2_pct": 0.515, "ft_pct": 0.810, "mp": 29.0},
                    {"name": "Vinicius Gobor", "num": "5", "pos": "Armador", "pts": 13.8, "reb": 3.5, "ast": 6.9, "fg3_pct": 0.360, "fg2_pct": 0.480, "ft_pct": 0.830, "mp": 28.5},
                ]
            },
            {
                "name": "Praia Clube / Uberlândia",
                "short_name": "PRA",
                "city": "Uberlândia, MG",
                "coach": "Guto Trompczynski",
                "ortg_base": 110.2, "drtg_base": 98.4, "pace_base": 76.8,
                "color": "#ca8a04", "accent": "#000000",
                "clutch": {"win_pct": 0.667, "pts": 8.0, "efg_pct": 0.528, "ft_pct": 0.805, "tov_rate": 0.104},
                "shot_clock": {"early_0_6s": {"freq": 0.23, "efg": 0.595}, "middle_7_18s": {"freq": 0.61, "efg": 0.525}, "late_19_24s": {"freq": 0.16, "efg": 0.410}},
                "splits": {"catch_shoot_3p": 0.388, "pullup_3p": 0.340, "open_fg": 0.555, "contested_fg": 0.425, "rim_fg": 0.630, "short_mid_fg": 0.415, "long_mid_fg": 0.380, "corner3_fg": 0.400, "above3_fg": 0.355},
                "playmaking": {"ast_tov_ratio": 1.68, "potential_ast": 31.5, "secondary_ast": 6.5},
                "defense": {"rim_def_fg": 0.518, "stl_pct": 8.6, "blk_pct": 4.4, "pf_per_40": 18.0, "fd_per_40": 20.2},
                "roster": [
                    {"name": "Rafa Moreira", "num": "11", "pos": "Ala-Pivô", "pts": 17.2, "reb": 8.0, "ast": 2.8, "fg3_pct": 0.370, "fg2_pct": 0.550, "ft_pct": 0.825, "mp": 30.0},
                    {"name": "Wellington", "num": "3", "pos": "Armador", "pts": 14.0, "reb": 3.6, "ast": 7.0, "fg3_pct": 0.365, "fg2_pct": 0.490, "ft_pct": 0.820, "mp": 28.0},
                ]
            }
        ]
    },

    # =========================================================================
    # ---------------- 7. TEMPORADA ANTERIOR: 2025–2026 -----------------------
    # =========================================================================
    {
        "id": "nbb-2025",
        "base_id": "nbb",
        "season": "2025–2026",
        "season_id": "2025-2026",
        "name": "NBB Caixa 2025–2026 (Transição de Elencos)",
        "category": "Elite Profissional Masculina",
        "organizer": "LNB / CBB",
        "teams": [
            {
                "name": "Sesi Franca (2025–26)",
                "base_name": "Sesi Franca",
                "short_name": "FRA-25",
                "city": "Franca, SP",
                "coach": "Helinho Garcia",
                "season": "2025–2026",
                "season_id": "2025-2026",
                "ortg_base": 114.2, "drtg_base": 100.8, "pace_base": 74.8,
                "color": "#1a4731", "accent": "#d4af37",
                "clutch": {"win_pct": 0.714, "pts": 8.1, "efg_pct": 0.535, "ft_pct": 0.820, "tov_rate": 0.105},
                "shot_clock": {"early_0_6s": {"freq": 0.22, "efg": 0.585}, "middle_7_18s": {"freq": 0.63, "efg": 0.540}, "late_19_24s": {"freq": 0.15, "efg": 0.430}},
                "splits": {"catch_shoot_3p": 0.405, "pullup_3p": 0.360, "open_fg": 0.565, "contested_fg": 0.440, "rim_fg": 0.640, "short_mid_fg": 0.420, "long_mid_fg": 0.395, "corner3_fg": 0.415, "above3_fg": 0.370},
                "playmaking": {"ast_tov_ratio": 1.82, "potential_ast": 33.5, "secondary_ast": 7.4},
                "defense": {"rim_def_fg": 0.525, "stl_pct": 8.0, "blk_pct": 4.5, "pf_per_40": 17.5, "fd_per_40": 19.2},
                "roster": [
                    {"name": "Lucas Dias", "num": "9", "pos": "Ala-Pivô", "pts": 18.9, "reb": 7.5, "ast": 3.4, "fg3_pct": 0.402, "fg2_pct": 0.552, "ft_pct": 0.850, "mp": 31.0},
                    {"name": "Georginho de Paula", "num": "32", "pos": "Armador", "pts": 17.2, "reb": 7.8, "ast": 7.1, "fg3_pct": 0.365, "fg2_pct": 0.528, "ft_pct": 0.770, "mp": 32.5},
                    {"name": "David Jackson", "num": "7", "pos": "Ala-Armador", "pts": 12.8, "reb": 3.2, "ast": 2.9, "fg3_pct": 0.420, "fg2_pct": 0.525, "ft_pct": 0.900, "mp": 23.5},
                    {"name": "Nathan Mariano", "num": "11", "pos": "Ala-Pivô", "pts": 10.8, "reb": 6.4, "ast": 1.3, "fg3_pct": 0.330, "fg2_pct": 0.590, "ft_pct": 0.740, "mp": 21.0},
                    {"name": "Didi Louzada", "num": "0", "pos": "Ala", "pts": 12.5, "reb": 4.2, "ast": 2.1, "fg3_pct": 0.380, "fg2_pct": 0.510, "ft_pct": 0.790, "mp": 24.0},
                    {"name": "Santiago Scala", "num": "6", "pos": "Armador", "pts": 8.4, "reb": 2.0, "ast": 3.8, "fg3_pct": 0.385, "fg2_pct": 0.450, "ft_pct": 0.870, "mp": 18.0},
                    {"name": "Paulo Zu", "num": "33", "pos": "Ala-Armador", "pts": 7.6, "reb": 2.8, "ast": 1.6, "fg3_pct": 0.350, "fg2_pct": 0.480, "ft_pct": 0.750, "mp": 16.0},
                ]
            },
            {
                "name": "Flamengo (2025–26)",
                "base_name": "Flamengo",
                "short_name": "FLA-25",
                "city": "Rio de Janeiro, RJ",
                "coach": "Gustavo De Conti",
                "season": "2025–2026",
                "season_id": "2025-2026",
                "ortg_base": 114.8, "drtg_base": 98.1, "pace_base": 77.0,
                "color": "#c5221f", "accent": "#000000",
                "clutch": {"win_pct": 0.750, "pts": 8.6, "efg_pct": 0.550, "ft_pct": 0.835, "tov_rate": 0.092},
                "shot_clock": {"early_0_6s": {"freq": 0.24, "efg": 0.605}, "middle_7_18s": {"freq": 0.60, "efg": 0.540}, "late_19_24s": {"freq": 0.16, "efg": 0.425}},
                "splits": {"catch_shoot_3p": 0.400, "pullup_3p": 0.350, "open_fg": 0.565, "contested_fg": 0.440, "rim_fg": 0.650, "short_mid_fg": 0.430, "long_mid_fg": 0.395, "corner3_fg": 0.415, "above3_fg": 0.370},
                "playmaking": {"ast_tov_ratio": 1.85, "potential_ast": 33.5, "secondary_ast": 7.2},
                "defense": {"rim_def_fg": 0.515, "stl_pct": 8.8, "blk_pct": 4.5, "pf_per_40": 17.2, "fd_per_40": 20.0},
                "roster": [
                    {"name": "Gui Deodato", "num": "1", "pos": "Ala", "pts": 16.0, "reb": 4.6, "ast": 3.0, "fg3_pct": 0.410, "fg2_pct": 0.550, "ft_pct": 0.830, "mp": 29.5},
                    {"name": "Alexey Borges", "num": "4", "pos": "Armador", "pts": 13.8, "reb": 3.4, "ast": 6.2, "fg3_pct": 0.375, "fg2_pct": 0.505, "ft_pct": 0.810, "mp": 26.5},
                    {"name": "Shaq Johnson", "num": "11", "pos": "Ala-Armador", "pts": 14.5, "reb": 4.4, "ast": 3.2, "fg3_pct": 0.360, "fg2_pct": 0.530, "ft_pct": 0.820, "mp": 27.0},
                    {"name": "Franco Baralle", "num": "3", "pos": "Armador", "pts": 13.5, "reb": 3.6, "ast": 6.1, "fg3_pct": 0.375, "fg2_pct": 0.500, "ft_pct": 0.830, "mp": 26.0},
                    {"name": "Taya Gallizzi", "num": "83", "pos": "Pivô", "pts": 10.8, "reb": 7.5, "ast": 1.1, "fg3_pct": 0.000, "fg2_pct": 0.640, "ft_pct": 0.690, "mp": 23.0},
                ]
            },
            {
                "name": "Minas Tênis Clube (2025–26)",
                "base_name": "Minas Tênis Clube",
                "short_name": "MTC-25",
                "city": "Belo Horizonte, MG",
                "coach": "Léo Costa",
                "season": "2025–2026",
                "season_id": "2025-2026",
                "ortg_base": 112.8, "drtg_base": 100.5, "pace_base": 74.8,
                "color": "#002d62", "accent": "#ffffff",
                "clutch": {"win_pct": 0.680, "pts": 7.6, "efg_pct": 0.525, "ft_pct": 0.805, "tov_rate": 0.108},
                "shot_clock": {"early_0_6s": {"freq": 0.20, "efg": 0.575}, "middle_7_18s": {"freq": 0.63, "efg": 0.525}, "late_19_24s": {"freq": 0.17, "efg": 0.410}},
                "splits": {"catch_shoot_3p": 0.385, "pullup_3p": 0.330, "open_fg": 0.545, "contested_fg": 0.425, "rim_fg": 0.630, "short_mid_fg": 0.410, "long_mid_fg": 0.380, "corner3_fg": 0.400, "above3_fg": 0.355},
                "playmaking": {"ast_tov_ratio": 1.68, "potential_ast": 31.0, "secondary_ast": 6.2},
                "defense": {"rim_def_fg": 0.530, "stl_pct": 8.0, "blk_pct": 4.3, "pf_per_40": 18.2, "fd_per_40": 19.2},
                "roster": [
                    {"name": "Chuzito González", "num": "8", "pos": "Ala-Armador", "pts": 16.2, "reb": 3.2, "ast": 2.9, "fg3_pct": 0.425, "fg2_pct": 0.510, "ft_pct": 0.880, "mp": 27.0},
                    {"name": "Danilo Fuzaro", "num": "24", "pos": "Ala", "pts": 14.6, "reb": 4.5, "ast": 2.5, "fg3_pct": 0.375, "fg2_pct": 0.525, "ft_pct": 0.785, "mp": 27.5},
                    {"name": "Paranhos", "num": "13", "pos": "Pivô", "pts": 12.2, "reb": 8.8, "ast": 1.4, "fg3_pct": 0.000, "fg2_pct": 0.620, "ft_pct": 0.695, "mp": 25.0},
                ]
            }
        ]
    },
    {
        "id": "cbi-sub19-2025",
        "base_id": "cbi-sub19",
        "season": "2025–2026",
        "season_id": "2025-2026",
        "name": "CBI Sub-19 2025 (Safra 2006/07)",
        "category": "Campeonato Brasileiro Interclubes de Base (CBB / CBC)",
        "organizer": "CBB & CBC",
        "teams": [
            {
                "name": "Paulistano Sub-19 (2025)",
                "base_name": "Paulistano Sub-19",
                "short_name": "CAP19-25",
                "city": "São Paulo, SP",
                "coach": "Beto",
                "season": "2025–2026",
                "season_id": "2025-2026",
                "ortg_base": 111.8, "drtg_base": 95.0, "pace_base": 78.0,
                "color": "#c8102e", "accent": "#ffffff",
                "clutch": {"win_pct": 0.800, "pts": 8.4, "efg_pct": 0.540, "ft_pct": 0.785, "tov_rate": 0.118},
                "shot_clock": {"early_0_6s": {"freq": 0.25, "efg": 0.605}, "middle_7_18s": {"freq": 0.59, "efg": 0.520}, "late_19_24s": {"freq": 0.16, "efg": 0.385}},
                "splits": {"catch_shoot_3p": 0.375, "pullup_3p": 0.315, "open_fg": 0.550, "contested_fg": 0.415, "rim_fg": 0.625, "short_mid_fg": 0.405, "long_mid_fg": 0.365, "corner3_fg": 0.385, "above3_fg": 0.340},
                "playmaking": {"ast_tov_ratio": 1.58, "potential_ast": 32.0, "secondary_ast": 6.8},
                "defense": {"rim_def_fg": 0.495, "stl_pct": 9.5, "blk_pct": 5.0, "pf_per_40": 19.2, "fd_per_40": 20.5},
                "roster": [
                    {"name": "Gabriel Landeira", "num": "11", "pos": "Ala-Armador", "pts": 17.0, "reb": 5.4, "ast": 3.8, "fg3_pct": 0.400, "fg2_pct": 0.540, "ft_pct": 0.840, "mp": 30.0},
                    {"name": "Breno Silva", "num": "15", "pos": "Pivô", "pts": 14.2, "reb": 10.5, "ast": 1.6, "fg3_pct": 0.000, "fg2_pct": 0.645, "ft_pct": 0.700, "mp": 28.0},
                ]
            }
        ]
    },

    # =========================================================================
    # ---------------- 8. TEMPORADA HISTÓRICA: 2024–2025 -----------------------
    # =========================================================================
    {
        "id": "nbb-2024",
        "base_id": "nbb",
        "season": "2024–2025",
        "season_id": "2024-2025",
        "name": "NBB Caixa 2024–2025 (Tricampeonato Franca)",
        "category": "Elite Profissional Masculina",
        "organizer": "LNB / CBB",
        "teams": [
            {
                "name": "Sesi Franca (2024–25)",
                "base_name": "Sesi Franca",
                "short_name": "FRA-24",
                "city": "Franca, SP",
                "coach": "Helinho Garcia",
                "season": "2024–2025",
                "season_id": "2024-2025",
                "ortg_base": 117.8, "drtg_base": 97.5, "pace_base": 73.2,
                "color": "#1a4731", "accent": "#d4af37",
                "clutch": {"win_pct": 0.842, "pts": 10.2, "efg_pct": 0.585, "ft_pct": 0.880, "tov_rate": 0.078},
                "shot_clock": {"early_0_6s": {"freq": 0.16, "efg": 0.610}, "middle_7_18s": {"freq": 0.69, "efg": 0.565}, "late_19_24s": {"freq": 0.15, "efg": 0.460}},
                "splits": {"catch_shoot_3p": 0.420, "pullup_3p": 0.380, "open_fg": 0.590, "contested_fg": 0.465, "rim_fg": 0.670, "short_mid_fg": 0.465, "long_mid_fg": 0.435, "corner3_fg": 0.440, "above3_fg": 0.390},
                "playmaking": {"ast_tov_ratio": 2.05, "potential_ast": 36.5, "secondary_ast": 8.8},
                "defense": {"rim_def_fg": 0.485, "stl_pct": 7.5, "blk_pct": 5.4, "pf_per_40": 16.2, "fd_per_40": 21.5},
                "roster": [
                    {"name": "Lucas Dias", "num": "9", "pos": "Ala-Pivô", "pts": 19.8, "reb": 7.9, "ast": 3.1, "fg3_pct": 0.415, "fg2_pct": 0.568, "ft_pct": 0.872, "mp": 32.5},
                    {"name": "Georginho de Paula", "num": "32", "pos": "Armador", "pts": 15.8, "reb": 8.5, "ast": 7.8, "fg3_pct": 0.352, "fg2_pct": 0.540, "ft_pct": 0.795, "mp": 33.0},
                    {"name": "Márcio Santos", "num": "3", "pos": "Pivô", "pts": 13.5, "reb": 7.8, "ast": 1.4, "fg3_pct": 0.290, "fg2_pct": 0.655, "ft_pct": 0.730, "mp": 24.5},
                    {"name": "David Jackson", "num": "7", "pos": "Ala-Armador", "pts": 15.2, "reb": 3.8, "ast": 3.6, "fg3_pct": 0.440, "fg2_pct": 0.550, "ft_pct": 0.925, "mp": 29.0},
                    {"name": "Lucas Mariano", "num": "28", "pos": "Pivô", "pts": 12.4, "reb": 5.2, "ast": 1.0, "fg3_pct": 0.385, "fg2_pct": 0.530, "ft_pct": 0.820, "mp": 21.0},
                    {"name": "Santiago Scala", "num": "6", "pos": "Armador", "pts": 9.5, "reb": 2.3, "ast": 4.8, "fg3_pct": 0.405, "fg2_pct": 0.480, "ft_pct": 0.890, "mp": 22.0},
                    {"name": "Jhonatan Luz", "num": "14", "pos": "Ala", "pts": 7.2, "reb": 3.5, "ast": 1.8, "fg3_pct": 0.370, "fg2_pct": 0.500, "ft_pct": 0.780, "mp": 18.0},
                ]
            },
            {
                "name": "Flamengo (2024–25)",
                "base_name": "Flamengo",
                "short_name": "FLA-24",
                "city": "Rio de Janeiro, RJ",
                "coach": "Gustavo De Conti",
                "season": "2024–2025",
                "season_id": "2024-2025",
                "ortg_base": 113.5, "drtg_base": 99.2, "pace_base": 76.2,
                "color": "#c5221f", "accent": "#000000",
                "clutch": {"win_pct": 0.714, "pts": 8.2, "efg_pct": 0.535, "ft_pct": 0.810, "tov_rate": 0.102},
                "shot_clock": {"early_0_6s": {"freq": 0.21, "efg": 0.585}, "middle_7_18s": {"freq": 0.62, "efg": 0.530}, "late_19_24s": {"freq": 0.17, "efg": 0.415}},
                "splits": {"catch_shoot_3p": 0.390, "pullup_3p": 0.335, "open_fg": 0.550, "contested_fg": 0.430, "rim_fg": 0.635, "short_mid_fg": 0.415, "long_mid_fg": 0.385, "corner3_fg": 0.405, "above3_fg": 0.360},
                "playmaking": {"ast_tov_ratio": 1.70, "potential_ast": 32.0, "secondary_ast": 6.5},
                "defense": {"rim_def_fg": 0.525, "stl_pct": 8.4, "blk_pct": 4.1, "pf_per_40": 17.8, "fd_per_40": 19.5},
                "roster": [
                    {"name": "Gabriel Jaú", "num": "25", "pos": "Ala-Pivô", "pts": 14.8, "reb": 7.2, "ast": 1.8, "fg3_pct": 0.360, "fg2_pct": 0.565, "ft_pct": 0.780, "mp": 28.5},
                    {"name": "Gui Deodato", "num": "1", "pos": "Ala", "pts": 15.2, "reb": 4.2, "ast": 2.6, "fg3_pct": 0.400, "fg2_pct": 0.540, "ft_pct": 0.820, "mp": 29.0},
                    {"name": "Didi Louzada", "num": "0", "pos": "Ala", "pts": 13.6, "reb": 4.5, "ast": 2.4, "fg3_pct": 0.370, "fg2_pct": 0.515, "ft_pct": 0.765, "mp": 26.5},
                    {"name": "Franco Baralle", "num": "3", "pos": "Armador", "pts": 13.2, "reb": 3.4, "ast": 6.2, "fg3_pct": 0.370, "fg2_pct": 0.490, "ft_pct": 0.835, "mp": 27.0},
                    {"name": "Scott Machado", "num": "1", "pos": "Armador", "pts": 10.5, "reb": 2.8, "ast": 6.8, "fg3_pct": 0.355, "fg2_pct": 0.470, "ft_pct": 0.850, "mp": 23.0},
                ]
            }
        ]
    }
]

HALL_OF_FAME = [
    {"nome": "Oscar Schmidt", "nome_completo": "Oscar Daniel Bezerra Schmidt", "posicao": "Ala", "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Oscar_Schmidt_2011.jpg/440px-Oscar_Schmidt_2011.jpg", "detalhes": "Maior pontuador da história do basquetebol mundial (49.737 pontos). O 'Mão Santa', medalhista de ouro nos Jogos Pan-Americanos de 1987 em Indianápolis contra os EUA."},
    {"nome": "Hortência Marcari", "nome_completo": "Hortência de Fátima Marcari", "posicao": "Ala-Armadora", "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Hortencia_Marcari.jpg/440px-Hortencia_Marcari.jpg", "detalhes": "Campeã Mundial em 1994, medalhista de prata nos Jogos Olímpicos de Atlanta 1996. Integrante do Naismith Memorial Basketball Hall of Fame e FIBA Hall of Fame."},
    {"nome": "Magic Paula", "nome_completo": "Maria Paula Gonçalves da Silva", "posicao": "Armadora", "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Magic_Paula.jpg/440px-Magic_Paula.jpg", "detalhes": "Campeã Mundial em 1994 e ouro Pan-Americano em 1987. Célebre visão de quadra e liderança técnica na Seleção Brasileira feminina."},
    {"nome": "Janeth Arcain", "nome_completo": "Janeth dos Santos Arcain", "posicao": "Ala-Armadora", "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Janeth_Arcain.jpg/440px-Janeth_Arcain.jpg", "detalhes": "Tetracampeã da WNBA pelo Houston Comets, campeã mundial em 1994, prata em Atlanta 1996 e bronze em Sydney 2000."},
    {"nome": "Wlamir Marques", "nome_completo": "Wlamir Marques", "posicao": "Ala", "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Wlamir_Marques.jpg/440px-Wlamir_Marques.jpg", "detalhes": "Bicampeão Mundial de Basquete com o Brasil (1959 e 1963) e duas vezes medalhista olímpico de bronze (Roma 1960 e Tóquio 1964)."},
    {"nome": "Tiago Splitter", "nome_completo": "Tiago Splitter", "posicao": "Pivô", "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Tiago_Splitter_2013.jpg/440px-Tiago_Splitter_2013.jpg", "detalhes": "Primeiro brasileiro campeão da NBA (San Antonio Spurs, 2014) e pilar dos títulos das Américas pela Seleção Brasileira."},
    {"nome": "Leandro Barbosa (Leandrinho)", "nome_completo": "Leandro Mateus Barbosa", "posicao": "Armador", "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Leandro_Barbosa_2016.jpg/440px-Leandro_Barbosa_2016.jpg", "detalhes": "The Brazilian Blur. Campeão da NBA em 2015 pelo Golden State Warriors e eleito NBA Sixth Man of the Year em 2007."},
]

SEASON_COMPARISONS: Dict[str, Any] = {
    "Sesi Franca": {
        "team_name": "Sesi Franca",
        "city": "Franca, SP",
        "badge_color": "#1a4731",
        "accent_color": "#d4af37",
        "narrative": "A evolução tática do Sesi Franca entre 2024 e 2027 reflete com exatidão o basquete moderno de elite. Em 2024–25, a equipe comandada por Helinho Garcia operava em meia-quadra cadenciada (Pace 73.2) com pivôs físicos (Márcio Santos e Lucas Mariano), gerando enorme volume de faltas cavadas (FTR 0.315) e o maior Net Rating recente do basquete nacional (+20.3). Em 2025–26, após a transferência de Márcio Santos para a Liga ACB (Breogán/Espanha), Franca acelerou o jogo para 74.8 posses, aumentando os arremessos de 3 em transição precoce para compensar a menor taxa de lances livres (FTR caiu para 0.272). Em 2026–27, com o jovem Nathan Mariano firmado no garrafão e rotação profunda da LDB, o equilíbrio foi restabelecido.",
        "seasons": [
            {
                "season": "2024–2025",
                "season_id": "2024-2025",
                "label": "2024–2025 (Tricampeão)",
                "trophy": "🏆 Campeão NBB & Copa Super 8",
                "record": "31-5 (86.1%)",
                "coach": "Helinho Garcia",
                "pace": 73.2,
                "ortg": 117.8,
                "drtg": 97.5,
                "net_rating": 20.3,
                "efg_pct": 0.564,
                "tov_pct": 0.121,
                "orb_pct": 0.295,
                "ftr": 0.315,
                "rim_freq": 0.38,
                "mid_freq": 0.25,
                "three_freq": 0.37,
                "key_departures": ["Lucas Mariano (fim da temporada)"],
                "key_arrivals": ["Georginho de Paula (retorno da Alemanha/Ulm)"],
                "pivotal_players": "Lucas Dias (MVP, 19.8 pts, 7.9 reb), Georginho (15.8 pts, 7.8 ast), Márcio Santos (13.5 pts, 7.8 reb, pivô dominante), David Jackson (15.2 pts, 92.5% FT).",
                "tactical_summary": "Cadência e imposição física no garrafão. O mais alto Net Rating da história recente do NBB (+20.3) e maior taxa de lances livres cavados (FTR 0.315)."
            },
            {
                "season": "2025–2026",
                "season_id": "2025-2026",
                "label": "2025–2026 (Transição)",
                "trophy": "Semifinalista NBB",
                "record": "27-9 (75.0%)",
                "coach": "Helinho Garcia",
                "pace": 74.8,
                "ortg": 114.2,
                "drtg": 100.8,
                "net_rating": 13.4,
                "efg_pct": 0.546,
                "tov_pct": 0.134,
                "orb_pct": 0.262,
                "ftr": 0.272,
                "rim_freq": 0.33,
                "mid_freq": 0.20,
                "three_freq": 0.47,
                "key_departures": ["Márcio Santos (Espanha / Liga ACB - Breogán)"],
                "key_arrivals": ["Nathan Mariano (promoção da base LDB)", "Paulo Zu (LDB)"],
                "pivotal_players": "Lucas Dias (18.9 pts, 7.5 reb), Georginho (17.2 pts, 7.1 ast), Nathan Mariano (10.8 pts, 6.4 reb, ascensão da base), David Jackson (minutos dosados: 23 min).",
                "tactical_summary": "Transição precoce e perímetro. Sem a presença física de Márcio Santos, a taxa de faltas cavadas (FTR) caiu 4.3 pontos percentuais e o time compensou com chutes de 3 em transição."
            },
            {
                "season": "2026–2027",
                "season_id": "2026-2027",
                "label": "2026–2027 (Atual)",
                "trophy": "⚡ Temporada Vigente (Líder)",
                "record": "20-4 (83.3%)",
                "coach": "Helinho Garcia",
                "pace": 75.4,
                "ortg": 115.8,
                "drtg": 99.8,
                "net_rating": 16.0,
                "efg_pct": 0.558,
                "tov_pct": 0.125,
                "orb_pct": 0.282,
                "ftr": 0.288,
                "rim_freq": 0.37,
                "mid_freq": 0.17,
                "three_freq": 0.46,
                "key_departures": [],
                "key_arrivals": ["Nathan Mariano consolidado como titular", "Didi Louzada"],
                "pivotal_players": "Lucas Dias (19.5 pts, 7.8 reb), Georginho (16.4 pts, 8.2 reb, 7.4 ast), David Jackson (14.1 pts, 91.5% FT), Nathan Mariano (11.2 pts, 6.5 reb).",
                "tactical_summary": "Consolidação moderna. Rotação profunda da LDB aliada à maturidade de Lucas Dias e Georginho, restabelecendo a proteção de aro e o espaçamento de elite."
            }
        ]
    },
    "Flamengo": {
        "team_name": "Flamengo",
        "city": "Rio de Janeiro, RJ",
        "badge_color": "#c5221f",
        "accent_color": "#000000",
        "narrative": "O Flamengo passou por renovação tática contínua: de um time focado no rebote ofensivo com Gabriel Jaú em 2024–25 para um backcourt ultra-veloz com Alexey Borges e Shaq Johnson em 2025–26 e 2026–27.",
        "seasons": [
            {
                "season": "2024–2025",
                "season_id": "2024-2025",
                "label": "2024–2025 (Vice-Campeão)",
                "trophy": "Vice-Campeão NBB & Final BCLA",
                "record": "29-7 (80.5%)",
                "coach": "Gustavo De Conti",
                "pace": 76.2, "ortg": 113.5, "drtg": 99.2, "net_rating": 14.3,
                "efg_pct": 0.540, "tov_pct": 0.118, "orb_pct": 0.310, "ftr": 0.295,
                "rim_freq": 0.36, "mid_freq": 0.22, "three_freq": 0.42,
                "key_departures": ["Gabriel Jaú (Europa)", "Scott Machado"],
                "key_arrivals": [],
                "pivotal_players": "Gabriel Jaú (14.8 pts, 7.2 reb), Gui Deodato (15.2 pts), Didi Louzada (13.6 pts), Franco Baralle (13.2 pts).",
                "tactical_summary": "Agressividade no rebote ofensivo com Gabriel Jaú e perímetro rápido sob o comando de De Conti."
            },
            {
                "season": "2025–2026",
                "season_id": "2025-2026",
                "label": "2025–2026",
                "trophy": "Campeão Copa Super 8",
                "record": "28-8 (77.8%)",
                "coach": "Gustavo De Conti",
                "pace": 77.0, "ortg": 114.8, "drtg": 98.1, "net_rating": 16.7,
                "efg_pct": 0.552, "tov_pct": 0.108, "orb_pct": 0.285, "ftr": 0.282,
                "rim_freq": 0.38, "mid_freq": 0.18, "three_freq": 0.44,
                "key_departures": ["Gabriel Jaú"],
                "key_arrivals": ["Alexey Borges (Armador)", "Shaq Johnson", "Taya Gallizzi"],
                "pivotal_players": "Alexey Borges (13.8 pts, 6.2 ast), Gui Deodato (16.0 pts), Shaq Johnson (14.5 pts), Taya Gallizzi (10.8 pts, 7.5 reb).",
                "tactical_summary": "Aceleração no backcourt com Alexey Borges e Franco Baralle dividindo o playmaking, além de presença física de Gallizzi."
            },
            {
                "season": "2026–2027",
                "season_id": "2026-2027",
                "label": "2026–2027 (Atual)",
                "trophy": "⚡ Temporada Vigente",
                "record": "21-5 (80.8%)",
                "coach": "Gustavo De Conti",
                "pace": 76.8, "ortg": 114.2, "drtg": 98.4, "net_rating": 15.8,
                "efg_pct": 0.548, "tov_pct": 0.112, "orb_pct": 0.292, "ftr": 0.280,
                "rim_freq": 0.39, "mid_freq": 0.16, "three_freq": 0.45,
                "key_departures": [],
                "key_arrivals": ["Kayo Gonçalves afirmado"],
                "pivotal_players": "Gui Deodato (15.8 pts), Franco Baralle (14.2 pts, 6.5 ast), Alexey Borges (12.4 pts), Shaq Johnson (13.9 pts).",
                "tactical_summary": "Pressão defensiva em toda a quadra, alta rotação de alas e transição de contra-ataque em menos de 6 segundos."
            }
        ]
    }
}

def generate_spatial_shots(team_name: str, season: str = "2026–2027", count: int = 180) -> List[Dict[str, Any]]:
    """
    Generates realistic spatial coordinates (in meters) for a team on a half court
    following modern shot distribution, adjusted by team and season.
    """
    shots = []
    seed = hashlib.sha256(f"{team_name}_{season}".encode()).digest()
    rng = random.Random(seed)
    
    # Season-specific tendencies: Franca 2024-25 had more rim/paint presence (Márcio Santos);
    # 2025-26 shifted towards perimeter 3-pointers; 2026-27 is modern balanced.
    three_pct_cutoff = 0.44
    paint_pct_cutoff = 0.80
    if "Franca" in team_name:
        if "2024" in season:
            three_pct_cutoff = 0.37  # fewer 3s, more inside
            paint_pct_cutoff = 0.75  # more rim & paint with Márcio Santos
        elif "2025" in season:
            three_pct_cutoff = 0.48  # heavy 3pt volume
            paint_pct_cutoff = 0.81
    
    for i in range(count):
        shot_type_roll = rng.random()
        clock_sec = rng.randint(2, 24)
        if shot_type_roll < three_pct_cutoff:
            # 3-Point Shot
            if rng.random() < 0.28:
                # Corner 3
                x = rng.choice([-6.85, 6.85]) + rng.uniform(-0.25, 0.25)
                y = rng.uniform(0.8, 2.8)
                is_3pt = True
                made = rng.random() < 0.385
            else:
                # Arc 3
                angle = rng.uniform(math.pi * 0.16, math.pi * 0.84)
                radius = rng.uniform(6.85, 8.4)
                x = radius * math.cos(angle)
                y = 1.575 + radius * math.sin(angle)
                is_3pt = True
                made = rng.random() < 0.358
        elif shot_type_roll < paint_pct_cutoff:
            # Rim / Restricted Area (<1.25m from rim center)
            r = rng.uniform(0.2, 1.22)
            angle = rng.uniform(0, 2 * math.pi)
            x = r * math.cos(angle)
            y = 1.575 + r * math.sin(angle)
            is_3pt = False
            made = rng.random() < 0.635
        else:
            # Mid-Range (short and long floaters / pull-ups)
            r = rng.uniform(2.2, 5.7)
            angle = rng.uniform(math.pi * 0.12, math.pi * 0.88)
            x = r * math.cos(angle)
            y = 1.575 + r * math.sin(angle)
            is_3pt = False
            made = rng.random() < 0.410
            
        zone = classify_shot_zone(x, y)
        shots.append({
            "shot_id": f"sh_{team_name[:3]}_{season[:4]}_{i}",
            "team_name": team_name,
            "season": season,
            "x": round(x, 2),
            "y": round(y, 2),
            "zone": zone,
            "clock_sec": clock_sec,
            "made": made,
            "pts": 3 if is_3pt and made else (2 if made else 0)
        })
    return shots

def get_complete_fallback_dataset() -> Dict[str, Any]:
    """
    Constructs the complete precomputed dataset for all competitions and seasons.
    """
    competitions_output = []
    all_teams_flat = []
    all_shots_by_team = {}
    hexbins_by_team = {}
    
    for comp in COMPETITIONS_DATA:
        comp_season = comp.get("season", "2026–2027")
        comp_season_id = comp.get("season_id", "2026-2027")
        comp_teams = []
        for t in comp["teams"]:
            team_season = t.get("season", comp_season)
            team_season_id = t.get("season_id", comp_season_id)
            shots = generate_spatial_shots(t["name"], season=team_season, count=180)
            
            # Store shots and hexbins with composite key and bare team name for current season
            team_key_season = f"{t['name']}__{team_season}"
            all_shots_by_team[team_key_season] = shots
            hexbins = compute_hexbin_analytics(shots, gridsize=14, min_count=2)
            hexbins_by_team[team_key_season] = hexbins
            
            if team_season == "2026–2027" or t["name"] not in all_shots_by_team:
                all_shots_by_team[t["name"]] = shots
                hexbins_by_team[t["name"]] = hexbins
                
            zone_eff = compute_zone_efficiency(shots)
            
            # Four Factors
            fga = len(shots)
            fgm = sum(1 for s in shots if s["made"])
            fg3m = sum(1 for s in shots if s["pts"] == 3)
            fg3a = sum(1 for s in shots if "3" in s["zone"])
            pts = sum(s["pts"] for s in shots)
            
            fta = round(fga * 0.26)
            ftm = round(fta * 0.78)
            orb = round(fga * 0.11)
            opp_drb = round(fga * 0.28)
            tov = round(fga * 0.16)
            opp_pts = round(pts * (t["drtg_base"] / t["ortg_base"]))
            
            ff = compute_four_factors(
                fgm=fgm, fga=fga, fg3m=fg3m,
                ftm=ftm, fta=fta,
                orb=orb, opp_drb=opp_drb,
                tov=tov, pts=pts + ftm, opp_pts=opp_pts
            )
            
            # Roster
            roster_with_metrics = []
            for p in t["roster"]:
                p_fga = round(p["pts"] * 0.85)
                p_fg3a = round(p_fga * 0.45)
                p_fg3m = round(p_fg3a * p["fg3_pct"])
                p_fg2a = p_fga - p_fg3a
                p_fg2m = round(p_fg2a * p["fg2_pct"])
                p_fgm = p_fg2m + p_fg3m
                p_fta = round(p["pts"] * 0.25)
                p_ftm = round(p_fta * p["ft_pct"])
                
                p_adv = compute_player_advanced_metrics(
                    pts=p["pts"] * 20, fga=p_fga * 20, fgm=p_fgm * 20,
                    fg3a=p_fg3a * 20, fg3m=p_fg3m * 20, fta=p_fta * 20, ftm=p_ftm * 20,
                    orb=p["reb"] * 0.3 * 20, drb=p["reb"] * 0.7 * 20, trb=p["reb"] * 20,
                    ast=p["ast"] * 20, stl=1.3 * 20, blk=0.7 * 20, tov=2.0 * 20,
                    pf=2.2 * 20, fd=3.4 * 20, mp=p["mp"]
                )
                roster_with_metrics.append({
                    **p,
                    "team": t["name"],
                    "season": team_season,
                    "season_id": team_season_id,
                    "competition_id": comp["id"],
                    "competition_name": comp["name"],
                    "fga": p_fga,
                    "fgm": p_fgm,
                    "fg3m": p_fg3m,
                    "fg3a": p_fg3a,
                    "ftm": p_ftm,
                    "fta": p_fta,
                    "advanced": p_adv
                })
                
            team_entry = {
                "name": t["name"],
                "base_name": t.get("base_name", t["name"]),
                "short_name": t["short_name"],
                "city": t["city"],
                "coach": t["coach"],
                "season": team_season,
                "season_id": team_season_id,
                "is_current_season": (team_season == "2026–2027"),
                "color": t["color"],
                "accent": t.get("accent", "#ffffff"),
                "competition_id": comp["id"],
                "base_competition_id": comp.get("base_id", comp["id"]),
                "competition_name": comp["name"],
                "four_factors": ff,
                "clutch": t.get("clutch", {}),
                "shot_clock": t.get("shot_clock", {}),
                "splits": t.get("splits", {}),
                "playmaking": t.get("playmaking", {}),
                "defense": t.get("defense", {}),
                "zone_efficiency": zone_eff,
                "roster": roster_with_metrics,
                "sample_games": 24
            }
            comp_teams.append(team_entry)
            all_teams_flat.append(team_entry)
            
        competitions_output.append({
            "id": comp["id"],
            "base_id": comp.get("base_id", comp["id"]),
            "season": comp_season,
            "season_id": comp_season_id,
            "name": comp["name"],
            "category": comp["category"],
            "organizer": comp["organizer"],
            "teams": comp_teams
        })
        
    return {
        "available_seasons": AVAILABLE_SEASONS,
        "season_comparisons": SEASON_COMPARISONS,
        "competitions": competitions_output,
        "teams": all_teams_flat,
        "hall_of_fame": HALL_OF_FAME,
        "all_shots": all_shots_by_team,
        "hexbins": hexbins_by_team
    }
