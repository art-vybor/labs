import System.Process
import Control.Concurrent
import System.IO
import System.Environment

main = do
    args <- getArgs
    fileName <- return $ args !! 0
    print fileName
    (inp, out, _, _) <- runInteractiveProcess fileName [] Nothing Nothing
    forkIO (hPutStrLn inp "" >> hClose inp)
    forkIO (putStrLn =<< hGetContents out)
    threadDelay 10000    
    return ()