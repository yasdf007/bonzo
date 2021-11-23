create table IF NOT EXISTS user_server(
    id BIGSERIAL PRIMARY KEY,
    userid BIGINT NOT NULL,
    serverid BIGINT NOT NULL,
    UNIQUE (userid, serverid)
);
create table IF NOT EXISTS xpInfo(
    id BIGINT PRIMARY KEY REFERENCES user_server(id) ON DELETE CASCADE,
    XP BIGINT DEFAULT 0,
    LVL INT DEFAULT 0,
    NextTextXpAt TIMESTAMP DEFAULT NOW()
);
create table IF NOT EXISTS server_settings(
    id BIGSERIAL primary key,
    server_id BIGINT UNIQUE NOT NULL,
    free_games_channel_id BIGINT UNIQUE,
    prefix varchar(5),
    locale varchar(2)
);