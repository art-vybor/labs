import Network
import System.IO
import Control.Concurrent

--  Start a primitive HTTP server on localhost:3000
--  The implementation is to use standard ghci library

main = withSocketsDo $ do -- standard portable initialization
    socket <- listenOn $ PortNumber 3000
    handler socket
    
handler socket = do
    (handle, _, _) <- accept socket
    hSetBuffering handle NoBuffering
    forkIO $ loop handle
    handler socket
    
loop handle = do
    line <- hGetLine handle
    reply handle (words line)
    loop handle

html =  "<html><boby>" ++
        "<canvas width=\"100\" height=\"100\" style=\"border: solid 1px blue;\"></canvas>" ++
        "<p>It works!" ++ 
        "<br><a href=\"http://localhost:3000/?x=1&y=1\">Recall me with arg (?&)</a>" ++
        "<br><a href=\"http://localhost:3000/Test\">Recall me with arg</a>" ++
        "</body></html>"


reply handle [] = do -- request completed
    hPutStrLn handle "HTTP/1.0 200 OK"
    hPutStrLn handle "Content-type: text/html"
    hPutStrLn handle $ "Content-length: " ++ show (length html)
    hPutStrLn handle ""
    hPutStrLn handle html
reply handle ws = do print ws
-- reply handle ws = do return () -- do nothing by default

--  Content to send


