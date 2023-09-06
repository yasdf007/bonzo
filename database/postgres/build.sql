create table IF NOT EXISTS user_server(
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    server_id BIGINT NOT NULL,
    UNIQUE (user_id, server_id)
);
create table IF NOT EXISTS xp_info(
    id BIGINT PRIMARY KEY REFERENCES user_server(id) ON DELETE CASCADE,
    xp BIGINT DEFAULT 0,
    text_xp_at BIGINT DEFAULT 0
);
create table IF NOT EXISTS server_settings(
    id BIGSERIAL primary key,
    server_id BIGINT UNIQUE NOT NULL,
    free_games_channel_id BIGINT UNIQUE,
    prefix varchar(5),
    locale varchar(2)
);