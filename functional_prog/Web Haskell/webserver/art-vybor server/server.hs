import Network
import Network.URI
import System.IO
import Control.Concurrent
import System.Process
import System.Directory
import System.Random
import Data.List

data State = State { curPage :: String } deriving (Show)

main = withSocketsDo $ do
    socket <- listenOn $ PortNumber 1488 -- set listening port
    createDirectoryIfMissing True "www/.temp"
    mainLoop socket State {curPage = "/index.html"}

mainLoop socket state = do
    (handle, _, _) <- accept socket
    hSetBuffering handle NoBuffering
    forkIO $ letsCommunicate handle state -- try to get request, if not => print current state
    mainLoop socket state

letsCommunicate handle state = do
    request <- hGetLine handle -- get request
    state' <- buildResponse handle (words request) state
    letsCommunicate handle state'

-- if request is empty
buildResponse handle [] state
    | isHTML $ curPage state = printResponse handle state -- if page is simple html file => simple print
    | otherwise = calcScript handle state -- else invoke script

-- if request is'not empty => run script
buildResponse handle request state = do
    if isGET request then do
        print $ "get request: " ++ argsFromGET request
        return state {curPage = argsFromGET request}
    else return state

------------------------------------------------------------
--                                                        --
--              Additional Function                       --
--                                                        --
------------------------------------------------------------

--invokescript

calcScript handle state = do
    script <- return (case parseURIReference $ curPage state of 
        Just x -> uriPath x
        Nothing -> "")
    args <- return (case parseURIReference $ curPage state of 
        Just x -> uriQuery x
        Nothing -> "")
    print $ "try to invoke script: " ++ script ++ " with args: " ++ args

    answer <- invokeScript script (drop 1 args)
    printResponse handle state {curPage = answer}

    return state {curPage = answer}

invokeScript script args = do
    file <- return $ "www/"++ drop 1 script
    print $ "invoke: " ++ file
    fileExists <- doesFileExist file
    answer <-   if fileExists then do
                    rand <- randomIO
                    nameFile <- return $ "www/.temp/" ++ (show $ abs (rand::Int)) ++ ".html"
                    threadDelay 10000
                    (inp, out, err, _) <- runInteractiveProcess file [] Nothing Nothing
                    print $ "error: " ++ show err
                    print $ "args: " ++ args
                    argsMas <- return $ if null args then [] else argsToMassive (args ++ "&") []
                    inString <- return $ (show $ length argsMas) ++ " " ++ argsToString argsMas ""
                    forkIO (hPutStrLn inp inString >> hClose inp)
                    forkIO (writeFile nameFile =<< hGetContents out)
                    threadDelay 10000
                    return $ drop 3 nameFile
                else do
                    print "error: file not exist"
                    return "/404.html"
    
    return answer

argsToString args ans
    | null args = ans
    | otherwise = argsToString xs (ans ++ fst cur ++ " " ++ snd cur ++ " ")
    where (cur:xs) = args

argsToMassive args answer
    | null args = answer
    | otherwise = argsToMassive (drop (valLen + 1) other) ((arg, val):answer)
    where
        argLen = case elemIndex '=' args of
            Just x -> x
            Nothing -> -1
        arg = take argLen args
        other = drop (argLen + 1) args
        valLen = case elemIndex '&' other of
            Just x -> x
            Nothing -> -1
        val = take valLen other



--html                    
isHTML curPage = if take 5 (reverse curPage) == "lmth." then True else False

-- work with get
argsFromGET [_, args, _] = args

isGET ["GET", "/favicon.ico", _] = False
isGET ["GET", "/", _] = False
isGET ["GET", _, _] = True
isGET _ = False

-- print response
printResponse handle state = do
    print $ "response: name = " ++ curPage state
    if curPage state == "/404.html" then printPageNotFoundResponse handle state
                                    else printOkResponse handle state
    return state

printPageNotFoundResponse handle state = do
    printPageNotFoundHeader handle
    printContentFromFile handle (curPage state)

printOkResponse handle state = do
    printOkHeader handle
    printContentFromFile handle (curPage state)

printPageNotFoundHeader handle = do
    hPutStrLn handle "HTTP/1.1 404 Not Found"
    hPutStrLn handle "Connection: close"
    hPutStrLn handle "Server: Bayonne/1.5.4"
    hPutStrLn handle "Content-type: text/html"

printOkHeader handle = do
    hPutStrLn handle "HTTP/1.1 200 OK"

printContent handle content = do
    hPutStrLn handle "Content-type: text/html"
    hPutStrLn handle $ "Content-length: " ++ show (length content)
    hPutStrLn handle ""
    hPutStrLn handle content

printContentFromFile handle file = do
    fileData <- readFile $ "www" ++ file
    printContent handle fileData    

