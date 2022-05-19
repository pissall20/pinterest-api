CREATE ROLE siddhesh WITH LOGIN PASSWORD 'abc@123';

ALTER ROLE siddhesh CREATEDB;

CREATE DATABASE events;

GRANT ALL PRIVILEGES ON DATABASE events TO siddhesh;

CREATE TABLE IF NOT EXISTS pinterest (
            "unique_id" VARCHAR PRIMARY KEY,
            "category" VARCHAR,
            "title" VARCHAR,
            "description" VARCHAR,
            "index" INTEGER,
            "follower_count" INTEGER,
            "tag_list" VARCHAR,
            "is_image_or_video" VARCHAR,
            "image_src" VARCHAR,
            "downloaded" INTEGER,
            "save_location" VARCHAR,
            "tag_list_clean" VARCHAR[]);

-- Schema of the datatable
-- |-- category: string (nullable = true)
-- |-- index: integer (nullable = true)
-- |-- unique_id: string (nullable = true)
-- |-- title: string (nullable = true)
-- |-- description: string (nullable = true)
-- |-- follower_count: integer (nullable = true)
-- |-- tag_list: string (nullable = true)
-- |-- is_image_or_video: string (nullable = true)
-- |-- image_src: string (nullable = true)
-- |-- downloaded: integer (nullable = true)
-- |-- save_location: string (nullable = true)
-- |-- tag_list_clean: array (nullable = true)
-- |    |-- element: string (containsNull = true)
