-- hi.hs -- A CGI demo

import Network.CGI

main = runCGI $ handleErrors cgiMain 

cgiMain = do
    pairs <- getInputs
    setHeader "Content-type" "text/plain"
    output $ show pairs -- Content-type:
    
{-  getInput

    getInputs
    Get the names and values of all inputs. 
    Note: the same name may occur more than once in the output, 
    if there are several values for the name.
    
    getMultiInput
    Get all the values of an input variable, 
    for example from a form. This can be used to get all the values from form 
    controls which allow multiple values to be selected.
    
--  forms.html, GET:
    [("t","test"),("r","on"),("b2","on"),("h","hidden text"),("s","Option 2")]
    
--  forms.html, POST:
    [("upload","-- args.hs\n\nimport System.Environment ( getArgs )\n\nmain = 
    getArgs >>= print\n\n{-  *Main> :main arg1 arg2 arg3\n    [\"arg1\",\"arg2\"
    ,\"arg3\"]\n-}\n\r"),("comment","")]
-}
