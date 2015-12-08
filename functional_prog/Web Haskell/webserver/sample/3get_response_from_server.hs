import Network
import Network.URI
import System.IO
import Control.Concurrent

main = withSocketsDo $ do
    socket <- listenOn $ PortNumber 1488
    htmlFile <- return $ "index.html"
    file <- readFile htmlFile
    handler socket file
    
handler socket file = do
    (handle, _, _) <- accept socket
    hSetBuffering handle NoBuffering
    forkIO $ loop handle file
    handler socket file

    
loop handle file = do
    line <- hGetLine handle
    reply handle (words line) file
    loop handle file

-- if not response => request
reply handle [] file = do
    hPutStrLn handle "HTTP/1.0 200 OK"
    hPutStrLn handle "Content-type: text/html"
    hPutStrLn handle $ "Content-length: " ++ show (length file)
    hPutStrLn handle ""
    hPutStrLn handle file

-- if response => run script
reply handle response file = do
                    if isGET response then
                        print $ case parseURIReference $ argsFromGET response of
                            Just x -> uriPath x
                    else return ()

argsFromGET [_, args, _] = args

isGET ["GET", "/favicon.ico", _] = False
isGET ["GET", "/", _] = False
isGET ["GET", _, _] = True
isGET _ = False