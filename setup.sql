
-- WealthNest PostgreSQL Setup Script


-- Drop existing tables (to reset the database)
DROP TABLE IF EXISTS holdings CASCADE;
DROP TABLE IF EXISTS instruments CASCADE;
DROP TABLE IF EXISTS users CASCADE;


-- USERS TABLE

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- INSTRUMENTS TABLE

CREATE TABLE instruments (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    sector VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- HOLDINGS TABLE

CREATE TABLE holdings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    instrument_id INTEGER NOT NULL REFERENCES instruments(id) ON DELETE CASCADE,
    total_units DECIMAL(18, 4) DEFAULT 0.0,
    average_cost DECIMAL(18, 2) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SAMPLE DATA
-- USERS
INSERT INTO users (username, email, hashed_password)
VALUES
('user1', 'a@g.com', 'hashed_pw_123'),
('testuser', 'test@example.com', 'hashed_pw_456');

-- INSTRUMENTS
INSERT INTO instruments (symbol, name, sector)
VALUES
('TCS', 'Tata Consultancy Services', 'IT'),
('INFY', 'Infosys Ltd', 'IT'),
('HDFCBANK', 'HDFC Bank Ltd', 'Banking'),
('RELIANCE', 'Reliance Industries Ltd', 'Energy'),
('ITC', 'ITC Ltd', 'FMCG'),
('SBIN', 'State Bank of India', 'Banking');

-- HOLDINGS
-- User1's Holdings
INSERT INTO holdings (user_id, instrument_id, total_units, average_cost)
VALUES
(1, 1, 5.0, 3200.00),   -- TCS
(1, 2, 10.0, 1450.00),  -- INFY
(1, 4, 8.0, 2300.00);   -- RELIANCE

-- TestUser's Holdings
INSERT INTO holdings (user_id, instrument_id, total_units, average_cost)
VALUES
(2, 3, 12.0, 1650.00),  -- HDFCBANK
(2, 5, 15.0, 420.00),   -- ITC
(2, 6, 20.0, 630.00);   -- SBIN


-- Verification Queries

-- SELECT * FROM users;
-- SELECT * FROM instruments;
-- SELECT * FROM holdings;
