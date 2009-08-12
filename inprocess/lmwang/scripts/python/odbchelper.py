def buildConnectionString(params):
    """Build a connection string from a dictionary of parameters.

    Retruns String."""
    return ";".join(["%s=%s" % (k,v) for k,v in params.items()])

if __name__ == "__main__":
    myParams = {"server":"trondheim",\
                "database":"testdb",\
                "uid":"urbansim",\
                "pwd":"xxx"\
                }
    print buildConnectionString(myParams)
    
                
