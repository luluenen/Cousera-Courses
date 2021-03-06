## RTT Measurements

TODO: Project description

### Requirements

* Python 3.4+
* [Ripe Atlas Cousteau](https://github.com/RIPE-NCC/ripe-atlas-cousteau), latest version.
* 

### Installation

.....
2. Run: `src/setup.sh`

### Usage

#### Measurement Creation

##### Input Data
* CSV file with the probes to measure, `input_data/probes.csv`. With the following format:

    | Prb_id | Atlas_id |\_IPv4\_|
    |--------|----------|--------|
    | 0      | ...      | ...    |
    | 1      | ...      | ...    |
    | ...    | ...      | ...    |

* Parameters: JSON file, `input_data/measure_parameters.json`, with the following keys:

    | Parameter       | Description                                                                        |Default value|
    |-----------------|------------------------------------------------------------------------------------|-------------|
    | `measure_type`  | Type of the measurement. "rtt" for Atlas' Ping. (Currently only implemented)       | rtt         |
    | *`key`*         | Atlas' API key for creating measurements. *Mandatory*.                             | -           |
    | `nb_probes`     | Number of probes in the overlay network to analyse.                                | 2           |
    | `random`        | "True" if loading `nb_probes` random probes from the CSV Probes file.              | False       |
    | `start` (\*)    | Time when the measurement will start running.                                      | -           |
    | `end` (\*)      | Time when the measurement will stop running.                                       | -           |
    | `interval`      | Time (in seconds) between each measurement epoch. (Only for periodic measurements).| 60          |
    |`packet_interval`| Time (in milliseconds) between each packet within a measurement epoch.             | 1000        |
    | `af`            | Network address family.                                                            | 4           |
    | `packets`       | Only valid with "rtt" as `measure_type`. Number of ICMP packets sent to ping the destination on each measurement epoch.|1|
   
    ###### Notes:
    
       - (\*) Date-Time format: ISO RFC 3339 always in UTC, so without the *Z* suffix (`%Y-%m-%dT%H:%M:%S.%f`)
       - If `start` and `end` times are not present or with a wrong format, it will be assumed as a *one-off* measurement.
       - It is highly recommended that the `start` time of the measurement be a few minutes in the future, and not in the current time.
       - Measurements cannot span fewer than 5 minutes. (Time between `start` and `end` times MUST be higher than 5 minutes).

##### Execution
Run with Python3.4 (or higher): `src/measuresOverlay.py`

- Help: `-h, --help`
- Optional parameters:
    `--probes`: Complete path to CSV file of probes for the measurement. 
                Default: `input_data/probes.csv`
                
    `--params`: Complete path to JSON file to load the parameters of the measurement. 
                Default: `input_data/measure_parameters.json`

##### Output Data
Output files are generated inside `/output_data/`, in a folder named with the current (local) time.
                    
* JSON file, `input_parameters.json`, with the actual parameters used to create the measurements (including defaults). 

* Measurement file, `measurement.csv`, where the first line is a JSON list with information of the probes used, and the second line is a list of the measurements IDs generated.
    
#### Retrieving Results

##### Input Data
Measurements (`measurement.csv`) file generated by `measuresOverlay.py`.
The first line of this file is a JSON list with the probes used (each probe being a dictionary with ID, Altas Probe ID and IP Address.
The second line is a list of the measurements IDs generated.
    

##### Execution
Run with Python3.4 (or higher): `src/results.py`

- Help: `-h, --help`
- Required parameter:
    `file`: File of measurement execution generated by `measuresOverlay.py` with the probes and the measurements IDs.

##### Output Data
Results of the measurements in the CSV file `output.csv`, inside a folder named with the creation (local) time.
This file contains one symmetric matrix below another, one for each measurement epoch. It has the following format:

| Probes | 0   | 1   | 2  | ... |
|--------|-----|-----|----|-----|
| 0      | 0   | x   | y  | ... |
| 1      | x   | 0   | z  | ... |
| 2      | y   | z   | 0  | ... |
| ...    | ... | ... | ...| ... |
