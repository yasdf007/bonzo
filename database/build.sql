create table IF NOT EXISTS user_server(
    id BIGSERIAL PRIMARY KEY,
    userid BIGINT NOT NULL,
    serverid BIGINT NOT NULL,
    UNIQUE (userid, serverid)
);
create index IF NOT EXISTS user_server_user_id_index on user_server using btree (userid);
create index IF NOT EXISTS user_server_server_id_index on user_server using btree (serverid);
create table IF NOT EXISTS xpInfo(
    id BIGINT PRIMARY KEY REFERENCES user_server(id) ON DELETE CASCADE,
    XP BIGINT DEFAULT 0,
    LVL INT DEFAULT 0,
    NextTextXpAt TIMESTAMP DEFAULT NOW()
);
create table IF NOT EXISTS free_games_channel(
    id bigserial,
    server_id bigint NOT NULL,
    channel_id bigint NOT NULL,
    UNIQUE (server_id, channel_id)
);
create index IF NOT EXISTS free_games_server_id_index on free_games_channel using btree (server_id);
create index IF NOT EXISTS free_games_channel_id_index on free_games_channel using btree (channel_id);