#!/bin/bash

# pins for actors set to OUT
gpio mode 24 out
gpio mode 21 out

# enable heat pump
gpio write 24 1
