# Description:
# 	ArcPy geoprocessing script for computing NDVI (Normalized Difference Vegetation Index)
#	for an input study area using NAIP imagery. The script is designed to accept NAIP Plus
# 	imagery retrieved from The National Map: https://viewer.nationalmap.gov/advanced-viewer/
#
# 	Since this script is set up as a geoprocessing tool, it must be opened in ArcGIS.

# Inputs:
# 	NAIP Imagery
#	Study Area
# 	Output path

# Outputs:
# 	GeoTIFF

# Import modules
import arcpy
from arcpy import env

# Get path to input .jp2
# Set parameter description
inputRaster = arcpy.GetParameterAsText(0)

# Get path to input study area
# Set parameter description
studyArea = arcpy.GetParameterAsText(1)

# Get output path
outputPath = arcpy.GetParameterAsText(2)

# Clip input raster to studyArea
# Update status window
# TODO

# Convert clipped raster into RasterLayer
# Update status window
# TODO

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