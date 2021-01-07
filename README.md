##### Iterativer Einsatz des Projekts

Sensor Heizkreis aktivieren  
Ventiltrieb einbeziehen
Cronjob - entweder web request, oder auf scripts
Sensor Daten in Datenbank schreiben  
Regel-Logik durchlaufen: 
Ist Sensor-Temperatur > threshhold_upper-limit => steuere Ventiltrieb 1000 punkte abwärts  Ist Sensor-Temperatur < threshhold_lower-limit => steuere Ventiltrieb 1000 punkte aufwärts



### TODO mixed
* remove microsecond and milliseconds precision in all datetime fields



### Architektur Entwurf 2

#### Raspi

Regelmäßiges: Per cron oder als python dev
* Cronjob ruft die regel-applikation regelmäßig auf; zB alle 5min 
* Cronjob ruft Sensor-Abfrage regelmäßig in kurzen Abständen auf



### app architecture draft 1

* OK - daemon, lightweight, checking sensor values every 2-10 secs. Writing in DB
  

App thread, watching configurated profiles and triggering possible necessary action to handlers;


deamon thread checking for threshold lightweight.



## WEB django gui

TODO

* OK sensoren in einzelne tabellen
* aktoren table: toggles, mit grund (bedingungen von regelung: 'name')
* OK all sensor table

Graphen anzeigen; js lib? 



### Regeln, beispiele, unvollständig

* halte warmwasser auf profil winter = 40-55 grad
    profil sommer = 30-45 grad. 

* Nachtabsenkung
* meherer Modi: Low, Full, zeitgesteuert Tag/Nacht; ua.

#### regelungs-vorgänge
alle 5 min durchgehen der regeln; Oder besser nur der Regeln die gültigkeit haben im aktuellen zeitpunkt - dh. die regeln haben gültigkeits-ranges.

ständig geltendes, wie zb absolute limits für diverse temperaturen.

programmiertechnisch, könnte jede regel eine klasse sein. Alle klassen sind registriert in file bzw directory und der reihe nach wird eine bestimmte methode von ihnen ("check") ausgeführt. 


### Aktoren

* Ventiltrieb: öffnungsgrad
	DB table changes history: dtime, changelevel, changedirection, key2rule, resulting-amount

* heizungspumpe: Leistungsstufe 1...10 
* Warmwasserpumpe: An / Aus, Stufe?

### toggles, changes
writing changes of motor states to DB
properties:
- From state
- To state
- dtime
- rule


