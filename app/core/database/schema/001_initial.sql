-- ================================================
-- 1) agents
-- ================================================
CREATE TABLE agents (
    id          SERIAL       PRIMARY KEY,
    name        VARCHAR(255),
    created_at  TIMESTAMP,
    updated_at  TIMESTAMP
);

-- ================================================
-- 2) processes
--    - Each process belongs to one agent.
-- ================================================
CREATE TABLE processes (
    id         SERIAL       PRIMARY KEY,
    command    VARCHAR(255),
    pid        INTEGER,
    agent_id   INTEGER      NOT NULL,
    CONSTRAINT fk_processes_agent
        FOREIGN KEY (agent_id) REFERENCES agents (id)
        ON DELETE CASCADE
);

-- ================================================
-- 3) rules
--    - Each rule belongs to one agent.
-- ================================================
CREATE TABLE rules (
    id         SERIAL       PRIMARY KEY,
    saddr      VARCHAR(255),
    daddr      VARCHAR(255),
    sport      INTEGER,
    dport      INTEGER,
    protocol   VARCHAR(50),
    action     VARCHAR(50),
    chain      VARCHAR(50),
    priority   INTEGER,
    comment    VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    agent_id   INTEGER      NOT NULL,
    CONSTRAINT fk_rules_agent
        FOREIGN KEY (agent_id) REFERENCES agents (id)
        ON DELETE CASCADE
);

-- ================================================
-- 4) users table
-- ================================================
CREATE TABLE users (
    id       SERIAL       PRIMARY KEY,
    email    VARCHAR(255),
    name     VARCHAR(255),
    password VARCHAR(255)
);
