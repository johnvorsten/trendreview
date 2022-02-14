
# Purpose
This software was created to simply trend review of certain classes of HVAC equipment, following ASHRAE guideline 36 'High Performance Sequence of Operations for HVAC Systems'

## Installation
Run `pip3 install trendreview`

## Usage example
See usage instrucitons:
`~:# python trendreview.py --help`
```bash
usage: trendreview.py [-h] --filepath FILEPATH --type {ddvav}
                      [--report-path LOG_FILEPATH]

Fault Diagnostics and Detection for trend review of mechanical equipment

optional arguments:
  -h, --help            show this help message and exit
  --filepath FILEPATH   file path to trended data in CSV format
  --type {ddvav}        Type of mechanical equipment being trended. Must be
                        one of ['ddvav']
  --report-path LOG_FILEPATH
                        Filename to save report, like c:/path/to/report.txt
```
Generate a report:</br>
`~:# python trendreview.py --filepath ./data/DD03.csv --type ddvav --report-path "C:/users/jvorsten/downloads/report.txt"`

Contents of report:</br>
```txt
Issue #1
Airflow measured while damper is closed:
The maximum allowed consecutive instances (3) was exceeded starting at data indices [18, 37]
See figure1.png


Issue #2
Cooling damper stuck open: [...]
```

Sample images:</br>
![Figure1](./figure1.png)
![Figure2](./figure2.png)

Graph all data:</br>
```cmd
`~:# python trendreview.py --filepath ./data/DD03.csv --type GraphAll --report-path "C:/users/jvorsten/downloads/report.txt"`
```

# Dual duct VAV

## Required headers
The only required header columns are:

[DateTime, DischargeTemperature, CoolingDamperCommand, CoolingDamperPosition, CoolingAirVolume, CoolingSetpoint, ControlTemperature, ScheduleMode, OccupancyMode, HeatCoolMode, HeatingDamperCommand, HeatingDamperPosition, HeatingAirVolume, RoomTemperature, AirflowSetpoint]

See the next sections for formatting and type instructions

## Dual-Duct VAV input data types
If you do not follow these data sanitation rules, then you may encounter an error.

* DateTime: (string) Must be [ISO 8061 time format](https://www.iso.org/iso-8601-date-and-time-format.html). ISO 8061 is a date and time string-formatting scheme. Format your timestamps like `YYYY-mm-ddTHH:MM:SS`. For example, `2021-12-29T16:31:21` is year 2021, December 29th 4:31 PM and 21 seconds. Notice that the hour format is zero padded and 24-hour. Make sure to zero-pad all of your months, days, hours, and minutes. If you are using excel, consider using formulas like =TEXT(A2, 'yyyy-mm-ddTHH:MM:SS') if your dates are stored in a serial number date format.

* ScheduleMode: (integer) Must be integer one of [1,0]. '1' indicates scheduled occupancy, and '0' indicates schedule unoccpuancy. This software does not make a distinction between modes like warmup/precomfort/cooldown/protection
* OccupancyMode: (integer) Must be boolean integer [1,0]. 1 for True/occupide mode, 0 for False/unoccupied mode
* HeatCoolMode: (string) string one of ['HEAT','COOL']
* HeatingDamperCommand: (numeric) data type, ranging from 0-100. Percentage inputs might not be supported
* HeatingDamperPosition: (numeric) data type, ranging from 0-100. Percentage inputs might not be supported
* HeatingAirVolume[ft^3/min]: (numeric) measured/calculated air volume from hot duct
* RoomTemperature[degrees Fahrenehit]: (numeric) measured room temperature
* AirflowSetpoint[ft^3/min]: (numeric) Current airflow setpoint
* CoolingSetpoint[degrees Fahrenehit]: (numeric) 
* ControlTemperature[degrees Fahrenehit]: (numeric) The value used to calculate the current control temperature / setpoint. Don't be confused by the CoolingSetpoint or HeatingSetpoint headers. This should be the actual value used to control to (the value being compared to the process variable to calculate error).
* DischargeTemperature[degrees Fahrenehit]: (numeric) measured discharge air temperature
* CoolingDamperCommand: (numeric) data type, ranging from 0-100. Percentage inputs might not be supported
* CoolingDamperPosition: (numeric) data type, ranging from 0-100. Percentage inputs might not be supported


## About data
The data directory contains (2) files: DD03.csv and DD64.csv.

Each of these files contain trended data from dual duct terminal units. Each of these terminal units have a specific configuration, and each of the trend files has certain trended objects related to each dual duct terminal unit.

Based on the headers we know which child objects each terminal unit has. For this documentation, they are listed below.

For DD03
* ['DateTime', 'DischargeTemperature', 'CoolingDamperCommand', 'CoolingDamperPosition', 'CoolingAirVolume', 'CoolingSetpoint', 'ControlTemperature', 'ScheduleMode', 'OccupancyMode', 'HeatCoolMode', 'HeatingDamperCommand', 'HeatingDamperPosition', 'HeatingAirVolume', 'RMSTPTDIAL', 'RoomTemperature', 'STPTDIAL', 'AirflowSetpoint']

For DD64
* All of the same headers are available', 'except the header data ['RMSTPTDIAL', 'RoomTemperature', 'STPTDIAL'] do not contain any data

Note that the column headers in CapitalCamelCase are officially recognized by this app.  I'll have to find a place with a list of all officially recognized headers/objects for each type of equipment...

# Air hander VAV

## Required headers

## AHU Input types
DateTime
SupplyAirTemperature
SupplyAirTemperatureSetpoint
MixedAirTemperature
ReturnAirTemperature
OutdoorAirTemperature
DuctStaticPressure
DuctStaticPressureSetpoint
HeatingCoilCommand
CoolingCoilCommand
FanSpeedCommand
CoolingCoilEnteringTemperature
CoolingCoilLeavingTemperature
HeatingCoilEnteringTemperature
HeatingCoilLeavingTemperature

Modes of operation:
Heating
Free cooling + modultaing OA damper
Mechanical + economizer cooling
Mechanical cooling + minimum OA damper
Other / dehumidifcation

Fault detection rules:
Duct static pressure too low with fan at full speed
MAT too low; should be between OAT and RAT
MAT too high; should be between OAT and RAT
Too many changes in OS
SAT too low; should be higher than MAT
OA fraction too low or too high; should equal %OAmin
SAT too low in full heating 
OAT too high for free cooling without additional mechanical cooling
OAT and MAT should be approximately equal 
OAT too low for 100% OA cooling
SAT too high; should be less than MAT
SAT too high in full cooling 
Temperature drop across inactive cooling coil
Temperature rise across inactive heating coil

# Testing
from project root (trendreview) at the terminal: `python -m unittest discover tests "test_*.py"`