CREATE TABLE identity_tb (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	participant_identity VARCHAR(36) NOT NULL UNIQUE,
	routing_identity VARCHAR(36) NOT NULL UNIQUE,
	idx INTEGER
);

CREATE TRIGGER IF NOT EXISTS update_identity_idx AFTER INSERT ON identity_tb
		BEGIN
		    UPDATE identity_tb SET idx=id WHERE id=NEW.id;
		END;

CREATE INDEX identity_tb_idx ON identity_tb(idx);

CREATE TABLE IF NOT EXISTS device_information_tb (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	information TEXT NOT NULL,
	identity_id INTEGER NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	idx INTEGER
);

CREATE TRIGGER IF NOT EXISTS update_device_info_idx AFTER INSERT ON device_information_tb
		BEGIN
		    UPDATE device_tb SET idx=id WHERE id=NEW.id;
		END;

CREATE INDEX device_information_idx ON device_information_tb(idx);