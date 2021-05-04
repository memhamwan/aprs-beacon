# APRS Beacon

A script that is dockerized to beacon objects into APRS from time to time. This can be run directly from the repo or as a docker image `memhamwan/aprs-beacon:latest`.

This script was originally written by KD7LXL and published to the HamWAN repo [here](https://github.com/HamWAN/hamwan_scripts/tree/master/aprsobject). It has been updated to suit MemHamWAN's use cases, which are slightly different due to infrastructure differences.

## Usage

Create a file `config/settings.yml` that has your pertinent settings. Refer to the in-repo file as an example. If using the docker image, be sure it is mounted at the absolute path `/usr/src/app/config/settings.yml`.

### Definitions

Latitue and longitude in APRS are formatted a bit oddly. Latitude is `HHMM.MM`, but longitude is `HHHMM.MM`, both as strings. Zero padding must be observed, otherwise the ARPS servers will simply discard the invalid packet.
