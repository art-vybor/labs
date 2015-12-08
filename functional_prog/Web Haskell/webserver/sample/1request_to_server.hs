import Network
import System.IO
import Control.Concurrent
import System.Environment




main = withSocketsDo $ do -- standard portable initialization
    socket <- listenOn $ PortNumber 1488
    args <- getArgs
    htmlFile <- return $ args !! 0
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

reply handle [] file = do -- request completed
    hPutStrLn handle "HTTP/1.0 200 OK"
    hPutStrLn handle "Content-type: text/html"
    hPutStrLn handle $ "Content-length: " ++ show (length file)
    hPutStrLn handle ""
    hPutStrLn handle file

reply handle answer file = do
                print answer
                    
