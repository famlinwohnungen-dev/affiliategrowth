-- Rückmeldungen von Lesern.
--
-- Bewusst minimal: Es wird nur gespeichert, was gebraucht wird, um die Seite
-- zu verbessern. Keine IP-Adressen, keine Kennungen, kein Tracking. Wer keine
-- E-Mail hinterlässt, bleibt vollständig anonym.

CREATE TABLE IF NOT EXISTS feedback (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  erstellt_am TEXT NOT NULL,                       -- ISO-8601, UTC
  seite       TEXT NOT NULL,                       -- Pfad, z. B. /artikel/g-data-vs-bitdefender/
  bewertung   TEXT CHECK (bewertung IN ('gut','schlecht')),
  nachricht   TEXT,                                -- optionaler Freitext
  email       TEXT,                                -- optional, nur für Rückfragen
  quelle      TEXT NOT NULL                        -- 'artikel' | 'widget'
);

-- Häufigste Abfragen: neueste zuerst, und Bewertungen je Seite.
CREATE INDEX IF NOT EXISTS idx_feedback_erstellt ON feedback (erstellt_am DESC);
CREATE INDEX IF NOT EXISTS idx_feedback_seite    ON feedback (seite, bewertung);
