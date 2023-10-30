Set loTemp = New Template
With loTemp
.Load "formatting.html"
.Rep "Balance","123456789"
.Rep "ShutdownTime","now"
Response.Write .Render
End With