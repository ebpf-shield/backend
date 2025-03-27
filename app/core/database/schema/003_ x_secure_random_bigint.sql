CREATE OR REPLACE FUNCTION secure_random_bigint() RETURNS bigint AS $$
DECLARE
    v_bytes bytea;
    v_value bigint := 0;
    v_length integer := 8;
    i integer := 0;
BEGIN
	v_bytes := gen_random_bytes(v_length);
	FOR i IN 0..v_length-1 LOOP
		v_value := (v_value << 8) | get_byte(v_bytes, i);
	END LOOP;
    RETURN v_value::bigint;
END;
$$ LANGUAGE plpgsql;