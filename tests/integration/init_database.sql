-- create database
CREATE DATABASE IF NOT EXISTS `scada`;

-- create the user for test database
CREATE USER 'scada_user'@'%' IDENTIFIED BY 'scada';
GRANT CREATE, ALTER, INDEX, LOCK TABLES, REFERENCES, UPDATE, DELETE, DROP, SELECT, INSERT ON `scada`.* TO 'scada_user'@'%';

FLUSH PRIVILEGES;

-- add data
INSERT INTO scada.company SET name='Рога и копыта', inn=1234566778, kpp=12345678;
INSERT INTO scada.tech_nest_location SET latitude='55.7522', longitude='37.6156', address='Санкт-Петербург, Дворцовая наб., 38';
INSERT INTO scada.tech_nest_location SET latitude='55.7539303', longitude='37.620795', address='Красная пл., Москва, 109012';
INSERT INTO scada.tech_nest SET location_id=1, company_id=1;
INSERT INTO scada.tech_nest SET location_id=2, company_id=1;
INSERT INTO scada.device SET mode='AUTO', ammeter='123', tech_nest_id=1;
INSERT INTO scada.device SET mode='MANUAL', ammeter='321', tech_nest_id=1;
INSERT INTO scada.device SET mode='AUTO', ammeter='123', tech_nest_id=2;
INSERT INTO scada.device SET mode='ACCIDENT', ammeter='321', tech_nest_id=2;