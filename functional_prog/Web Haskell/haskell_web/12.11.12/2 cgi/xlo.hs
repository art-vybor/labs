-- xlo.hs -- low-level CGI program

import System.Environment ( getEnvironment
                          , getEnv
                          )
import System.IO
import qualified Data.ByteString as BS

main = 
    putStrLn "Content-type: text/plain\n"
    >>  hSetBuffering stdin NoBuffering -- для загрузки длинных НЕ-txt файлов
    >>  lookupEnv' "REQUEST_METHOD"
    >>= query
    >>= putStrLn
    
query (Just "GET")  = getEnv "QUERY_STRING"
{-
query (Just "POST") = hGetContents stdin 

    Внимание! hGetContents stdin сохранено только для демонстрационных целей.
    Действительно, работает с короткими текстовыми файлами без использования
    CONTENT_LENGTH (за счет "ленивости"), но не может работать с длинными
    и бинарными файлами
-}
query (Just "POST") = do
    contentLength <- getEnv("CONTENT_LENGTH")
    buffer <- BS.hGet stdin (read contentLength)
    return $ show buffer
    -- не идеально, но результат уже пригоден к анализу ;)    
query  Nothing      = return "No REQUEST_METHOD"

-- lookupEnv not implemented in my GHC 7.0.3, (added to GHC 7.6.1)
lookupEnv' :: String -> IO (Maybe String)
lookupEnv' name = fmap (lookup name) getEnvironment

{-  From forms.html, GET method:

    t=the+text&r=on&b2=on&h=hidden+text&s=Option+2
    
--  From forms.html, POST method (hGetContents stdin):

------WebKitFormBoundary29jn2n7fliJaJO0G
Content-Disposition: form-data; name="upload"; filename="lo.hs"
Content-Type: text/x-haskell

-- lo.hs -- low-level CGI program

import System.Environment (getEnvironment)

main = 
    putStrLn "Content-type: text/plain\n"
    >>  getEnvironment
    >>= mapM_ printPair
    
printPair (name, value) = putStrLn $ name ++ " = " ++ value

{-  
    ... здесь идёт текст "как есть" ...
-}

------WebKitFormBoundary29jn2n7fliJaJO0G
Content-Disposition: form-data; name="comment"

A Haskell source
------WebKitFormBoundary29jn2n7fliJaJO0G--
    
    
-}
