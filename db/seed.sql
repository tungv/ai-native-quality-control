-- Original synthetic data, MIT. Three-dimensional vectors teach mechanics;
-- they are hand-authored, not embeddings from a model.
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE products (
    sku text PRIMARY KEY,
    tenant_id text NOT NULL,
    name text NOT NULL,
    price_cents integer NOT NULL CHECK (price_cents >= 0),
    in_stock boolean NOT NULL,
    embedding vector(3) NOT NULL,
    CHECK (vector_norm(embedding) > 0)
);

INSERT INTO products VALUES
('trail-shoes', 'shop-a', 'Trail Shoes', 12900, true, '[1,0,0]'),
('rain-jacket', 'shop-a', 'Rain Jacket', 8900, true, '[0.8,0.6,0]'),
('city-backpack', 'shop-a', 'City Backpack', 5900, false, '[0,0,1]'),
('private-shoes', 'shop-b', 'Private Shop Shoes', 11900, true, '[1,0,0]');
