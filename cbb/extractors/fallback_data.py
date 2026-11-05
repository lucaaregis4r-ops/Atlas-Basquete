"""
Comprehensive Multi-Competition Dataset for Brazilian Basketball.
Covers:
- NBB Caixa & Copa Super 8 (Elite Adulta)
- CBI Sub-19 Masculino & Feminino (Campeonato Brasileiro Interclubes)
- CBI Sub-17 Masculino & Feminino (Campeonato Brasileiro Interclubes)
- CBI Super 15 (Sub-15) Masculino & Feminino (Campeonato Brasileiro Interclubes)
- Brasileirão CBB Adulto (Campeonato Brasileiro de Clubes CBB)
- LDB Sub-22 (Liga de Desenvolvimento de Basquete)
- Seleções Brasileiras CBB
"""
from typing import Dict, List, Any
import random
import math
from cbb.analysis.four_factors import compute_four_factors
from cbb.analysis.player_advanced import compute_player_advanced_metrics
from cbb.analysis.shot_efficiency import classify_shot_zone, compute_zone_efficiency
from cbb.court.generator import compute_hexbin_analytics

COMPETITIONS_DATA: List[Dict[str, Any]] = [
    # ---------------- 1. NBB CAIXA & COPA SUPER 8 ----------------
    {
        "id": "nbb",
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

    # ---------------- 2. CBI SUB-19 (CAMPEONATO BRASILEIRO INTERCLUBES) ----------------
    {
        "id": "cbi-sub19",
        "name": "CBI Sub-19 Masculino & Feminino",
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
            }
        ]
    },

    # ---------------- 3. CBI SUB-17 (CAMPEONATO BRASILEIRO INTERCLUBES) ----------------
    {
        "id": "cbi-sub17",
        "name": "CBI Sub-17 Masculino & Feminino",
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
            }
        ]
    },

    # ---------------- 4. BRASILEIRÃO CBB ADULTO ----------------
    {
        "id": "brasileirao-cbb",
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

def generate_spatial_shots(team_name: str, count: int = 180) -> List[Dict[str, Any]]:
    """
    Generates realistic spatial coordinates (in meters) for a team on a half court
    following modern shot distribution (concentration at rim and beyond 3PT line).
    """
    shots = []
    random.seed(abs(hash(team_name)) % 10000)
    for i in range(count):
        shot_type_roll = random.random()
        clock_sec = random.randint(2, 24)
        if shot_type_roll < 0.44:
            # 3-Point Shot
            if random.random() < 0.28:
                # Corner 3
                x = random.choice([-6.85, 6.85]) + random.uniform(-0.25, 0.25)
                y = random.uniform(0.8, 2.8)
                is_3pt = True
                made = random.random() < 0.385
            else:
                # Arc 3
                angle = random.uniform(math.pi * 0.16, math.pi * 0.84)
                radius = random.uniform(6.85, 8.4)
                x = radius * math.cos(angle)
                y = 1.575 + radius * math.sin(angle)
                is_3pt = True
                made = random.random() < 0.358
        elif shot_type_roll < 0.80:
            # Rim / Restricted Area (<1.25m from rim center)
            r = random.uniform(0.2, 1.22)
            angle = random.uniform(0, 2 * math.pi)
            x = r * math.cos(angle)
            y = 1.575 + r * math.sin(angle)
            is_3pt = False
            made = random.random() < 0.635
        else:
            # Mid-Range (short and long floaters / pull-ups)
            r = random.uniform(2.2, 5.7)
            angle = random.uniform(math.pi * 0.12, math.pi * 0.88)
            x = r * math.cos(angle)
            y = 1.575 + r * math.sin(angle)
            is_3pt = False
            made = random.random() < 0.410
            
        zone = classify_shot_zone(x, y)
        shots.append({
            "shot_id": f"sh_{team_name[:3]}_{i}",
            "team_name": team_name,
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
    Constructs the complete precomputed dataset for all competitions.
    """
    competitions_output = []
    all_teams_flat = []
    all_shots_by_team = {}
    hexbins_by_team = {}
    
    for comp in COMPETITIONS_DATA:
        comp_teams = []
        for t in comp["teams"]:
            shots = generate_spatial_shots(t["name"], count=180)
            all_shots_by_team[t["name"]] = shots
            
            # Compute Goldsberry Hexbins and Zone Metrics
            hexbins = compute_hexbin_analytics(shots, gridsize=14, min_count=2)
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
                "short_name": t["short_name"],
                "city": t["city"],
                "coach": t["coach"],
                "color": t["color"],
                "accent": t.get("accent", "#ffffff"),
                "competition_id": comp["id"],
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
            "name": comp["name"],
            "category": comp["category"],
            "organizer": comp["organizer"],
            "teams": comp_teams
        })
        
    return {
        "competitions": competitions_output,
        "teams": all_teams_flat,
        "hall_of_fame": HALL_OF_FAME,
        "all_shots": all_shots_by_team,
        "hexbins": hexbins_by_team
    }
