### inner join von cntrl_controlevent mit allen sensordatas

´´´
select s1.temperature, s2.temperature, cntrl_controlevent.dtime from sensors_sensordata_01 as s1, sensors_sensordata_02 as s2 inner join cntrl_controlevent on cntrl_controlevent.id where s1.ctrl_event_id=cntrl_controlevent.id and s2.ctrl_event_id=cntrl_controlevent.id;

select s1.temperature, s2.temperature, s3.temperature, s4.temperature, cntrl_controlevent.dtime from sensors_sensordata_01 as s1, sensors_sensordata_02 as s2, sensors_sensordata_03 as s3, sensors_sensordata_04 as s4 inner join cntrl_controlevent on cntrl_controlevent.id where s1.ctrl_event_id=cntrl_controlevent.id and s2.ctrl_event_id=cntrl_controlevent.id and s3.ctrl_event_id=cntrl_controlevent.id and s4.ctrl_event_id=cntrl_controlevent.id;


select s1.temperature, cntrl_controlevent.dtime from sensors_sensordata_01 as s1 inner join cntrl_controlevent on cntrl_controlevent.id=s1.ctrl_event_id;

```
