import Network
import System.IO
import Control.Concurrent

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
    -- print to browser --
    reply handle (words line)
    loop handle

html = "<html><boby><p>It works!</body></html>"
sz = length html

reply handle ["Connection:","keep-alive"] = do
    hPutStrLn handle "HTTP/1.0 200 OK"
    hPutStrLn handle "Content-type: text/html"
    hPutStrLn handle ("Content-length: " ++ (show sz))
    hPutStrLn handle ""
    hPutStrLn handle html

reply handle ws = do
    print ws
