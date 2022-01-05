
## About data
The data directory contains (2) files: DD03.csv and DD64.csv. 
Each of these files contain trended data from dual duct terminal units. Each of these terminal units have a specific configuration, and each of the trend files has certain trended objects related to each dual duct terminal unit.
Based on the headers we know which child objects each terminal unit has. For this documentation, they are listed below.
For DD03
['DateTime', 'DischargeTemperature', 'CoolingDamperCommand', 'CoolingDamperPosition', 'CoolingAirVolume', 'CoolingSetpoint', 'ControlTemperature', 'ScheduleMode', 'OccupancyMode', 'HeatCoolMode', 'HeatingDamperCommand', 'HeatingDamperPosition', 'HeatingAirVolume', 'RMSTPTDIAL', 'RoomTemperature', 'STPTDIAL', 'AirflowSetpoint']
For DD64
All of the same headers are available', 'except the header data ['RMSTPTDIAL', 'RoomTemperature', 'STPTDIAL'] do not contain any data

Note that the column headers in CapitalCamelCase are officially recognized by this app.  I'll have to find a place with a list of all officially recognized headers/objects for each type of equipment...

## Dual-Duct VAV input data types
If you do not follow these data sanitation rules, then you may encounter an error.

DateTime: (string) Must be [ISO 8061 time format](https://www.iso.org/iso-8601-date-and-time-format.html). ISO 8061 is a date and time string-formatting scheme. Format your timestamps like `YYYY-mm-ddTHH:MM:SS`. For example, `2021-12-29T16:31:21` is year 2021, December 29th 4:31 PM and 21 seconds. Notice that the hour format is zero padded and 24-hour. Make sure to zero-pad all of your months, days, hours, and minutes. If you are using excel, consider using formulas like =TEXT(A2, 'yyyy-mm-ddTHH:MM:SS') if your dates are stored in a serial number date format.  
ScheduleMode: (integer) Must be integer one of [1,0]. '1' indicates scheduled occupancy, and '0' indicates schedule unoccpuancy. This software does not make a distinction between modes like warmup/precomfort/cooldown/protection
OccupancyMode: (integer) Must be boolean integer [1,0]. 1 for True/occupide mode, 0 for False/unoccupied mode
HeatCoolMode: (string) string one of ['HEAT','COOL']
HeatingDamperCommand: (numeric) data type, ranging from 0-100. Percentage inputs might not be supported
HeatingDamperPosition: (numeric) data type, ranging from 0-100. Percentage inputs might not be supported
HeatingAirVolume[ft^3/min]: (numeric) measured/calculated air volume from hot duct
RoomTemperature[degrees Fahrenehit]: (numeric) measured room temperature
AirflowSetpoint[ft^3/min]: (numeric) Current airflow setpoint
CoolingSetpoint[degrees Fahrenehit]: (numeric) 
ControlTemperature[degrees Fahrenehit]: (numeric) The value used to calculate the current control temperature / setpoint. Don't be confused by the CoolingSetpoint or HeatingSetpoint headers. This should be the actual value used to control to (the value being compared to the process variable to calculate error).
DischargeTemperature[degrees Fahrenehit]: (numeric) measured discharge air temperature
CoolingDamperCommand: (numeric) data type, ranging from 0-100. Percentage inputs might not be supported
CoolingDamperPosition: (numeric) data type, ranging from 0-100. Percentage inputs might not be supported

## Testing
from project root (trendreview) at the terminal: `python -m unittest discover tests "test_*.py"`
