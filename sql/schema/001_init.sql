-- Kasandra — schemat SQLite v1
-- Projektowany na wiele źródeł (KRS, CRBR, przyszłe: KRZ, itp.)
-- source TEXT jest polem otwartym — nowe źródło = nowe wiersze, nie nowe tabele.

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

-- --------------------------------------------------------------------------
-- companies — lista obserwowanych podmiotów (watchlista)
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS companies (
    id          INTEGER PRIMARY KEY,
    krs         TEXT    NOT NULL UNIQUE,
    nip         TEXT,
    regon       TEXT,
    slug        TEXT    NOT NULL UNIQUE,     -- czytelny skrót, np. "zabka"
    nazwa       TEXT,
    crbr_exempt INTEGER NOT NULL DEFAULT 0,  -- 1 = zwolniona z CRBR (np. GPW)
    notes       TEXT,
    created_at  TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

-- --------------------------------------------------------------------------
-- snapshots — każdy pobrany i znormalizowany odczyt, dowolne źródło
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS snapshots (
    id                  INTEGER PRIMARY KEY,
    company_id          INTEGER NOT NULL REFERENCES companies(id),
    source              TEXT    NOT NULL,   -- 'krs' | 'crbr' | ...
    collected_at        TEXT    NOT NULL,   -- YYYY-MM-DD
    status              TEXT    NOT NULL DEFAULT 'ok',
        -- 'ok'          — dane pobrane i znormalizowane
        -- 'brak_wpisow' — źródło nie zwróciło wyników
        -- 'error'       — błąd pobierania
    normalized_payload  TEXT,               -- JSON; NULL gdy status != 'ok'
    payload_hash        TEXT,               -- SHA-256 normalized_payload; do szybkiego diffowania
    raw_path            TEXT,               -- ścieżka do surowego pliku (rel. od REPO_ROOT)
    created_at          TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),

    UNIQUE (company_id, source, collected_at)
);

CREATE INDEX IF NOT EXISTS idx_snapshots_company_source
    ON snapshots (company_id, source);

CREATE INDEX IF NOT EXISTS idx_snapshots_collected_at
    ON snapshots (collected_at);

-- --------------------------------------------------------------------------
-- changes — zmiany wykryte między kolejnymi snapshotami (Blok 2)
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS changes (
    id              INTEGER PRIMARY KEY,
    company_id      INTEGER NOT NULL REFERENCES companies(id),
    source          TEXT    NOT NULL,
    alert_rule      TEXT    NOT NULL,   -- np. 'A-ZARZAD-PREZES', 'A-CRBR-BEN-NOWY'
    field           TEXT,               -- które pole zmiany; NULL = zmiana binarna
    value_before    TEXT,               -- JSON
    value_after     TEXT,               -- JSON
    snapshot_old_id INTEGER REFERENCES snapshots(id),
    snapshot_new_id INTEGER REFERENCES snapshots(id),
    detected_at     TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE INDEX IF NOT EXISTS idx_changes_company
    ON changes (company_id);

CREATE INDEX IF NOT EXISTS idx_changes_rule
    ON changes (alert_rule);

-- --------------------------------------------------------------------------
-- alerts — zgrupowane, czytelne alerty gotowe do wyświetlenia (Blok 2)
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS alerts (
    id           INTEGER PRIMARY KEY,
    company_id   INTEGER NOT NULL REFERENCES companies(id),
    alert_rule   TEXT    NOT NULL,
    title        TEXT    NOT NULL,
    summary      TEXT    NOT NULL,
    evidence     TEXT,               -- JSON — lista change_id lub inline
    priority     TEXT    NOT NULL,   -- 'N' | 'S' | 'W' | 'K'
    status       TEXT    NOT NULL DEFAULT 'new',
        -- 'new' | 'seen' | 'dismissed'
    generated_at TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE INDEX IF NOT EXISTS idx_alerts_company
    ON alerts (company_id);

CREATE INDEX IF NOT EXISTS idx_alerts_status
    ON alerts (status);

CREATE INDEX IF NOT EXISTS idx_alerts_priority
    ON alerts (priority);
