Public Sub AddMapSurrounds()
  Dim pMxDoc As IMxDocument
  Dim pActiveView As IActiveView
  Dim pEnv As IEnvelope
  Dim pID As New UID
  Dim pMapSurround As IMapSurround
  Dim pMarkerNorthArrow As IMarkerNorthArrow
  Dim pCharacterMarkerSymbol As ICharacterMarkerSymbol
  
  Set pMxDoc = Application.Document
  Set pActiveView = pMxDoc.PageLayout
  Set pEnv = New Envelope
  
  'Add a north arrow
  pEnv.PutCoords 0.2, 0.2, 1, 1
  pID.Value = "esriCore.MarkerNorthArrow"
  Set pMapSurround = CreateSurround(pID, pEnv, "North Arrow", pMxDoc.FocusMap, pMxDoc.PageLayout)
  'Change out the default north arrow
  Set pMarkerNorthArrow = pMapSurround 'QI
  Set pCharacterMarkerSymbol = pMarkerNorthArrow.MarkerSymbol 'clones the symbol
  pCharacterMarkerSymbol.CharacterIndex = 200 'change the symbol
  pMarkerNorthArrow.MarkerSymbol = pCharacterMarkerSymbol 'set it back
  
  'Add a legend
  'In this case just use the default legend
  pEnv.PutCoords 7.5, 0.2, 8.5, 4
  pID.Value = "esriCore.Legend"
  Set pMapSurround = CreateSurround(pID, pEnv, "Legend", pMxDoc.FocusMap, pMxDoc.PageLayout)
  
  'Refresh the graphics
  pActiveView.PartialRefresh esriViewGraphics, Nothing, Nothing
End Sub


Private Function CreateSurround(pID As UID, pEnv As IEnvelope, strName As String, _
                           pMap As IMap, pPageLayout As IPageLayout) As IMapSurround
  
  Dim pGraphicsContainer As IGraphicsContainer
  Dim pActiveView As IActiveView
  Dim pMapSurroundFrame As IMapSurroundFrame
  Dim pMapSurround As IMapSurround
  Dim pMapFrame As IMapFrame
  Dim pElement As IElement
  
  'MapSurrounds are held in a MapSurroundFrame
  'MapSurroundFrames are related to MapFrames
  'MapFrames hold Maps
  Set pGraphicsContainer = pPageLayout
  Set pMapFrame = pGraphicsContainer.FindFrame(pMap)
  Set pMapSurroundFrame = pMapFrame.CreateSurroundFrame(pID, Nothing)
  pMapSurroundFrame.MapSurround.Name = strName

  'Set the geometry of the MapSurroundFrame to give it a location
  'Activate it and add it to the PageLayout's graphics container
  Set pElement = pMapSurroundFrame
  Set pActiveView = pPageLayout
  pElement.Geometry = pEnv
  pElement.Activate pActiveView.ScreenDisplay
  pGraphicsContainer.AddElement pElement, 0
  
  Set CreateSurround = pMapSurroundFrame.MapSurround
End Function



