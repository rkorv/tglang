function conditionLine()	{
	gsub( /[\t]/, "_" )		# Mark any TABs left in code
	sub( /[ \t]*$/, "" )		# Drop trailing whitespace
}
BEGIN	{
	if( LLEN == 0 ) LLEN = 75	# Desired line length of comment
	if( ccol == 0 ) ccol = 41	# Embedded comment origin
	TABWIDTH = 8
}
#########################################################################
/^[ \t]*[#]/	{			# Some kind of pre-processor line
	if( match( $0, /^[ \t]*[#][ \t]*[^ \t][^ \t]*/ ) > 0 )	{
		cmd = substr( $0, 1, RLENGTH )
		gsub( /[ \t]*/, "", cmd ) # Drop blanks
		if( (cmd == "#if")	|| (cmd == "#elif")	||
		    (cmd == "#else")	|| (cmd == "#endif")	||
		    (cmd == "#ifdef")	|| (cmd == "#ifndef")	||
		    (cmd == "#include")	|| (cmd == "#error") )	{
			# Simply print this control line
			print
			next
		} else if( (cmd != "#define") && (cmd != "#undef") )	{
			print
			print "#error what kind of deal is this"
			next
		}
	}
}
#########################################################################
{	conditionLine() }		# Drop nasty stuff about line
#########################################################################
#/\/\*[-=*]*\*\//	{		# Pass bar comment intact
#	print
#	next
#}
#########################################################################
# Interpret "/*--", that does not terminate comment on line, as block prefix
/\/\*[-=*][-=*]*[ \t]*$/	{
        # printf "Deaton original: %s.\n", $0
        if( match( $0, /\/\*[-=*][-=*]*[ \t]*$/ ) > 0 )  {
                left = substr( $0, 1, RSTART-1 )
                mid = "/* *" substr( $0, RSTART + 2, 1 )
                right = substr( $0, RSTART + RLENGTH )
                # printf "Deaton: %s|%s|%s.\n", left, mid, right
                $0 = sprintf( "%s%s%s", left, mid, right )
        }
}
#########################################################################
# Interpret "/*-*/" as a comment bar idiom
/\/\*[-=*][-=*]*\*\//	{
	if( match( $0, /\/\*[-=][-=]*\*\// ) > 0 )	{
		# Eat everything up until the final "*/"
		line = substr( $0, 1, RSTART+RLENGTH-3 )
		lineLen = length( line )
		c = substr( line, lineLen )
		mid = ""
		if( lineLen < 72 )	{
			wid = 72 - lineLen
			mid = sprintf( "%" wid "." wid "s", " " )
			gsub( /./, c, mid )
		}
		print line mid c "*/"
		next
	}
}
#########################################################################
# Handle C++ style comments by encapsulating
match( $0, /\/\// ) > 0	{
	$0 = sprintf( "%s/* %s */", substr( $0, 1, RSTART - 1 ),
	   substr( $0, RSTART + RLENGTH ) )
}
#########################################################################
#########################################################################
/\/\*.*\*\//	{			# Comment is complete on a single line
	# If it has fancy literals, do as a block comment
	if( $0 ~ /\*[-=*]/ )	{
		blockComment()
		next
	}
	# Compute amount of leading whitespace needed
	if( match( $0, /^[ ][ ]*/ ) > 0 )	{
		# Strip off leading spaces
		spaces = substr( $0, 1, RLENGTH )
		spacesLength = RLENGTH
		sub( /^[ ][ ]*/, "" )
	} else	{
		# No leading spaces
		spaces = ""
		spacesLength = length( spaces )
	}
	# Locate code (up to comment with any leading whitespace)
	if( substr( $0, 1, 2 ) != "/*" )	{
		# Line has code before the comment
		match( $0, /[ ]*\/\*[ ]*/ );
		code = substr( $0, 1, RSTART - 1 )
		codeLength = length( code )
		$0 = substr( $0, RSTART )
		used = (spacesLength + codeLength)
		if( used < ccol )	origin = ccol
		else			origin = used + 1
		fillerLength = origin - used - 1
		filler = blanks( fillerLength )
	} else	{
		# No code before the comment
		code = ""
		codeLength = length( code )
		filler = ""
		fillerLength = length( filler )
	}
	# Isolate comment and add trailing padding if necessary
	sub( /^[ ]*[\/][*][ ]*/, "" )	# Drop comment leadin
	sub( /[ ]*[*][\/][ ]*$/, "" )	# Drop comment trailer
	gsub( /[	][	]*/, " " ) # Squeeze whitespace in comment
	# comment = $0			# What is left is the commentary
	# What is left is the commentary
	comment = toupper( substr( $0, 1, 1 ) ) substr( $0, 2 )
	commentLength = length( comment )
	# May need to pad the code line with whitespace to align comment
	trailingPad = LLEN - spacesLength - codeLength - fillerLength - commentLength - 6
	if( trailingPad > 0 )	{
		# Add trailing spaces
		comment = comment blanks( trailingPad )
	}
	comment = "/* " comment " */"	# Add delimiters
	commentLength = length( comment )
	# printf "comment=|%s|, l=%d\n", comment, commentLength	# FIXME
	printf "%s%s%s%s\n", spaces, code, filler, comment
	next
}
#########################################################################
# Also allow a C++ style comment
/\/\//  {				# C++ style comment
	# Compute amount of leading whitespace needed
	if( match( $0, /^[ ][ ]*/ ) > 0 )	{
		# Strip off leading spaces
		spaces = substr( $0, 1, RLENGTH )
		spacesLength = RLENGTH
		sub( /^[ ][ ]*/, "" )
	} else	{
		# No leading spaces
		spaces = ""
		spacesLength = length( spaces )
	}
	# Locate code (up to comment with any leading whitespace)
	if( substr( $0, 1, 2 ) != "//" )	{
		# Line has code before the comment
		match( $0, /[ ]*\/\/[ ]*/ );
		code = substr( $0, 1, RSTART - 1 )
		codeLength = length( code )
		$0 = substr( $0, RSTART )
		used = (spacesLength + codeLength)
		if( used < ccol )	origin = ccol
		else			origin = used + 1
		fillerLength = origin - used - 1
		filler = blanks( fillerLength )
	} else	{
		# No code before the comment
		code = ""
		codeLength = length( code )
		filler = ""
		fillerLength = length( filler )
	}
	# Isolate comment and add trailing padding if necessary
	sub( /^[ ]*[\/][\/][ ]*/, "" )	# Drop comment leadin
	sub( /[ ]*$/, "" )		# Drop comment trailer
	gsub( /[	][	]*/, " " ) # Squeeze whitespace in comment
	# comment = $0			# What is left is the commentary
	# What is left is the commentary
	comment = toupper( substr( $0, 1, 1 ) ) substr( $0, 2 )
	commentLength = length( comment )
	# May need to pad the code line with whitespace to align comment
	trailingPad = LLEN - spacesLength - codeLength - fillerLength - commentLength - 3
	if( trailingPad > 0 )	{
		# Add trailing spaces
		comment = comment blanks( trailingPad )
	}
	comment = "// " comment		# Add delimiters
	commentLength = length( comment )
	# printf "comment=|%s|, l=%d\n", comment, commentLength	# FIXME
	printf "%s%s%s%s\n", spaces, code, filler, comment
	next
}
#########################################################################
# A line beginning with "/*" will be a block comment
/^[ \t]*[\/][*]/	{
	sub( /\/\*/, "/* " )		# Ensure we have blanks around "/*"
	blockComment()
	next
}
{	print	}			# Print everything else intack
#########################################################################
function blockComment()	{
	leadin = $0
	sub( /\/\*.*/, "", leadin )	# Drop everything after leading spaces
	lmin = llen = length( leadin ) + 2
	for( ; ; )	{
		sub( /^[ \t]*/, "" )		# Drop leading whitespace now
		if( $0 ~ /^\*[ \t]*$/ )	{
			# Line contains only a "*", so treat as line break
			flushline()
			printf "%s *\n", leadin
		} else if( $0 ~ /[*][+]/ )	{
			# Line contains "*+", so copy verbatim until next one
			doline()
			while( getline > 0 )	{
				sub( /^[ \t]*/, "" )
				if( $0 ~ /^[*][-]/ ) break
				if( $0 ~ /^[*][+]/ )	{
					doline()
				} else	{
					if( match( $0, /^[*][ \t]?/ ) > 0 )	{
						# Drop leading asterisk
						$0 = substr( $0,	\
							RSTART + RLENGTH )
					}
					printf "%s * %s\n", leadin, $0
				}
			}
			doline()
		} else if( NF > 0 )	{
			if( doline() ) return
		}
		if( getline <= 0 ) break
	}
	flushline()
}
#########################################################################
# Add each token to output line
function doline(		i, token, tlen )	{
	for( i = 1; i <= NF; ++i )	{
		token = $i
		if( token == "/*" )	{
			in_comment = 1
			flushline()
			printf "%s/*\n", leadin
		} else if( token == "*" )	{
			if( NF == 1 )	{
				flushline()
				printf "%s *\n", leadin
			}
		} else if( token ~ /[*][\/]$/ )	{
			if( token != "*/" )	{
				# Has leading garbage
				tlen = length( token )-2
				if( (llen + tlen + 1) >= LLEN )	{
					flushline()
				}
				line = line " " substr( token, 1, tlen )
				llen += tlen + 1
			}
			flushline()
			printf "%s */\n", leadin
			starSlash = 0
			return( 1 )
		} else if( token ~ /^\*[-=*]*$/ )	{
			flushline()
			tlen = LLEN - llen
			token = substr( token, 1, tlen )
			x = sprintf( "%-" tlen "." tlen "s", token )
			gsub( / /, substr( token, 2, 1 ), x )
			printf "%s %s\n", leadin, x
		} else if( token ~ /^\*[+][-=*]*$/ )	{
			flushline()
			tlen = LLEN - llen
			token = substr( token, 1, tlen )
			x = sprintf( "%-" tlen "." tlen "s", token )
			gsub( / /, substr( token, 3, 1 ), x )
			printf "%s %s\n", leadin, x
		} else	{
			tlen = length( token )
			if( (llen + tlen + 1) >= LLEN )	{
				flushline()
			}
			line = line " " token
			llen += tlen + 1
		}
	}
	return( 0 )
}
#########################################################################
function flushline()	{
	if( llen > lmin ) printf "%s *%s\n", leadin, line
	line = ""
	llen = lmin
}
#########################################################################
function blanks( n,		s )	{
	if( n > 0 )	s = sprintf( "%" n "." n "s", " " )
	else	s = ""
	return( s )
}
