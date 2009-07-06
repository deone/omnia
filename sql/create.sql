grant all on procure.* to 'procure'@'localhost' identified by 'procure';
grant all on procure_test.* to 'procure'@'localhost' identified by 'procure';

create database if not exists procure;
create database if not exists procure_test;
