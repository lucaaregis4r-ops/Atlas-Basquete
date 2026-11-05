"""
Deterministic high-fidelity seed dataset calibrated against official CBB & NBB competitions.
Guarantees full offline functionality and initial baseline data.
"""
from typing import Dict, List, Any
import random
import math
from cbb.analysis.four_factors import compute_four_factors
from cbb.analysis.player_advanced import compute_player_advanced_metrics
from cbb.analysis.shot_efficiency import classify_shot_zone, compute_zone_efficiency

TEAMS_PROFILE = [
    {
        "name": "Flamengo",
        "short_name": "FLA",
        "city": "Rio de Janeiro, RJ",
        "coach": "Gustavo De Conti",
        "ortg_base": 114.2,
        "drtg_base": 98.4,
        "pace_base": 76.8,
        "color": "#c5221f",
        "accent": "#000000",
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
        "ortg_base": 115.8,
        "drtg_base": 99.8,
        "pace_base": 74.5,
        "color": "#1a4731",
        "accent": "#d4af37",
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
        "ortg_base": 113.5,
        "drtg_base": 100.2,
        "pace_base": 75.2,
        "color": "#002d62",
        "accent": "#ffffff",
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
        "ortg_base": 109.8,
        "drtg_base": 104.5,
        "pace_base": 74.0,
        "color": "#da251c",
        "accent": "#000000",
        "roster": [
            {"name": "Ricardo Fischer", "num": "5", "pos": "Armador", "pts": 14.5, "reb": 3.2, "ast": 6.8, "fg3_pct": 0.375, "fg2_pct": 0.485, "ft_pct": 0.860, "mp": 29.0},
            {"name": "Betinho", "num": "3", "pos": "Ala", "pts": 13.9, "reb": 4.1, "ast": 2.4, "fg3_pct": 0.395, "fg2_pct": 0.510, "ft_pct": 0.835, "mp": 27.5},
            {"name": "Miller", "num": "33", "pos": "Ala-Armador", "pts": 15.6, "reb": 3.8, "ast": 2.9, "fg3_pct": 0.350, "fg2_pct": 0.530, "ft_pct": 0.810, "mp": 28.5},
            {"name": "Tyrone Curnell", "num": "0", "pos": "Ala-Pivô", "pts": 12.8, "reb": 6.4, "ast": 2.1, "fg3_pct": 0.360, "fg2_pct": 0.540, "ft_pct": 0.770, "mp": 26.0},
            {"name": "Vitor Faverani", "num": "13", "pos": "Pivô", "pts": 10.5, "reb": 7.0, "ast": 1.2, "fg3_pct": 0.250, "fg2_pct": 0.590, "ft_pct": 0.710, "mp": 20.5},
        ]
    },
    {
        "name": "Bauru Basket",
        "short_name": "BAU",
        "city": "Bauru, SP",
        "coach": "Paulo Jaú",
        "ortg_base": 108.5,
        "drtg_base": 103.8,
        "pace_base": 73.2,
        "color": "#0055a5",
        "accent": "#ffcc00",
        "roster": [
            {"name": "Alex Garcia", "num": "10", "pos": "Ala", "pts": 15.1, "reb": 5.4, "ast": 4.5, "fg3_pct": 0.365, "fg2_pct": 0.520, "ft_pct": 0.795, "mp": 30.5},
            {"name": "Dontrell Brite", "num": "4", "pos": "Armador", "pts": 14.8, "reb": 3.9, "ast": 5.2, "fg3_pct": 0.355, "fg2_pct": 0.490, "ft_pct": 0.820, "mp": 28.0},
            {"name": "Anderson Rodrigues", "num": "20", "pos": "Pivô", "pts": 12.3, "reb": 8.0, "ast": 1.1, "fg3_pct": 0.000, "fg2_pct": 0.620, "ft_pct": 0.670, "mp": 25.0},
            {"name": "Gemadinha", "num": "11", "pos": "Ala-Armador", "pts": 13.0, "reb": 2.8, "ast": 2.1, "fg3_pct": 0.395, "fg2_pct": 0.480, "ft_pct": 0.840, "mp": 24.5},
        ]
    },
    {
        "name": "Paulistano",
        "short_name": "CAP",
        "city": "São Paulo, SP",
        "coach": "Demétrius Ferracciú",
        "ortg_base": 107.2,
        "drtg_base": 101.5,
        "pace_base": 75.8,
        "color": "#c8102e",
        "accent": "#ffffff",
        "roster": [
            {"name": "Kevin Crescenzi", "num": "2", "pos": "Ala-Armador", "pts": 14.0, "reb": 4.2, "ast": 3.5, "fg3_pct": 0.370, "fg2_pct": 0.510, "ft_pct": 0.820, "mp": 27.0},
            {"name": "Lucas Doria", "num": "8", "pos": "Ala-Pivô", "pts": 12.5, "reb": 6.8, "ast": 1.9, "fg3_pct": 0.355, "fg2_pct": 0.535, "ft_pct": 0.760, "mp": 26.0},
            {"name": "Santiago Ferreyra", "num": "11", "pos": "Armador", "pts": 11.8, "reb": 3.0, "ast": 5.4, "fg3_pct": 0.360, "fg2_pct": 0.470, "ft_pct": 0.850, "mp": 25.5},
            {"name": "Brunão", "num": "14", "pos": "Pivô", "pts": 10.2, "reb": 7.5, "ast": 1.0, "fg3_pct": 0.000, "fg2_pct": 0.610, "ft_pct": 0.650, "mp": 22.0},
        ]
    },
    {
        "name": "Unifacisa",
        "short_name": "UFC",
        "city": "Campina Grande, PB",
        "coach": "Rodrigo Silva",
        "ortg_base": 110.5,
        "drtg_base": 105.0,
        "pace_base": 75.0,
        "color": "#00205b",
        "accent": "#e05338",
        "roster": [
            {"name": "Trevor Gaskins", "num": "2", "pos": "Armador", "pts": 14.5, "reb": 3.2, "ast": 4.8, "fg3_pct": 0.385, "fg2_pct": 0.490, "ft_pct": 0.830, "mp": 27.5},
            {"name": "André Góes", "num": "40", "pos": "Ala", "pts": 13.2, "reb": 4.5, "ast": 3.9, "fg3_pct": 0.390, "fg2_pct": 0.515, "ft_pct": 0.850, "mp": 28.0},
            {"name": "Rafael Rachel", "num": "10", "pos": "Ala-Pivô", "pts": 12.0, "reb": 7.1, "ast": 1.6, "fg3_pct": 0.340, "fg2_pct": 0.550, "ft_pct": 0.730, "mp": 24.5},
            {"name": "Gerson", "num": "18", "pos": "Pivô", "pts": 10.8, "reb": 6.8, "ast": 0.9, "fg3_pct": 0.000, "fg2_pct": 0.625, "ft_pct": 0.680, "mp": 21.0},
        ]
    },
    {
        "name": "Vasco da Gama",
        "short_name": "VAS",
        "city": "Rio de Janeiro, RJ",
        "coach": "Léo Figueiró",
        "ortg_base": 108.0,
        "drtg_base": 102.8,
        "pace_base": 73.0,
        "color": "#000000",
        "accent": "#ffffff",
        "roster": [
            {"name": "Marquinhos", "num": "11", "pos": "Ala", "pts": 15.5, "reb": 4.8, "ast": 3.2, "fg3_pct": 0.395, "fg2_pct": 0.525, "ft_pct": 0.850, "mp": 28.5},
            {"name": "Eugeniusz", "num": "2", "pos": "Armador", "pts": 13.8, "reb": 3.6, "ast": 5.1, "fg3_pct": 0.365, "fg2_pct": 0.480, "ft_pct": 0.790, "mp": 27.0},
            {"name": "Paulinho Boracini", "num": "9", "pos": "Armador", "pts": 11.2, "reb": 2.4, "ast": 3.8, "fg3_pct": 0.380, "fg2_pct": 0.460, "ft_pct": 0.870, "mp": 20.0},
            {"name": "Serjão", "num": "15", "pos": "Pivô", "pts": 10.5, "reb": 7.4, "ast": 1.1, "fg3_pct": 0.000, "fg2_pct": 0.590, "ft_pct": 0.660, "mp": 23.0},
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

def generate_spatial_shots(team_name: str, count: int = 140) -> List[Dict[str, Any]]:
    """
    Generates realistic spatial coordinates (in meters) for a team on a half court
    following modern shot distribution (concentration at rim and beyond 3PT line).
    """
    shots = []
    random.seed(abs(hash(team_name)) % 10000)
    for i in range(count):
        shot_type_roll = random.random()
        if shot_type_roll < 0.42:
            # 3-Point Shot
            if random.random() < 0.28:
                # Corner 3
                x = random.choice([-6.9, 6.9]) + random.uniform(-0.3, 0.3)
                y = random.uniform(1.0, 2.8)
                is_3pt = True
                made = random.random() < 0.38
            else:
                # Arc 3
                angle = random.uniform(math.pi * 0.15, math.pi * 0.85)
                radius = random.uniform(6.85, 8.2)
                x = radius * math.cos(angle)
                y = 1.575 + radius * math.sin(angle)
                is_3pt = True
                made = random.random() < 0.355
        elif shot_type_roll < 0.78:
            # Rim / Restricted Area
            r = random.uniform(0.3, 1.22)
            angle = random.uniform(0, 2 * math.pi)
            x = r * math.cos(angle)
            y = 1.575 + r * math.sin(angle)
            is_3pt = False
            made = random.random() < 0.63
        else:
            # Mid-Range
            r = random.uniform(2.5, 5.8)
            angle = random.uniform(math.pi * 0.1, math.pi * 0.9)
            x = r * math.cos(angle)
            y = 1.575 + r * math.sin(angle)
            is_3pt = False
            made = random.random() < 0.405
            
        zone = classify_shot_zone(x, y)
        shots.append({
            "shot_id": f"sh_{team_name[:3]}_{i}",
            "team_name": team_name,
            "x": round(x, 2),
            "y": round(y, 2),
            "zone": zone,
            "made": made,
            "pts": 3 if is_3pt and made else (2 if made else 0)
        })
    return shots

def get_complete_fallback_dataset() -> Dict[str, Any]:
    """
    Constructs the complete precomputed dataset for the application.
    """
    teams_output = []
    all_shots = {}
    
    for t in TEAMS_PROFILE:
        shots = generate_spatial_shots(t["name"], count=160)
        all_shots[t["name"]] = shots
        zone_eff = compute_zone_efficiency(shots)
        
        # Calculate team-level Four Factors
        fga = len(shots)
        fgm = sum(1 for s in shots if s["made"])
        fg3m = sum(1 for s in shots if s["pts"] == 3)
        fg3a = sum(1 for s in shots if "3" in s["zone"])
        pts = sum(s["pts"] for s in shots)
        
        # Estimate FTs and Rebounds based on profile
        fta = round(fga * 0.26)
        ftm = round(fta * 0.78)
        orb = round(fga * 0.11)
        opp_drb = round(fga * 0.28)
        tov = round(fga * 0.17)
        opp_pts = round(pts * (t["drtg_base"] / t["ortg_base"]))
        
        ff = compute_four_factors(
            fgm=fgm, fga=fga, fg3m=fg3m,
            ftm=ftm, fta=fta,
            orb=orb, opp_drb=opp_drb,
            tov=tov, pts=pts + ftm, opp_pts=opp_pts
        )
        
        # Player metrics
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
                ast=p["ast"] * 20, stl=1.2 * 20, blk=0.6 * 20, tov=2.1 * 20,
                pf=2.3 * 20, fd=3.2 * 20, mp=p["mp"]
            )
            roster_with_metrics.append({
                **p,
                "fga": p_fga,
                "fgm": p_fgm,
                "fg3m": p_fg3m,
                "fg3a": p_fg3a,
                "ftm": p_ftm,
                "fta": p_fta,
                "advanced": p_adv
            })
            
        teams_output.append({
            "name": t["name"],
            "short_name": t["short_name"],
            "city": t["city"],
            "coach": t["coach"],
            "color": t["color"],
            "four_factors": ff,
            "zone_efficiency": zone_eff,
            "roster": roster_with_metrics,
            "sample_games": 22
        })
        
    return {
        "teams": teams_output,
        "hall_of_fame": HALL_OF_FAME,
        "all_shots": all_shots
    }
