
# This is not a python file but just a way to 
# save this command line command

# This creates a geometry type table in the Chromium
# database. 
ogr2ogr -f "MSSQLSpatial" "MSSQL:server=ALBUGIERKE\ALBUGIERKE;database=Chromium;trusted_connection=yes;" "Watersheds- Revised.shp" -lco "GEOM_TYPE=geography" -lco "GEOM_NAME=geog4326" -nln "Watersheds" -progress