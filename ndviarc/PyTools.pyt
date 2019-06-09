import arcpy
from arcpy import Parameter, Raster
import numpy

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [NDVI]


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
    #   Raster dataset

    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "NDVI from NAIP"
        self.description = "Calculates an output NDVI raster (GeoTIFF) using the input NAIP Plus (4-band) imagery."
        self.canRunInBackground = True

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
            displayName="Study Area",
            name="in_study_area",
            datatype="DEShapefile",
            parameterType="Required",
            direction="Input")

        # Output path
        outputPath = Parameter(
            displayName="Output Path",
            name="out_path",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Output")

        params = [inputRaster, studyArea, outputPath]
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

    def compareCoordinateSystems(self, s1, s2):
        # Describe s1
        s1Describe = arcpy.Describe(s1)
        # Describe s2
        s2Describe = arcpy.Describe(s2)
        print "s1 spatial reference: " + s1Describe.spatialReference.name
        print "s2 spatial reference: " + s2Describe.spatialReference.name
        return s1Describe.spatialReference.name == s2Describe.spatialReference.name

    def execute(self, parameters, messages):
        # Retrieve individual parameters
        inputRaster = parameters[0].valueAsText # NAIP Plus raster in .jp2 format
        studyArea = parameters[1].valueAsText   # Shapefile that should include a single polygon
        outputPath = parameters[2].valueAsText  # Should include the output file name

        # Log outputPath
        messages.addMessage("Result will be located at {0}".format(outputPath))

        # Verify that input raster and study area have the same coordinate system
        coordinateSystemsMatch = self.compareCoordinateSystems(inputRaster, studyArea)
        if coordinateSystemsMatch:
            messages.addMessage("Coordinate systems for inputs are the same.")
        else:
            messages.addMessage("Coordinate systems for inputs are NOT the same.")
            raise arcpy.ExecuteError

        # Verify that studyArea has a single feature
        if int(arcpy.GetCount_management(studyArea)[0]) != 1:
            messages.addErrorMessage("{0} must have a single feature only.".format(studyArea))
            raise arcpy.ExecuteError

        # Update status window
        messages.addMessage("Getting extent of study area...")
        # Describe the input raster
        inputRasterDescription = arcpy.Describe(inputRaster)
        # Describe the input studyArea
        studyAreaDescription = arcpy.Describe(studyArea)
        studyAreaExtent = studyAreaDescription.Extent
        # Update environment variables
        arcpy.env.outputCoordinateSystem = inputRasterDescription.spatialReference
        arcpy.env.snapRaster = inputRaster

        # Get extent variables
        xMin = studyAreaExtent.XMin
        yMin = studyAreaExtent.YMin
        xMax = studyAreaExtent.XMax
        yMax = studyAreaExtent.YMax

        # Generate rectangle string argument for Clip_management
        rectangleString = str(xMin) + " " + str(yMin) + " " + str(xMax) + " " + str(yMax)

        # Update status window
        messages.addMessage("Clipping NAIP imagery to study area...")
        # Clip input raster to studyArea
        # arcpy.Clip_management(inputRaster, rectangleString, outputPath, "#", "#", "NONE", "NO_MAINTAIN_EXTENT")
        arcpy.Clip_management(inputRaster, rectangleString, "in_memory/studyArea_clip", "#", "#", "NONE", "NO_MAINTAIN_EXTENT")

        # Update status window
        messages.addMessage("Converting NAIP imagery to RasterLayer...")
        # Convert clipped raster into Raster instance
        clipped_naip = Raster("in_memory/studyArea_clip")

        # Update status window
        messages.addMessage("Creating raster layer from Red Band...")
        # Turn Red band (1) into its own RasterLayer
        arcpy.MakeRasterLayer_management("in_memory/studyArea_clip", "redBandLayer", "", "", 1)
        redBandNumPy = arcpy.RasterToNumPyArray("redBandLayer")

        # Update status window
        messages.addMessage("Creating raster layer from NIR Band...")
        # Turn NIR band (4) into its own RasterLayer
        arcpy.MakeRasterLayer_management("in_memory/studyArea_clip", "nirBandLayer", "", "", 4)
        nirBandNumPy = arcpy.RasterToNumPyArray("nirBandLayer")

        # Create new numpy array equal to (nirBand - redBand) / (nirBand + redBand)
        ndviNumPy = numpy.divide((numpy.subtract(nirBandNumPy, redBandNumPy)), (numpy.add(nirBandNumPy, redBandNumPy)))
        ndviNumPy = numpy.multiply(ndviNumPy, 100)
        ndviNumPy = numpy.around(ndviNumPy)
        # Log numpy array for testing purposes
        messages.addMessage(ndviNumPy)

        # Convert numpy array to Raster
        outputRaster = arcpy.NumPyArrayToRaster(ndviNumPy)

        # Update status window
        messages.addMessage("Saving result...")
        # Save outputRaster
        outputRaster.save(outputPath)

        # Delete intermediate data
        arcpy.Delete_management("in_memory/studyArea_clip")

        return