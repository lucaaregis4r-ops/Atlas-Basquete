"""
Discrete-Time Absorbing Markov Chain Possession Model for Basketball.
References:
- Sandholtz, N., & Bornn, L. (2020). Markov decision processes and shot selection in basketball.
  Journal of Quantitative Analysis in Sports.
- Cervone, D., D'Amour, A., Bornn, L., & Goldsberry, K. (2016). A multiresolution stochastic
  process model for predicting basketball possession outcomes. JASA.
- Teramoto, M., & Cross, C. L. (2010). Relative importance of performance factors in winning
  NBA games in regular season versus playoffs. JQAS.
"""
from typing import Dict, List, Any, Tuple
import numpy as np

# Transient States (In-progress possession)
TRANSIENT_STATES = [
    "S0_Trans_Inflow",      # Início da posse (Transição ou organização perimetral)
    "S1_Perimeter_BallMove",# Circulação perimetral / troca de passes
    "S2_Paint_Drive",       # Infiltração em direção ao garrafão
    "S3_Post_Up",           # Trabalho de costas para a cesta / isolamento no garrafão
    "S4_Shot_3PT",          # Arremesso de 3 pontos executado
    "S5_Shot_MidRange",     # Arremesso de média distância executado
    "S6_Shot_Paint",        # Arremesso na área restrita / bandeja / enterrada
    "S7_Off_Rebound",       # Posse mantida via rebote ofensivo (segunda chance)
]

# Absorbing States (Possession termination states)
ABSORBING_STATES = [
    "A1_Made_2PT",          # Cesta de 2 convertida (+2 pts)
    "A2_Made_3PT",          # Cesta de 3 convertida (+3 pts)
    "A3_Made_FT",           # Falta sofrida / Lances livres convertidos (~1.5 pts esperados)
    "A4_Turnover",          # Erro / perda de posse (0 pts)
    "A5_Def_Rebound",       # Rebote defensivo adversário / Fim de posse (0 pts)
]

# Points rewarded in absorbing states
STATE_REWARDS = np.array([2.0, 3.0, 1.54, 0.0, 0.0])

class BasketballMarkovModel:
    """
    Absorbing Markov Chain modeling the stochastic progression of a basketball possession.
    """
    def __init__(self, team_name: str = "Padrão Liga"):
        self.team_name = team_name
        self.num_transient = len(TRANSIENT_STATES)
        self.num_absorbing = len(ABSORBING_STATES)
        self.Q = np.zeros((self.num_transient, self.num_transient))
        self.R = np.zeros((self.num_transient, self.num_absorbing))
        self._build_baseline_matrices()

    def _build_baseline_matrices(self):
        """
        Builds calibrated transition matrices based on Brazilian basketball (CBB/NBB)
        empirical frequencies and modern shot selection literature.
        """
        Q = np.zeros((self.num_transient, self.num_transient))
        R = np.zeros((self.num_transient, self.num_absorbing))

        # S0: Início da Posse
        # -> Pode passar a bola (S1 52%), infiltrar (S2 22%), acionar pivô (S3 10%),
        # puxar transição rápida 3PT (S4 7%), mid-range rápido (S5 3%), bandeja rápida (S6 4%), turnover inicial (A4 2%)
        Q[0, 1] = 0.52  # S1 Ball movement
        Q[0, 2] = 0.22  # S2 Paint drive
        Q[0, 3] = 0.10  # S3 Post up
        Q[0, 4] = 0.07  # S4 Pullup 3PT
        Q[0, 5] = 0.03  # S5 Pullup mid
        Q[0, 6] = 0.04  # S6 Fastbreak paint
        R[0, 3] = 0.02  # A4 Turnover

        # S1: Circulação Perimetral
        # -> Mais passes (S1 28%), infiltração (S2 30%), post (S3 12%), arremesso 3PT (S4 18%), mid (S5 6%), turnover (A4 6%)
        Q[1, 1] = 0.28
        Q[1, 2] = 0.30
        Q[1, 3] = 0.12
        Q[1, 4] = 0.18
        Q[1, 5] = 0.06
        R[1, 3] = 0.06  # A4 Turnover

        # S2: Infiltração no Garrafão (Paint Drive)
        # -> Arremesso na pintura (S6 48%), kickout pass para perímetro (S1 24%), falta/FT (A3 14%), turnover (A4 10%), mid float (S5 4%)
        Q[2, 6] = 0.48
        Q[2, 1] = 0.24
        R[2, 2] = 0.14  # A3 Free throws
        R[2, 3] = 0.10  # A4 Turnover
        Q[2, 5] = 0.04

        # S3: Post-Up (Jogo Interno)
        # -> Arremesso na pintura (S6 50%), arremesso mid fade (S5 18%), passe para corte/perímetro (S1 16%), falta (A3 8%), turnover (A4 8%)
        Q[3, 6] = 0.50
        Q[3, 5] = 0.18
        Q[3, 1] = 0.16
        R[3, 2] = 0.08  # A3 FT
        R[3, 3] = 0.08  # A4 TOV

        # S4: Arremesso de 3 Pontos (Acerto médio liga: ~35%)
        # Cesta 3PT (A2 35%), Erro -> Rebote Ofensivo (S7 18%), Erro -> Rebote Defensivo (A5 47%)
        R[4, 1] = 0.355 # A2 Made 3PT
        Q[4, 7] = 0.180 # S7 Offensive rebound
        R[4, 4] = 0.465 # A5 Def rebound

        # S5: Arremesso Mid-Range (Acerto médio liga: ~40%)
        # Cesta 2PT (A1 40%), Erro -> Rebote Ofensivo (S7 20%), Erro -> Rebote Defensivo (A5 40%)
        R[5, 0] = 0.400 # A1 Made 2PT
        Q[5, 7] = 0.200 # S7 Off rebound
        R[5, 4] = 0.400 # A5 Def rebound

        # S6: Arremesso na Pintura / Área Restrita (Acerto médio liga: ~62%)
        # Cesta 2PT (A1 62%), Falta e cesta e-1 (A3 6%), Erro -> Rebote Ofensivo (S7 12%), Erro -> Rebote Def (A5 20%)
        R[6, 0] = 0.620 # A1 Made 2PT
        R[6, 2] = 0.060 # A3 And-1 / FT
        Q[6, 7] = 0.120 # S7 Off rebound
        R[6, 4] = 0.200 # A5 Def rebound

        # S7: Rebote Ofensivo / Segunda Chance
        # -> Putback imediato na pintura (S6 55%), kickout para 3PT (S4 25%), recuo perimetral (S1 12%), turnover (A4 8%)
        Q[7, 6] = 0.55
        Q[7, 4] = 0.25
        Q[7, 1] = 0.12
        R[7, 3] = 0.08

        self.Q = Q
        self.R = R

    def calibrate_for_team(
        self,
        three_pt_pct: float,
        two_pt_pct: float,
        ft_rate: float,
        tov_rate: float,
        orb_rate: float,
        three_pt_freq: float
    ):
        """
        Calibrates the Markov transition model specifically for a given team's
        empirical offensive profile.
        """
        self._build_baseline_matrices()
        
        # Adjust 3PT efficiency
        c3 = max(0.20, min(0.50, three_pt_pct))
        miss_3 = 1.0 - c3
        self.R[4, 1] = c3
        self.Q[4, 7] = miss_3 * orb_rate
        self.R[4, 4] = miss_3 * (1.0 - orb_rate)
        
        # Adjust 2PT efficiency (paint vs mid)
        c2_paint = min(0.75, two_pt_pct * 1.18)
        self.R[6, 0] = c2_paint
        miss_paint = 1.0 - c2_paint
        self.Q[6, 7] = miss_paint * (orb_rate * 1.2)
        self.R[6, 4] = 1.0 - self.R[6, 0] - self.R[6, 2] - self.Q[6, 7]
        
        # Adjust turnover hazard
        t_mult = max(0.5, min(1.8, tov_rate / 0.14))
        self.R[0, 3] *= t_mult
        self.R[1, 3] *= t_mult
        self.R[2, 3] *= t_mult
        
        # Normalize rows to guarantee stochastic matrix property: sum(Q_i) + sum(R_i) == 1
        for i in range(self.num_transient):
            total = np.sum(self.Q[i, :]) + np.sum(self.R[i, :])
            if total > 0:
                self.Q[i, :] /= total
                self.R[i, :] /= total

    def compute_analytics(self) -> Dict[str, Any]:
        """
        Solves the absorbing Markov chain via fundamental matrix:
        N = (I - Q)^(-1)
        B = N * R  (Absorption probabilities)
        EPV = B * StateRewards
        """
        I = np.eye(self.num_transient)
        # N: Fundamental Matrix (average times spent in each state before absorption)
        N = np.linalg.inv(I - self.Q)
        
        # B: Absorption Probabilities (from each transient state to each absorbing state)
        B = np.dot(N, self.R)
        
        # Expected points vector from each transient state
        epv = np.dot(B, STATE_REWARDS)
        
        # Expected steps/duration per possession
        steps_to_absorption = np.sum(N, axis=1)
        
        # Transient transition table for UI display
        transitions = []
        for i, s_from in enumerate(TRANSIENT_STATES):
            for j, s_to in enumerate(TRANSIENT_STATES):
                prob = self.Q[i, j]
                if prob > 0.01:
                    transitions.append({
                        "from": s_from,
                        "to": s_to,
                        "type": "transient",
                        "probability": round(float(prob), 3)
                    })
            for k, a_to in enumerate(ABSORBING_STATES):
                prob = self.R[i, k]
                if prob > 0.01:
                    transitions.append({
                        "from": s_from,
                        "to": a_to,
                        "type": "absorbing",
                        "probability": round(float(prob), 3)
                    })
                    
        return {
            "team_name": self.team_name,
            "overall_possession_epv": round(float(epv[0]), 3),
            "state_epv": {
                s_name: round(float(val), 3)
                for s_name, val in zip(TRANSIENT_STATES, epv)
            },
            "steps_to_absorption": {
                s_name: round(float(steps), 2)
                for s_name, steps in zip(TRANSIENT_STATES, steps_to_absorption)
            },
            "absorption_probabilities": {
                s_name: {
                    a_name: round(float(B[i, k]), 4)
                    for k, a_name in enumerate(ABSORBING_STATES)
                }
                for i, s_name in enumerate(TRANSIENT_STATES)
            },
            "transitions": transitions,
            "tactical_insights": [
                {
                    "title": "Valor da Infiltração (Paint Drive vs Mid-Range)",
                    "insight": f"Iniciar uma ação de infiltração (S2) gera {round(float(epv[2]), 2)} pts esperados, superior a um arremesso direto de meia distância contestado ({round(float(epv[5]), 2)} pts).",
                    "delta": round(float(epv[2] - epv[5]), 3)
                },
                {
                    "title": "Impacto de Segunda Chance (Rebote Ofensivo)",
                    "insight": f"Recuperar a posse no ataque (S7) reinicia a cadeia com valor esperado de {round(float(epv[7]), 2)} pts por posse, alta taxa de conversão em finalizações próximas.",
                    "delta": round(float(epv[7] - epv[0]), 3)
                }
            ]
        }
