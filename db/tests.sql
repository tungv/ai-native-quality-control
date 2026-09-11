\set ON_ERROR_STOP on
BEGIN;

DO $$
DECLARE
    actual text[];
BEGIN
    -- Filter scope before ranking; secondary order makes equal scores stable.
    SELECT array_agg(sku ORDER BY distance, sku) INTO actual
    FROM (
        SELECT sku, embedding <=> '[1,0,0]'::vector AS distance
        FROM products
        WHERE tenant_id = 'shop-a' AND in_stock
        ORDER BY distance, sku
        LIMIT 2
    ) ranked;
    IF actual IS DISTINCT FROM ARRAY['trail-shoes', 'rain-jacket'] THEN
        RAISE EXCEPTION 'Filtered cosine ranking mismatch: %', actual;
    END IF;

    SELECT array_agg(sku ORDER BY sku) INTO actual
    FROM products WHERE tenant_id = 'missing-shop';
    IF actual IS NOT NULL THEN
        RAISE EXCEPTION 'Missing tenant must have no results';
    END IF;

    -- A negative control demonstrates why a similarity score is not isolation.
    SELECT array_agg(sku ORDER BY distance, sku) INTO actual
    FROM (
        SELECT sku, embedding <=> '[1,0,0]'::vector AS distance
        FROM products WHERE in_stock
        ORDER BY distance, sku LIMIT 2
    ) unscoped;
    IF NOT ('private-shoes' = ANY(actual)) THEN
        RAISE EXCEPTION 'Negative control no longer exposes the cross-tenant fixture';
    END IF;

    BEGIN
        INSERT INTO products VALUES ('bad-price', 'shop-a', 'Invalid', -1, true, '[1,0,0]');
        RAISE EXCEPTION 'Negative price unexpectedly accepted';
    EXCEPTION WHEN check_violation THEN NULL;
    END;

    BEGIN
        INSERT INTO products VALUES ('zero-vector', 'shop-a', 'Invalid', 100, true, '[0,0,0]');
        RAISE EXCEPTION 'Zero vector unexpectedly accepted';
    EXCEPTION WHEN check_violation THEN NULL;
    END;

    BEGIN
        INSERT INTO products VALUES ('bad-dimensions', 'shop-a', 'Invalid', 100, true, '[1,0]');
        RAISE EXCEPTION 'Wrong vector dimensions unexpectedly accepted';
    EXCEPTION WHEN data_exception THEN NULL;
    END;

    RAISE NOTICE 'PASS: filtered ranking, missing tenant, leakage control, price, norm, dimensions';
END $$;

ROLLBACK;
