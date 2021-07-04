# iotMW
The IoT based Microwave is built as a device to provide measured heating for industrial applications
[![GitHub issues](https://img.shields.io/github/issues/harshvs99/robotARM)](https://github.com/harshvs99/iotMW/issues)
<!-- [![GitHub forks](https://img.shields.io/github/forks/harshvs99/robotARM)](https://github.com/harshvs99/iotMW/network) -->
[![GitHub stars](https://img.shields.io/github/stars/harshvs99/robotARM)](https://github.com/harshvs99/iotMW/stargazers)
[![GitHub license](https://img.shields.io/github/license/harshvs99/robotARM)](https://github.com/harshvs99/iotMW/blob/master/LICENSE)


## Problem Statement
The project is a temperature controlled microwave, for use in bakeries etc. which rely on precise heating setups, while conventional microwaves provide only timer based heatings 

## Design
The iotMW works to provide a calibrated temperature sensor, stopping only at specified temperatures.

- Peripheral TFT and Buttons: Added using the SPI protocol using an FSM diagram for flow control
- Temperature Offsets: With rigrous testing, we calculate offsets and builds on it for sensor translation of the algorithm based on input data
