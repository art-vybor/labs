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

html =  "<html><boby><form name=\"frm\">" ++
        "<input type=\"hidden\" name=\"x\" id=\"x\" value=\"0\">" ++
        "<input type=\"hidden\" name=\"y\" id=\"y\" value=\"0\">" ++
        "<canvas width=\"100\" height=\"100\" style=\"border: solid 1px blue;\"" ++
        " onmousemove=\"frm.x.value=event.clientX; frm.y.value=event.clientX; document.frm.submit()\"></canvas>" ++
        "</form></body></html>"
        -- some problems with direct subbmitting mouse up/down events as all of the document is
        -- reloaded on submit

reply handle [] = do -- request completed
    hPutStrLn handle "HTTP/1.0 200 OK"
    hPutStrLn handle "Content-type: text/html"
    hPutStrLn handle $ "Content-length: " ++ show (length html)
    hPutStrLn handle ""
    hPutStrLn handle html
reply handle ws = do print ws
-- reply handle ws = do return () -- do nothing by default

--  Content to send


