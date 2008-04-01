## Script Name: Clip Multiple Featureclasses
## Description: Clips one or more shapefiles
## from a folder and palces the clipped
## feature classes into a Geodatabase.
## Created by: Peter Caballero
## Date: 10/20/04

#import lib.path_configuration
# Import standard library modules
import win32com.client, sys, os

# Create the Geoprocessor object
GP = win32com.client.Dispatch("esriGeogprocessing.GPDispatch.1")

# Set the input workspace
GP.workspace = sys.argv[1]

# Set the clip featureclass
clipFeatures = sys.argv[2]

# Set the output workspace
outWorkspace = sys.argv[3]

# Set the cluster tolerance
clusterTolerance= sys.argv[4]

try:
    # Get a list of the featureclasses in the input folder
    fcs = GP.ListFeatureClasses()
    # Loop through the list of feature classes
    fcs.Reset()
    fc = fcs.Next()



    while fc:
        # Validate the new feature class name for the output workspace.
        outFeatureClass = outWorkspace + "/" + GP.ValidateTableName(fc,
                                                                outWorkSpace)
        # Clip each feature class in the list with the clip feature class.
        # Do not clip the clipfeatures, it may be int the same workspace.
        if str(fc) != str(os.path.split(clipFeatures)[1]):
            GP.Clip(fc, clipFeatures, outFeatureClass, clusterTolerance)
        fc = fcs.Next()
except:
    GP.AddMessage(GP.GetMessages(2))
    print GP.GetMessages(2)
  
            



                                                            
    
                                                

