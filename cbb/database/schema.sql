-- DuckDB Schema for Basquete BR — Atlas Tático

CREATE TABLE IF NOT EXISTS matches (
    match_id VARCHAR PRIMARY KEY,
    competition VARCHAR NOT NULL,
    season VARCHAR NOT NULL,
    match_date DATE,
    phase VARCHAR,
    team_home VARCHAR NOT NULL,
    team_away VARCHAR NOT NULL,
    score_home INTEGER,
    score_away INTEGER,
    validation_status VARCHAR DEFAULT 'VALID',
    source_url VARCHAR,
    raw_hash VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS team_boxscores (
    match_id VARCHAR NOT NULL,
    team_name VARCHAR NOT NULL,
    season VARCHAR DEFAULT '2026-2027',
    is_home BOOLEAN NOT NULL,
    pts INTEGER,
    fgm INTEGER,
    fga INTEGER,
    fg3m INTEGER,
    fg3a INTEGER,
    ftm INTEGER,
    fta INTEGER,
    orb INTEGER,
    drb INTEGER,
    trb INTEGER,
    ast INTEGER,
    stl INTEGER,
    blk INTEGER,
    tov INTEGER,
    pf INTEGER,
    fd INTEGER,
    possessions DOUBLE,
    pace DOUBLE,
    ortg DOUBLE,
    drtg DOUBLE,
    net_rating DOUBLE,
    efg_pct DOUBLE,
    tov_pct DOUBLE,
    orb_pct DOUBLE,
    ftr DOUBLE,
    PRIMARY KEY (match_id, team_name, season)
);

CREATE TABLE IF NOT EXISTS player_boxscores (
    id VARCHAR PRIMARY KEY,
    match_id VARCHAR NOT NULL,
    player_name VARCHAR NOT NULL,
    team_name VARCHAR NOT NULL,
    season VARCHAR DEFAULT '2026-2027',
    number VARCHAR,
    position VARCHAR,
    min_played DOUBLE,
    pts INTEGER,
    fgm INTEGER,
    fga INTEGER,
    fg3m INTEGER,
    fg3a INTEGER,
    ftm INTEGER,
    fta INTEGER,
    orb INTEGER,
    drb INTEGER,
    trb INTEGER,
    ast INTEGER,
    stl INTEGER,
    blk INTEGER,
    tov INTEGER,
    pf INTEGER,
    fd INTEGER,
    dunks INTEGER,
    plus_minus INTEGER,
    fiba_pir DOUBLE,
    game_score DOUBLE,
    ts_pct DOUBLE,
    usg_pct DOUBLE
);

CREATE TABLE IF NOT EXISTS cbb_rankings_historical (
    id VARCHAR PRIMARY KEY,
    naipe VARCHAR NOT NULL,
    ano_temporada INTEGER,
    fundamento VARCHAR NOT NULL,
    tipo_metrica VARCHAR NOT NULL,
    posicao INTEGER,
    jogador_nome VARCHAR NOT NULL,
    jogador_numero VARCHAR,
    equipe VARCHAR,
    valor_principal DOUBLE,
    jogos INTEGER,
    tempo_medio VARCHAR
);

CREATE TABLE IF NOT EXISTS cbb_hall_athletes (
    nome VARCHAR PRIMARY KEY,
    nome_completo VARCHAR,
    foto VARCHAR,
    posicao VARCHAR,
    detalhes VARCHAR
);

CREATE TABLE IF NOT EXISTS shot_events (
    shot_id VARCHAR PRIMARY KEY,
    match_id VARCHAR NOT NULL,
    team_name VARCHAR NOT NULL,
    player_name VARCHAR NOT NULL,
    season VARCHAR DEFAULT '2026-2027',
    period INTEGER,
    clock_seconds INTEGER,
    x_m DOUBLE,
    y_m DOUBLE,
    zone VARCHAR,
    made BOOLEAN,
    points_value INTEGER
);

CREATE TABLE IF NOT EXISTS audit_log (
    event_id VARCHAR PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR NOT NULL,
    records_count INTEGER,
    payload_hash VARCHAR,
    status VARCHAR
);
