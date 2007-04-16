#**********************************************************************
# Description:
# Tests if a field exists and outputs two booleans:
#   Exists - true if the field exists, false if it doesn't exist
#   Not_Exists - true if the field doesn't exist, false if it does exist
#                (the logical NOT of the first output).
#
# Arguments:
#  0 - Table name
#  1 - Field name
#  2 - Exists (boolean - see above)
#  3 - Not_Exists (boolean - see above)
#
# Created by: ESRI
#**********************************************************************

# Standard error handling - put everything in a try/except block
#
try:

    # Import system modules
    import sys, string, os, arcgisscripting

    # Create the Geoprocessor object
    gp = arcgisscripting.create()

    # Get input arguments - table name, field name
    #
    in_Table = gp.GetParameterAsText(0)
    in_Field = gp.GetParameterAsText(1)

    # First check that the table exists
    #
    if not gp.Exists(in_Table):
        raise Exception, "Input table does not exist"

    # Use the ListFields function to return a list of fields that matches
    #  the name of in_Field. This is a wildcard match. Since in_Field is an
    #  exact string (no wildcards like "*"), only one field should be returned,
    #  exactly matching the input field name.
    #
    fields = gp.ListFields(in_Table, in_Field)

    # If ListFields returned anything, the Next operator will fetch the
    #  field. We can use this as a Boolean condition.
    #
    field_found = fields.Next()

    # Branch depending on whether field found or not. Issue a
    #  message, and then set our two output variables accordingly
    #
    if field_found:
        gp.AddMessage("Field %s found in %s" % (in_Field, in_Table))
        gp.SetParameterAsText(2, "True")
        gp.SetParameterAsText(3, "False")
    else:
        gp.AddMessage("Field %s not found in %s" % (in_Field, in_Table))
        gp.SetParameterAsText(2, "False")
        gp.SetParameterAsText(3, "True")


# Handle script errors
#
except Exception, errMsg:

    # If we have messages of severity error (2), we assume a GP tool raised it,
    #  so we'll output that.  Otherwise, we assume we raised the error and the
    #  information is in errMsg.
    #
    if gp.GetMessages(2):   
        gp.AddError(GP.GetMessages(2))
    else:
        gp.AddError(str(errMsg))      