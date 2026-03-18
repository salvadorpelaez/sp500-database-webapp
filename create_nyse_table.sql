-- SQL Script to create NYSE table
-- Run this in your SQLite database first

CREATE TABLE NYSE (
    Ticker          TEXT PRIMARY KEY,
    Company_Name    TEXT,
    ISIN_Code       TEXT,
    Sector          TEXT
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_nyse_ticker ON NYSE(Ticker);
CREATE INDEX IF NOT EXISTS idx_nyse_sector ON NYSE(Sector);
