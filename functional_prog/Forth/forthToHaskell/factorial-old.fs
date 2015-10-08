\ factorial-old.fs
\ loop testing: factorial ; ok in gforth 0.7.0
\ simple version: x > 0 
: factorial ( x -- x! ) 
    1 +         ( x+1 -- )
    1           ( x+1 1 -- )
    swap        ( 1 x+1 -- )
    1           ( 1 x+1 1 -- )
    do          ( 1 -- )
        I       ( 1 index -- )
        *           ( 1*index -- ) \ from lessforth.py
    loop ( factorial )
;
." 1 factorial -- " 1 factorial . cr
." 2 factorial -- " 2 factorial . cr
." 3 factorial -- " 3 factorial . cr
." 4 factorial -- " 4 factorial . cr
." 5 factorial -- " 5 factorial . cr
\ end of program

