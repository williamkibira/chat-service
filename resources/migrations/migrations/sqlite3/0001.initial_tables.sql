CREATE TABLE participant_tb (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	uid VARCHAR(36) NOT NULL UNIQUE,
	identifier VARCHAR(36) NOT NULL UNIQUE,
	idx INTEGER
);

CREATE TRIGGER IF NOT EXISTS update_participant_idx AFTER INSERT ON participant_tb
		BEGIN
		    UPDATE participant SET idx=id WHERE id=NEW.id;
		END;

CREATE INDEX participant_tb_idx ON participant_tb(idx);

CREATE TABLE IF NOT EXISTS device_tb (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	information TEXT NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	idx INTEGER
);

CREATE TRIGGER IF NOT EXISTS update_device_idx AFTER INSERT ON device_tb
		BEGIN
		    UPDATE device_tb SET idx=id WHERE id=NEW.id;
		END;

CREATE INDEX device_tb_idx ON device_tb(idx);