CREATE TABLE IF NOT EXISTS identity_tb (
	id SERIAL PRIMARY KEY,
	participant_identifier UUID NOT NULL UNIQUE,
	routing_identifier UUID NOT NULL UNIQUE,
	idx BIGSERIAL NOT NULL UNIQUE
);

CREATE INDEX identity_index_idx ON identity_tb USING btree(idx);

CREATE TABLE IF NOT EXISTS device_information_tb (
	id SERIAL PRIMARY KEY,
	information TEXT NOT NULL,
	identity_id BIGINT NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	idx BIGSERIAL NOT NULL UNIQUE
);

CREATE INDEX device_information_idx ON device_information_tb USING btree(idx);

