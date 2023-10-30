option Explicit

' Hello world output in the diag box

dim ask
dim title

dim answer
ask = "Hey,what's your name?"
title = "Who are you?"

answer = InputBox(ask,title)


if answer = vbEmpty then
	MsgBox "You want to cancel? Fine!"	
	WSCript.Quit
elseif answer = "" then
	MsgBox  "You want to stay incongnito,all right with me..."	
else
	MsgBox  "Welcome " & answer & "!"
end if
