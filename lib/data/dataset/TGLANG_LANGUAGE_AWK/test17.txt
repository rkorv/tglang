#!/usr/bin/awk -f

# libdeps.awk -- ldd $(which binary1 binary2 binaryN...) | libdeps.awk

((fieldno) && $fieldno ~ /\//) {
    arr[$fieldno]
    next
}

(( NF > 1 ) && (!fieldno)) {
    for (i = 1; i <= NF; i++) {
        if ($i == "Name") {
            fieldno = i ; break
        }
    }
}

END {
    for ( i in arr )
        print i | "sort -r"

    close("sort -r")
}
