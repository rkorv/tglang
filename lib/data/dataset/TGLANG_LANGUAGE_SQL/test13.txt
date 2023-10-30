DROP DATABASE IF EXISTS media;
CREATE DATABASE media;
USE media;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) COMMENT 'Имя пользователя',
  nickname VARCHAR(255) UNIQUE COMMENT 'Псевдоним пользователя',
  email VARCHAR(255) COMMENT 'Почта пользователя',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  ) COMMENT = 'Пользователь';

DROP TABLE IF EXISTS categories;
CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) COMMENT 'Название файла'
  );

DROP TABLE IF EXISTS files;
CREATE TABLE files (
  id SERIAL PRIMARY KEY,
  files_name VARCHAR(255) COMMENT 'Название файла',
  description TEXT COMMENT 'Описание',
  path VARCHAR(255) COMMENT 'Путь к файлу',
  users_id BIGINT(20) UNSIGNED,
  files_id BIGINT(20) UNSIGNED,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (users_id) REFERENCES users(id),
  FOREIGN KEY (files_id) REFERENCES categories(id)
  ) COMMENT = 'Файлы пользователя';