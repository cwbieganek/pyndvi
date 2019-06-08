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
    # Description:
    #   ArcPy geoprocessing script for computing NDVI (Normalized Difference Vegetation Index)
    #   for an input study area using NAIP imagery. The script is designed to accept NAIP Plus
    #   imagery retrieved from The National Map: https://viewer.nationalmap.gov/advanced-viewer/
    #
    #   Since this script is set up as a geoprocessing tool, it must be opened in ArcGIS.

    # Inputs:
    #   NAIP Imagery
    #   Study Area
    #   Output path

    # Outputs:
    #   GeoTIFF

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
        # Retrieve individual parameters
        inputRaster = parameters[0].valueAsText # NAIP Plus raster in .jp2 format
        studyArea = parameters[1].valueAsText   # Shapefile that should include a single polygon
        outputPath = parameters[2].valueAsText  # Should include the output file name


        # Verify that studyArea has a single feature
        if int(arcpy.GetCount_management(studyArea)[0]) != 1:
            messages.addErrorMessage("{0} must have a single feature only.".format(studyArea))
            raise arcpy.ExecuteError

        # Update status window
        messages.addMessage("Clipping NAIP imagery to study area...");
        # Clip input raster to studyArea
        arcpy.Clip_analysis(inputRaster, studyArea, "in_memory/studyArea_clip");

        # Update status window
        messages.addMessage("Converting NAIP imagery to RasterLayer...");
        # Convert clipped raster into Raster instance
        clipped_naip = Raster("in_memory/studyArea_clip")

        # Turn Red band (1) into its own RasterLayer
        # Update status window
        # redBand = TODO

        # Turn NIR band (4) into its own RasterLayer
        # nirBand = TODO

        # Create new RasterLayer equal to (nirBand - redBand) / (nirBand + redBand)
        # outputRaster = TODO

        # Convert outputRaster to GeoTIFF
        # TODO

        # Save GeoTIFF at outputPath
        # TODO
        return