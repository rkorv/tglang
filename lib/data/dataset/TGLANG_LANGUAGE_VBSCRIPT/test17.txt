'
' FILE: CreateNewAdmin.vbs
' AUTHOR: Brian Arriaga
' CREATED: 2 June 2016
' MODIFIED:  2 June 2016
' ORIGINALLY CREATED FOR: EFT Server 6.5-7.3
' PURPOSE: This script can create a new admin user or group within EFT Server by using the CreateAdmin method.
' This script was created as a workaround to add Universal Groups and Domain Local Groups as admins into EFT Server.
' In EFT Server 7.2.x and prior, these groups are outside of visible scope for the admin portion of AD viewer.
' To use this script, modify the connection details and the AdminAccountType, isGroup, NewAdminPassword, 
' 
' NOTE: The creation and modification of COM API scripts is not within the standard scope of Support.
' All COM API scripts are supplied as a courtesy "AS IS" with no implied or explicit guarantee of function.
' GlobalSCAPE is not responsible for any damage to system or data as a result of using supplied COM API scripts.
' Further information and usage instruction on COM API methods can be found online within the help file: http://help.globalscape.com/help/
'


Set SFTPServer = WScript.CreateObject("SFTPCOMInterface.CIServer")

CRLF = (Chr(13)& Chr(10))

'Modify the below connection details to reflect your own environment.
txtServer = "localhost"
txtPort =  "1110"
txtAdminUserName = "a"
txtAdminPassword = "a"

'Modify the below 4 entries to configure the admin account/settings you desire.
'AdminAccountType:
' EFTAccount = 0,
' LocalComputerAccount = 1,
' ADAccount = 2,

AdminAccountType = 2

'group:
' True = Admin being added is a group
' False = Admin being added is not a group

isGroup = True

'NewAdminPassword
' Enter the desired Name for the new adminUser
' If AD group is being used (AdminAccountType=2) make sure to specify the domain in Domain\Group format.
NewAdmin = ""

'NewAdminPassword
' Enter the desired password for the new adminUser
' If group is being used, can be set to anything

NewAdminPassword= "P@ssWord!"


Call ConnectToServer()
Call CreateNewAdmin()


SFTPServer.Close
Set SFTPServer = nothing


'==========================================
'This sub connects to the server
'=========================================
Sub ConnectToServer()
	SFTPServer.Connect txtServer, txtPort, txtAdminUserName, txtAdminPassword

	If Err.Number = 0 Then
		WScript.Echo "Connected to EFT Server: "  & txtServer
	End If

  	If Err.Number <> 0 Then
    		WScript.Echo "Error connecting to '" & txtServer & ":" &  txtPort & "' -- " & err.Description & " [" & CStr(err.Number) & "]", vbInformation, "Error"
  	End If

End Sub

'==========================================
'This sub create a new Admin User or Group into EFT Server using the "CreateAdmin" method in format CreateAdmin(Admin Name, Admin Pass, Admin Type, Admin is Group)
'=========================================
Sub  CreateNewAdmin()
	
	Set adminUser = SFTPServer.CreateAdmin(NewAdmin, NewAdminPassword, AdminAccountType, isGroup)
	WScript.Echo "Admin login " + adminUser.Login + " created."

End Sub