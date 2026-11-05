# Definições Metodológicas e Fórmulas Analíticas

Este documento detalha as fórmulas matemáticas, pressupostos estocásticos e literatura de suporte empregados no **Basquete BR — Atlas Tático**.

---

## 1. Dean Oliver (2004) — Quatro Fatores de Basquetebol

### 1.1 Posse de Bola Estimada (Possessions)
$$\text{Poss} = \text{FGA} + 0.44 \times \text{FTA} - \text{ORB} + \text{TOV}$$
- **Fator 0.44:** Ponderação empírica para lances livres (considerando faltas de 2 e 3 lances, faltas técnicas e cestas e-falta "and-1").

### 1.2 Ritmo Padronizado FIBA 40 Minutos (Pace 40m)
$$\text{Pace} = 40 \times \frac{\text{Poss}}{\text{MP} / 5}$$
Ao contrário da NBA (48 minutos), os jogos FIBA têm duração regulamentar de 40 minutos.

### 1.3 Quatro Fatores (Pesos Empíricos)
1. **Aproveitamento Efetivo (eFG% — Peso ~40%):**
   $$eFG\% = \frac{\text{FGM} + 0.5 \times 3\text{PM}}{\text{FGA}}$$
2. **Taxa de Desperdício de Posse (TOV% — Peso ~25%):**
   $$TOV\% = \frac{\text{TOV}}{\text{FGA} + 0.44 \times \text{FTA} + \text{TOV}}$$
3. **Taxa de Rebote Ofensivo (ORB% — Peso ~20%):**
   $$ORB\% = \frac{\text{ORB}}{\text{ORB} + \text{Opp\_DRB}}$$
4. **Taxa de Lances Livres (FTR — Peso ~15%):**
   $$FTR = \frac{\text{FTA}}{\text{FGA}}$$

### 1.4 Eficiência Ofensiva e Defensiva
- **Offensive Rating (ORtg):** $\text{ORtg} = 100 \times \frac{\text{PTS}}{\text{Poss}}$
- **Defensive Rating (DRtg):** $\text{DRtg} = 100 \times \frac{\text{Opp\_PTS}}{\text{Opp\_Poss}}$
- **Net Rating:** $\text{NetRtg} = \text{ORtg} - \text{DRtg}$

### 1.5 Expectativa Pitagórica de Vitórias (Pythagorean Win Expectancy)
$$\text{ExpWin\%} = \frac{\text{ORtg}^{13.91}}{\text{ORtg}^{13.91} + \text{DRtg}^{13.91}}$$
O expoente $13.91$ foi calibrado por Daryl Morey e Dean Oliver especificamente para a distribuição de pontos no basquete.

---

## 2. Modelagem Estocástica de Markov (Sandholtz & Bornn 2020)

Uma posse de basquete é modelada como um processo estocástico em tempo discreto com estados transitórios $Q$ e absorventes $R$.

### 2.1 Forma Canônica da Matriz de Transição
$$P = \begin{pmatrix} Q & R \\ 0 & I \end{pmatrix}$$
Onde:
- $Q \in \mathbb{R}^{m \times m}$ representa as probabilidades de transição entre estados não-terminais.
- $R \in \mathbb{R}^{m \times k}$ representa as probabilidades de transição para os estados absorventes (cesta 2PT, cesta 3PT, lance livre, turnover, rebote defensivo).

### 2.2 Matriz Fundamental
$$N = (I - Q)^{-1} = I + Q + Q^2 + Q^3 + \dots$$
O elemento $n_{ij}$ da matriz fundamental indica o número médio de vezes que o ataque passa pelo estado transitório $j$ dado que iniciou no estado $i$.

### 2.3 Probabilidades de Absorção e Valor Esperado (EPV)
$$B = N \cdot R$$
$$EPV(S_i) = \sum_{k=1}^5 B_{i, k} \times \text{Recompensa}(A_k)$$

---

## 3. Eficiência Espacial de Kirk Goldsberry (2012, 2019)

### 3.1 Pontos por Arremesso (Points Per Shot — PPS)
$$PPS_{\text{zona}} = \frac{\text{Pontos Marcados}_{\text{zona}}}{\text{Tentativas}_{\text{zona}}}$$

### 3.2 Superávit de Eficiência Espacial (Spatial Efficiency Surplus — SES)
$$SES = PPS_{\text{zona}} - PPS_{\text{benchmark\_liga}}$$
- **Zona Quente (Hot):** $SES \ge +0.10$ pts/arremesso.
- **Zona Neutra (Neutral):** $-0.10 < SES < +0.10$ pts/arremesso.
- **Zona Fria (Cold):** $SES \le -0.10$ pts/arremesso.

---

## 4. Métricas Individuais e Incerteza Amostral

### 4.1 True Shooting Percentage (TS%)
$$TS\% = \frac{\text{PTS}}{2 \times (\text{FGA} + 0.44 \times \text{FTA})}$$

### 4.2 Taxa de Uso de Posse (USG%)
$$USG\% = 100 \times \frac{(\text{FGA} + 0.44 \times \text{FTA} + \text{TOV}) \times (\text{Tm\_MP} / 5)}{\text{MP} \times (\text{Tm\_FGA} + 0.44 \times \text{Tm\_FTA} + \text{Tm\_TOV})}$$

### 4.3 Performance Index Rating Oficial FIBA (PIR)
$$PIR = (\text{PTS} + \text{TRB} + \text{AST} + \text{STL} + \text{BLK} + \text{FR}) - ((\text{FGA} - \text{FGM}) + (\text{FTA} - \text{FTM}) + \text{TOV} + \text{FC})$$

### 4.4 Intervalo de Confiança de Wilson (95%)
$$w = \frac{p + \frac{z^2}{2n} \pm z \sqrt{\frac{p(1-p)}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}$$
Com $z = 1.96$ para 95% de confiança bicaudal.
