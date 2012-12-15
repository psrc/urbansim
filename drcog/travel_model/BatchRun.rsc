
Macro "Init" (args)
	// path, Options, year
    Shared path, Options, year
    dim path[14]                      // path of the master network directories and the scenario directory

	//path[1] = "C:\\Projects\\Ompo\\Conversion\\Application\\"
	//path[2] = ChooseDirectory("Choose a Model Directory", ) //scenarioDirectory
	path[2] = args.scenarioDirectory
	path[2] = path[2] + "\\"

	path[3] = args.genericDirectory
	path[3] = path[3] + "\\"
	
    // path of the master network directories and the scenario directory
	if path[3] <> "" then do
		path[4] = path[3] + "inputs\\master_network\\"
		path[5] = path[3] + "inputs\\turn penalties\\"
		path[6] = path[3] + "inputs\\other\\"
		//path[7] = path[3] + "inputs\\taz\\"
		path[7] = args.exchangeDirectory + "\\"  //excel spreadsheet 'y[year]tazdata.xls'
		path[8] = path[3] + "controls\\"
		path[9] = path[3] + "programs\\"
		path[10] =path[3] + "temp\\"
		path[11] =path[3] + "scripts\\"
	end
	
	year  = args.year
	
endMacro	

Macro "BatchRun" (args)
    RunMacro("Init", args)
	
    //this is to be used as an interface between transcad and urbansim
	// path, Options, stage
    Shared path, Options, year	

	stage = args.Stage
    if stage = null then do
        stage = "UpdateLineLayer"  
        end	

	/* available stages (see Macro OMPO5 in ompo5.rsc):
	UpdateLineLayer
	HighwaySkim
	TransitSkim
	TripGeneration
	TripDistribution
	ModeChoice
	TimeOfDay
	HighwayAssign
	TransitAssign
	EJSummaries
	DTArun
	*/
	
    Options = args.Options
    if Options = null then do
	    dim Options[10]
        Options[1] = "0"
		Options[2] = 0
		Options[3] = "0"
		Options[4] = "0"
		Options[5] = "0"
		Options[6] = "1"
		Options[7] = "1"
		Options[8] = "0"
		Options[9] = "8"
		Options[10] = "0"
    end	
	
    /* Options
    stop_after_each_step = Options[1]           // Stops the model after each step
    iftoll=Options[2]		                    // indicate if toll is used, 0 means no toll.
    fixgdwy=Options[3]                          // indicate if fixed-guideway is used, 0 means no fixed-guideway
    userben=Options[4]                          // indicate if user benefits are to be written, 0 means no user benefits
    stop_after_each_itr = Options[5]            // Stops the model after each iteration
    iteration=StringToInt(Options[6])           // Get iteration number from GUI
    logsumAuto=Options[7]                       // indicate if mode choice is to write logsums by auto ownership (needed for urbansim)
    logsumMode=Options[8]                       // indicate if mode choice is to write logsums by mode
    max_iteration = StringToInt(Options[9])     // Converges by 3rd iteration; user can define max. 
    cordonPricing = Options[10]                 // Cordon pricing:  Reset the non-toll skims to 0 if toll skimmed	
	*/
	
	RunMacro("OMPO5", path, Options, stage)
	        
endMacro    
            
macro "ImportxlsFile" (args)
    RunMacro("Init", args)
	RunMacro("Create TAZ File")
endMacro    
            
macro "ExortMatrices" (args)
	matrices = args.matrices
	
	RunMacro("Convert Matrices to CSV", matrices)
endMacro
			
macro "SEMCOGExportMatrices" (args)
    outputFile     = args.ExportTo
    matrixOpts     = args.Matrix
            
    errMsg1 = "Specified matrix or core does not exist: "
    errMsg2 = "The matrix/core specification is incorrect."
    errMsg3 = "Can not open matrix file: "
    errMsg4 = "Can not write to the output file."
    errMsg5 = "Specified row or column index does not exist: "
            
    if matrixOpts = null | TypeOf(matrixOpts) <> "array" then do
        ret.error = errMsg2
        return(ret)
        end 
            
    //process matrixOpts to get matrices and cores
    dim MasterOpts[matrixOpts.length]
    for i = 1 to matrixOpts.length do
        matrixFile = matrixOpts[i][MATRIX_PATH]
        if GetFileInfo(matrixFile) = null then do
            ret.error = errMsg1 + matrixFile
            return(ret)
            end
            
        on error do
            ret.error = errMsg3 +  matrixFile
            return(ret)
            end
        on notfound do
            ret.error = errMsg3 +  matrixFile
            return(ret)
            end
            
        matrixHandler = OpenMatrix(matrixFile,)
            
        matrixCores = GetMatrixCoreNames(matrixHandler)
        matrixIndices = GetMatrixIndexNames(matrixHandler)
            
        row_index = matrixOpts[i][ROW_INDEX]
        col_index = matrixOpts[i][COL_INDEX]
            
        if ArrayPosition(matrixIndices[1],{row_index},) <= 0 |
           ArrayPosition(matrixIndices[2],{col_index},) <= 0 then do
            ret.error = errMsg5 + matrixFile
            return(ret)
            end
            
        coreOpts = matrixOpts[i][CORE_OPTS]
        if coreOpts = null then do
            ret.error = errMsg2
            return(ret)
            end
            
        dim coreNames[coreOpts.length]
        dim coreLabels[coreOpts.length]
        dim coreOrders[coreOpts.length]
        for j = 1 to coreOpts.length do
            coreNames[j] = coreOpts[j][1]
            coreLabels[j] = coreOpts[j][2]
            
            pos = ArrayPosition(matrixCores,{coreNames[j]},) 
            if pos <= 0 then do
                ret.error = "Matrix "+matrixFile+" does not contain core '"+core+"'."
                return(ret)
                end
            
            coreOrders[j] = pos
            end //for j = 1 to coreOpts.length
            
        MasterOpts[i] = {}
        MasterOpts[i].matrix = matrixHandler
        MasterOpts[i].indices = {row_index,col_index}
        MasterOpts[i].coreNames = coreNames
        MasterOpts[i].coreLabels = coreLabels
        MasterOpts[i].coreOrders = coreOrders
            
        end  //for i = 1 to matrixOpts.length
            
    on error default
    on notfound default
            
            
    //make a copy of the first matrix with specified cores only, rename them to output lebals,
    //add cores from other matrices if necessary, export the matrix to file
    //(matrices have to be compatibal)
    theMatrix = MasterOpts[1].matrix
            
    _indices = MasterOpts[1].indices
    _cores   = MasterOpts[1].coreNames 
    _coreLabels = MasterOpts[1].coreLabels
    _coreOrders = MasterOpts[1].coreOrders
            
    theMc = CreateMatrixCurrency(theMatrix, _cores[1], _indices[1], _indices[2],)
            
    minfo = GetMatrixInfo(theMatrix)
    matopts  = CopyArray(minfo[6])
    matopts.[File Name] = GetTempFileName("*.mtx")
    matopts.Cores =  _coreOrders
    matopts.Indices = "Current"
            
    theMatrix = CopyMatrix(theMc, matopts)
            
    //set core name to be the output labels
    for i = 1 to _coreLabels.length do
        SetMatrixCoreName(theMatrix, _cores[i], _coreLabels[i])
        end 
            
    // add other cores
    on error do
        ret.error = "Input matrices are not compatible."
        return(ret)
        end 
    on notfound do
        ret.error = "Input matrices are not compatible."
        return(ret)
        end 
            
    for i = 2 to MasterOpts.length do
        matrix = MasterOpts[i].matrix
            
        _cores      = MasterOpts[i].coreNames 
        _coreLabels = MasterOpts[i].coreLabels
        _indices    = MasterOpts[i].indices
            
        for j = 1 to _cores.length do
            //add an empty core
            AddMatrixCore(theMatrix, _coreLabels[j])
            theMc = CreateMatrixCurrency(theMatrix, _coreLabels[j],_indices[1],_indices[2],)
            
            //set cell values from the matrix
            args.[Force Missing] = "No"
            EvaluateMatrixExpression(theMc,"["+GetMatrixName(matrix)+"].["+_cores[j]+"]",rows,cols,args)
            end
        end 
            
    on error default
    on notfound default
            
    on error do
        ret.error = errMsg4
        return(ret)
        end 
    fp = OpenFile(outputFile,"w")
    WriteLine(fp," ")
    CloseFile(fp)
            
    opts = {}
    opts.Complete = "Yes"
    opts.Decimals = 2
    CreateTableFromMatrix(theMatrix,outputFile,"CSV", opts)    
            
    on error default
            
    //clean up
    theMc = null
    theMatrix = null
            
    for i = 1 to MasterOpts.length do
        matrix = MasterOpts[i].matrix
        matrix = null
        end 
    return(null)
endMacro    
            
Macro "GetFileLocation"
    ArgOpts = null
            
    if ArgOpts <> null then do
        ArgOpts.error = null
        return(ArgOpts)
        end 
            
    //Ret = RunMacro("SEMCOG Init")
    if Ret = null then do
        ret.error = "Error initiating SEMCOG. Please run SEMCOG setup in TransCAD."
        return()
        end 
            
    {scenario_file, StepMacro, StepTitle, StepFlag, StageName, Args} = Ret
            
    if !RunMacro("TCP Load Scenario File", scenario_file, Args, &Arr) then  do // if loading not OK 
        ret.error = "Error loading scenario file " + scenario_file
        return()
        end 
    {, ScenArr, ScenSel} = Arr                                  // since same loading done earlier in project dbox init
    if ScenSel = null then do
        ret.error = "Error loading scenario file " + scenario_file
        return()
        end 
    scen_idx = ScenSel[1]
    Args = ScenArr[scen_idx][5]
    ArgOpts = RunMacro("TCP Convert to Argument Options", Args)
            
    return(ArgOpts)
endMacro    
            
macro "StartMacro" (args)
ShowMessage("Started "+i2s(args.length))
exit()      
endMacro    
            