' List Exchange XML Queue Data


On Error Resume Next

strComputer = "."
Set objWMIService = GetObject("winmgmts:" _
    & "{impersonationLevel=impersonate}!\\" & strComputer & _
        "\ROOT\MicrosoftExchangeV2")

Set colItems = objWMIService.ExecQuery _
    ("Select * from Exchange_QueueData")

For Each objItem in colItems
    Wscript.Echo "Server name: " & objItem.ServerName
    Wscript.Echo "XML queue data: " & objItem.XMLQueueData
    Wscript.Echo
Next
