#!/usr/bin/env python3
from __future__ import absolute_import, unicode_literals
import re
import octoprint.plugin
import octoprint.filemanager
import octoprint.filemanager.util

class GSkewer(octoprint.filemanager.util.LineProcessorStream):
    def __init__(self, input_stream, xytan, yztan, zxtan):
        super().__init__(input_stream)

        self.xytan = xytan
        self.yztan = yztan
        self.zxtan = zxtan

        if not zxtan == 0:
            print('The ZX error is set to', zxtan, 'degrees')

        if xytan == 0.0 and yztan == 0.0 and zxtan == 0.0:
            print('No skew parameters provided. Nothing will be done.')

        self.xin = 0.0
        self.yin = 0.0
        self.zin = 0.0
        #filename = args.file

        #outname = re.sub(r'.gcode', '-skewed.gcode', filename)

        #if os.path.isfile(outname):
        #os.remove(outname)

        #outfile = open(outname, 'a')


    def process_line(self, encoded):
        line = encoded.decode("utf-8")

        comment = None
        parts = line.split(";", 1)
        if len(parts) == 2:
          line, comment = parts

        gmatch = re.match(r'G[0-1]', line, re.I)
        if gmatch:
            # print('line was a G0/G1 command!', line)

            # load the incoming X coordinate into a variable. Previous value will be used if new value is not found.
            xsrch = re.search(r'[xX]-?\d*\.*\d*', line, re.I)
            if xsrch:  # if an X value is found
                # Strip the letter from the coordinate.
                self.xin = float(re.sub(r'[xX]', '', xsrch.group()))

            # load the incoming Y coordinate into a variable. Previous value will be used if new value is not found.
            ysrch = re.search(r'[yY]-?\d*\.*\d*', line, re.I)
            if ysrch:
                # Strip the letter from the coordinate.
                self.yin = float(re.sub(r'[yY]', '', ysrch.group()))

            # load the incoming Z coordinate into a variable. Previous value will be used if new value is not found.
            zsrch = re.search(r'[zZ]-?\d*\.*\d*', line, re.I)
            if zsrch:
                # Strip the letter from the coordinate.
                self.zin = float(re.sub(r'[zZ]', '', zsrch.group()))

            # calculate the corrected/skewed XYZ coordinates
            xout = round(self.xin - self.yin * self.xytan, 3)
            yout = round(self.yin - self.zin * self.yztan, 3)
            xout = round(xout - self.zin * self.zxtan, 3)
            # Z coodinates must remain the same to prevent layers being tilted!
            zout = self.zin

            lineout = line
            #print('old line:', lineout)

            if xsrch:
                lineout = re.sub(r'[xX]-?\d*\.*\d*', 'X' + str(xout), lineout)

            if ysrch:
                lineout = re.sub(r'[yY]-?\d*\.*\d*', 'Y' + str(yout), lineout)

            if zsrch:
                lineout = re.sub(r'[zZ]-?\d*\.*\d*', 'Z' + str(zout), lineout)

            if comment != None:
                lineout = lineout + ";" + comment

            #print('new line: ', lineout)
            return lineout.encode("utf-8")
        else:
            #print('Skipping, not a movement.', line)
            return encoded

class GSkewerPlugin(octoprint.plugin.TemplatePlugin,
                    octoprint.plugin.SettingsPlugin):
    def skew_gcode(self, path, file_object, links=None, printer_profile=None, allow_overwrite=True, *args, **kwargs):
        if not octoprint.filemanager.valid_file_type(path, type="gcode"):
            return file_object

        #import os
        #name, _ = os.path.splitext(file_object.filename)
        #if not name.endswith("_skew"):
        #    return file_object

        xytan = self._settings.get_float(["xytan"])
        yztan = self._settings.get_float(["yztan"])
        xztan = self._settings.get_float(["xztan"])
        
        self._logger.info("Applying skew compensation...")

        return octoprint.filemanager.util.StreamWrapper(file_object.filename, GSkewer(file_object.stream(), xytan, yztan, xztan))

    def get_settings_defaults(self):
        return dict(xytan=0.0, yztan=0.0, xztan=0.0)

    def get_template_configs(self):
        return [dict(type="settings", custom_bindings=False)]

__plugin_pythoncompat__ = ">=3.7,<4"

def __plugin_load__():
    plugin = GSkewerPlugin()

    global __plugin_implementation__
    __plugin_implementation__ = plugin

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.filemanager.preprocessor": plugin.skew_gcode
    }

