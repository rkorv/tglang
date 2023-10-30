' List Your Domain Controller


Set objDomain = GetObject("LDAP://rootDse")

objDC = objDomain.Get("dnsHostName")
Wscript.Echo "Authenticating domain controller:" & objDC
