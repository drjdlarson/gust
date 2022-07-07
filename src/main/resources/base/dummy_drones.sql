drop table if EXISTS drone_collection;
drop table if EXISTS drone0_rate1;
drop table if EXISTS drone0_rate2;
drop table if EXISTS drone1_rate1;
drop table if EXISTS drone1_rate2;
CREATE TABLE if not EXISTS drone_collection (
  uid INTEGER PRIMARY KEY,
  name TEXT
 );
 CREATE TABLE if not EXISTS drone0_rate1 (
    m_time float PRIMARY key,
    flt_mode integer,
    arm_state bool,
    voltage float,
    current float,
    next_wp integer,
    time_of_flight float,
    relay_switch bool,
    engine_switch bool,
    connection_status bool
 );
 Create table if not exists drone0_rate2 (
   m_time float PRIMARY key,
   roll float,
   pitch float,
   heading float,
   track float,
   vspeed float,
   gndspeed float,
   airspeed float,
   latitude float,
   longitude float,
   altitude float
 );
 
  CREATE TABLE if not EXISTS drone1_rate1 (
    m_time float PRIMARY key,
    flt_mode integer,
    arm_state bool,
    voltage float,
    current float,
    next_wp integer,
    time_of_flight float,
    relay_switch bool,
    engine_switch bool,
    connection_status bool
 );
 Create table if not exists drone1_rate2 (
   m_time float PRIMARY key,
   roll float,
   pitch float,
   heading float,
   track float,
   vspeed float,
   gndspeed float,
   airspeed float,
   latitude float,
   longitude float,
   altitude float
 );
 
 insert into drone_collection (uid, name) VALUES (0, 'drone0');
 insert into drone_collection (uid, name) VALUES (1, 'drone1');
 
 insert into drone0_rate1 (
   m_time, flt_mode, arm_state, voltage, current, next_wp, time_of_flight, 
   relay_switch, engine_switch, connection_status)
 VALUES (0.0, 2, 1, 4.6, 5.7, 2, 3.4, 0, 1, 1);
 insert into drone0_rate1 (
   m_time, flt_mode, arm_state, voltage, current, next_wp, time_of_flight, 
   relay_switch, engine_switch, connection_status)
 VALUES (0.02, 3, 0, 3.4, -5.3, 6, 3.2, 1, 0, 0);
 
 insert into drone0_rate2 (
   m_time, roll, pitch, heading, track, vspeed, gndspeed, airspeed, latitude, longitude, altitude)
 VALUES (0.01, 2.3, 30.4, 2, 2.4, 0.3, 0.5, 10.0, 43, -87, 100);
  insert into drone0_rate2 (
   m_time, roll, pitch, heading, track, vspeed, gndspeed, airspeed, latitude, longitude, altitude)
 VALUES (0.04, 2.3, 3.4, 3, 5.4, 1.3, 2.2, 1.4, 44, -88, 150);
 
 
 insert into drone1_rate1 (
   m_time, flt_mode, arm_state, voltage, current, next_wp, time_of_flight, 
   relay_switch, engine_switch, connection_status)
 VALUES (0.02, 1, 0, 5.6, -9.7, 1, 4.4, 1, 0, 1);
 insert into drone1_rate1 (
   m_time, flt_mode, arm_state, voltage, current, next_wp, time_of_flight, 
   relay_switch, engine_switch, connection_status)
 VALUES (0.03, 1, 0, 5.4, -5.3, 7, 3.2, 1, 1, 0);
 
 insert into drone1_rate2 (
   m_time, roll, pitch, heading, track, vspeed, gndspeed, airspeed, latitude, longitude, altitude)
 VALUES (0.01, 4.3, 0.4, 3, 5.4, 1.3, 2.5, 1.0, 53, -97, 110);
  insert into drone1_rate2 (
   m_time, roll, pitch, heading, track, vspeed, gndspeed, airspeed, latitude, longitude, altitude)
 VALUES (0.07, 2.8, 2.4, 8, 8.4, 7.3, 6.2, 5.4, 45, -84, 130);
 
 
 
select * from drone_collection;
SELECT * from drone0_rate1;
SELECT * from drone0_rate2;
SELECT * from drone1_rate1;
SELECT * from drone1_rate2;
