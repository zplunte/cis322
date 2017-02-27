#!/usr/bin/bash
# A bash script for initializing the LOST db in the OSNAP env 

# Initialize the database under $HOME
initdb -D $HOME/data

# Start running database server, create logfile
pg_ctl -D $HOME/data -l logfile start
