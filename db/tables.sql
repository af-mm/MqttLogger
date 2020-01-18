CREATE TABLE mqtt_broker_history(
	id serial PRIMARY KEY,
	ts timestamptz NOT NULL DEFAULT current_timestamp,
	topic varchar(255) NOT NULL,
	message varchar(4096) NOT NULL
);

CREATE TABLE mqtt_broker_last_values(
	topic varchar(255) NOT NULL PRIMARY KEY,
	message varchar(4096) NOT NULL,
	ts timestamptz NOT NULL DEFAULT current_timestamp
);
