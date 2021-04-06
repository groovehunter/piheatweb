#!/bin/bash

LOGDIR='/home/pi/pw/log'
echo $LOGDIR

chgrp www-data $LOGDIR/debug.log

chmod g+w $LOGDIR/debug.log

chgrp www-data $LOGDIR/root.log

chmod g+w $LOGDIR/root.log

chgrp www-data $LOGDIR/piheat.log

chmod g+w $LOGDIR/piheat.log

chgrp www-data $LOGDIR/django.log

chmod g+w $LOGDIR/django.log
~                                                                                      
~                                                                                      
~                                                                                      
~                                                                                      
~                                                                                      
~                                                   
