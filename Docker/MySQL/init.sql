
DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';




CREATE TABLE users (
    user_id  VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nickname VARCHAR(50) NOT NULL,
    icon_image_url VARCHAR(255) DEFAULT '/static/image/icon' NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE channels (
    channel_id VARCHAR(255) PRIMARY KEY,
    channel_name VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id  VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE messages (
    message_id VARCHAR(255) PRIMARY KEY,
    message_content TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    channel_id  VARCHAR(255) NOT NULL,
    user_id  VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id) ON DELETE CASCADE
);

CREATE TABLE hobby_genres (
    hobby_genre_id VARCHAR(255) PRIMARY KEY,
    hobby_genre_name VARCHAR(50) NOT NULL
);




-- ALTER TABLE channels DROP FOREIGN KEY hobby_genre_id;
-- FOREIGN KEY (hobby_genre_id) REFERENCES hobby_genres (hobby_genre_id) 
-- ON DELETE SET NULL ON UPDATE CASCADE;
-- ALTER TABLE channels
-- ADD COLUMN hobby_genre_id VARCHAR(255) NOT NULL;
-- ALTER TABLE channels ADD CONSTRAINT hobby_genre_id
-- FOREIGN KEY (hobby_genre_id)
-- REFERENCES hobby_genres(hobby_genre_id);

INSERT INTO users(user_id, email, password, nickname,  icon_image_url) VALUES('970af84c-dd40-47ff-af23-282b72b7cca8','test@gmail.com','password','testuser','37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578');


-- ALTER TABLE channels DROP FOREIGN KEY user_id;
-- FOREIGN KEY (user_id) REFERENCES users (user_id) 
-- ON DELETE SET NULL ON UPDATE CASCADE;
-- INSERT INTO channels(channel_id, channel_name, user_id) VALUES('1','サッカー','1');

-- INSERT INTO messages(message_id, message_content,  channel_id,  user_id) VALUES('1','こんにちは！','1','1');

