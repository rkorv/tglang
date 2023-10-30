
' Monitor Active Directory Replication


strComputer = "."
Set objWMIService = GetObject("winmgmts:" _
    & "{impersonationLevel=impersonate}!\\" & _
        strComputer & "\root\MicrosoftActiveDirectory")

Set colReplicationOperations = objWMIService.ExecQuery _
        ("Select * from MSAD_ReplPendingOp")

If colReplicationOperations.Count = 0 Then
    Wscript.Echo "There are no replication jobs pending."
    Wscript.Quit
Else
    For each objReplicationJob in colReplicationOperations 
        Wscript.Echo "Serial number: " & objReplicationJob.SerialNumber
        Wscript.Echo "Time in queue: " & objReplicationJob.TimeEnqueued
        Wscript.Echo "DSA DN: " & objReplicationJob.DsaDN
        Wscript.Echo "DSA address: " & objReplicationJob.DsaAddress
        Wscript.Echo "Naming context DN: " & objReplicationJob.NamingContextDn
    Next
End If
