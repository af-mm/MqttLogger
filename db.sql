create table mqtt_broker_history(
	id serial primary key,
	ts timestamptz not null default current_timestamp,
	topic varchar(255) not null,
	message varchar(4096) not NULL
);

create table mqtt_broker_last_values(
	topic varchar(255) not null primary key,
	message varchar(4096) not null,
	ts timestamptz not null default current_timestamp
);
