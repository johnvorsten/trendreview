
## About data
The data directory contains (2) files: DD03.csv and DD64.csv. 
Each of these files contain trended data from dual duct terminal units. Each of these terminal units have a specific configuration, and each of the trend files has certain trended objects related to each dual duct terminal unit.
Based on the headers we know which child objects each terminal unit has. For this documentation, they are listed below.
For DD03
['Date', 'Time', 'DischargeTemperature', 'CoolingDamperCommand', 'CooingDamperPosition', 'CoolingAirVolume', 'CoolingSetpoint', 'ControlTemperature', 'ScheduleMode', 'OccupancyMode', 'HeatCoolMode', 'HeatingDamperCommand', 'HeatingDamperPosition', 'HeatingAirVolume', 'RMSTPTDIAL', 'RoomTemperature', 'STPTDIAL', 'AirflowSetpoint']
For DD64
All of the same headers are available', 'except the header data ['RMSTPTDIAL', 'RoomTemperature', 'STPTDIAL'] do not contain any data

Note that the column headers in CapitalCamelCase are officially recognized by this app.  I'll have to find a place with a list of all officially recognized headers/objects for each type of equipment...

## Common data types
Date: Must be date format
Time: Must be string like HH:MM
ScheduleMode: Must be integer one of [1,2,3,4]
OccupancyMode: Must be boolean integer [1,0]. 1 for True/occupide mode, 0 for False/unoccupied mode
HeatCoolMode: string one of ['heat','cool']