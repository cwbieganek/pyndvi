import arcpy
from arcpy import Parameter


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = None
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        return

class NDVI(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "NDVI from NAIP"
        self.description = "Calculates an output NDVI raster (GeoTIFF) using the input NAIP Plus (4-band) imagery."
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Input NAIP Plus raster (.jp2)
        inputRaster = Parameter(
            displayName="NAIP Plus Imagery",
            name="in_naip",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Input")

        # Input study area (Shapefile)
        studyArea = Parameter(
            displayName="Input Features",
            name="in_features",
            datatype="DEShapefile",
            parameterType="Required",
            direction="Input")

        # Output path
        studyArea = Parameter(
            displayName="Input Features",
            name="in_features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Output")

        params = None
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        return