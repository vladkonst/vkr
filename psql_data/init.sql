CREATE TABLE skeys(
    id SERIAL PRIMARY KEY,
    skey VARCHAR,
    counter INTEGER
);
CREATE TABLE otp_data(
    id SERIAL PRIMARY KEY,
    hashed_otp VARCHAR,
    unique_id UUID,
    verified BOOLEAN,
    gen_try_count SMALLINT,
    valid_try_count SMALLINT,
    experation_time TIMESTAMP,
    call_id VARCHAR
);