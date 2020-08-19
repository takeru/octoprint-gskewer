#!/usr/bin/env python3
import re
import octoprint.plugin
import octoprint.filemanager
import octoprint.filemanager.util

class gskewer(octoprint.filemanager.util.LineProcessorStream):
    def __init__(self, input_stream, xytan, yztan, zxtan):
        super(input_stream)
        
        self.xytan = xytan
        self.yztan = yztan
        self.zxtan = zxtan
        
        if not zxtan == 0:
        print('The ZX error is set to', zxtan, 'degrees')

        if xytan == 0.0 and yztan == 0.0 and zxtan == 0.0:
            print('No skew parameters provided. Nothing will be done.')

        filename = args.file

        outname = re.sub(r'.gcode', '-skewed.gcode', filename)

        xin = 0.0
        yin = 0.0
        zin = 0.0
        
        #if os.path.isfile(outname):
        #os.remove(outname)

        #outfile = open(outname, 'a')
        
        
    def process_line(self, line):
        gmatch = re.match(r'G[0-1]', line, re.I)
        if gmatch:
            print('line was a G0/G1 command!')

            # load the incoming X coordinate into a variable. Previous value will be used if new value is not found.
            xsrch = re.search(r'[xX]\d*\.*\d*', line, re.I)
            if xsrch:  # if an X value is found
                # Strip the letter from the coordinate.
                xin = float(re.sub(r'[xX]', '', xsrch.group()))

            # load the incoming Y coordinate into a variable. Previous value will be used if new value is not found.
            ysrch = re.search(r'[yY]\d*\.*\d*', line, re.I)
            if ysrch:
                # Strip the letter from the coordinate.
                yin = float(re.sub(r'[yY]', '', ysrch.group()))

            # load the incoming Z coordinate into a variable. Previous value will be used if new value is not found.
            zsrch = re.search(r'[zZ]\d*\.*\d*', line, re.I)
            if zsrch:
                # Strip the letter from the coordinate.
                zin = float(re.sub(r'[zZ]', '', zsrch.group()))

            # calculate the corrected/skewed XYZ coordinates
            xout = round(xin - yin * xytan, 3)
            yout = round(yin - zin * yztan, 3)
            xout = round(xout - zin * zxtan, 3)
            # Z coodinates must remain the same to prevent layers being tilted!
            zout = zin

            lineout = line
            print('old line:', lineout)

            if xsrch:
                lineout = re.sub(r'[xX]\d*\.*\d*', 'X' + str(xout), lineout)

            if ysrch:
                lineout = re.sub(r'[yY]\d*\.*\d*', 'Y' + str(yout), lineout)

            if zsrch:
                lineout = re.sub(r'[zZ]\d*\.*\d*', 'Z' + str(zout), lineout)

            print('new line: ', lineout)
            return lineout
        else:
            print('Skipping, not a movement.', line)
            return line
        
class GSkewerPlugin(octoprint.plugin.OctoPrintPlugin):
    def skew_gcode(path, file_object, links=None, printer_profile=None, allow_overwrite=True, *args, **kwargs):
        if not octoprint.filemanager.valid_file_type(path, type="gcode"):
            return file_object

        #import os
        #name, _ = os.path.splitext(file_object.filename)
        #if not name.endswith("_skew"):
        #    return file_object

        return octoprint.filemanager.util.StreamWrapper(file.object.filename, GSkewer(file_object.stream(), 0, 0, 0))

__plugin_name__ = "gskewer"
__plugin_description__ = "Skews G0 and G1 commands to correct for error in each axis. Does not skew G2 or G3, so use on such gcode at your own risk."
__plugin_pythoncompat__ = ">=3.7, <4"

def __plugin_load__():
    plugin = GSkewerPlugin()
    
    global __plugin_implementation__
    __plugin_implementation__ = plugin
    
    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.filemanager.preprocessor": skew_gcode
    }

