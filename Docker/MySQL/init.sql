
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

CREATE TABLE hobby_genres (
    hobby_genre_id VARCHAR(255) PRIMARY KEY,
    hobby_genre_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE channels (
    channel_id VARCHAR(255) PRIMARY KEY,
    channel_name VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id  VARCHAR(255) NOT NULL,
    hobby_genre_id VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (hobby_genre_id)
    REFERENCES hobby_genres(hobby_genre_id)
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


INSERT INTO users(user_id, email, password, nickname,  icon_image_url) VALUES('970af84c-dd40-47ff-af23-282b72b7cca8','test@gmail.com','password','testuser','37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578');
INSERT INTO hobby_genres(hobby_genre_id, hobby_genre_name) VALUES('3b2f1a2a-5d6f-4a9f-bc3b-23429dfb21ac','スポーツ');


INSERT INTO channels(channel_id, channel_name, user_id, hobby_genre_id) VALUES('c8d1d11e-0f22-4e63-9039-9a8e10b24360','サッカー','970af84c-dd40-47ff-af23-282b72b7cca8',"3b2f1a2a-5d6f-4a9f-bc3b-23429dfb21ac");

INSERT INTO messages(message_id, message_content,  channel_id,  user_id) VALUES('91f3f5ab-4bce-4c77-8de7-2b215f6fd1a6','こんにちは！','c8d1d11e-0f22-4e63-9039-9a8e10b24360','970af84c-dd40-47ff-af23-282b72b7cca8');

