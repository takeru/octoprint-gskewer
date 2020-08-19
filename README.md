# About Gskewer
This is the OctoPrint plugin version of Gskewer; a tool to skew transform gcode file coordinates to account for axis misalignment of a 3D printer.

In order to use Gskewer you will need to print a test cube, take accurate measurements of the cube, then input those measurements into the Gskewer settings page of OctoPrint. 

The G-code file to be modified, the measured error (in mm), and the distance from zero where the measurement was taken is then entered into skew.py before being run.


# Preparing to use Gskewer
The task of measuring the error between axis pairs is shown in good detail at http://www.zs1jen.org/Station_Manuals/Reference/3D_Printers/14_RepRapPro_-_Axis_compensation.pdf

The files to be printed for the above process are at https://github.com/reprappro/RepRapFirmware/blob/master/STL/calibration_90mm.stl

The general idea of the measurements required and which arguments they correspond to is illustrated below.

![MechanizedMedic](https://github.com/MechanizedMedic/gskewer/raw/master/gskewer_measuring1.png "Positive skew error.")
![MechanizedMedic](https://github.com/MechanizedMedic/gskewer/raw/master/gskewer_measuring2.png "Negative skew error.")

These measurements are to be taken for each of the three axis pairs of the cube: XY, YZ, and ZX.

You will end up with six measurements/arguments: xylen, xyerr, yzlen, yzerr, zxlen, and zxerr.

The initial six measurements can be simplified to a tangent argument by dividing the error by length. (ie: xyerr/xylen=xytan) The three tangent arguments are: xytan, yztan, and zxtan.

# Installing Gskewer

OctoPrint Gskewer can currently only be installed manually using this URL:

    https://github.com/Kranex/octoprint-gskewer/archive/master.zip

TODO: Properly explain installation steps and get Gskewer listed in the OctoPrint plugin repo.

# Using Gskewer

Gskewer will automatically replace uploaded or generated Gcode with a skewed version using the settings provided in the OctoPrint settings menu. Changing the settings will not correct previously uploaded or generated Gcode, the original unskewed versions of these files will need to be uploaded again to be skewed.

Currently only `xytan`, `xztan` and `yztan` can be set in the settings menu. These are easly calculated using the above instructions. In the future I may implement a more convenient method of fine tuning the skew parameters however for now this appears to works just fine.
