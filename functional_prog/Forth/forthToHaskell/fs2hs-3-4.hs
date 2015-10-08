-- fs2hs-1.hs utf-8 ru unix eolns

-- import Data.Char

import Text.ParserCombinators.Parsec
import System.Environment ( getArgs )

-- import Text.Parsec
-- import Text.Parsec.String
-- import Text.Parsec.Expr
-- import Text.Parsec.Token
-- import Text.Parsec.Language

-- Forth source parser, ok -----------------------------------------------------

data W = IntNum    Int
    | Word         String
    | Quoted       String
    | StackComment String
    | LineComment  String
    | Definition   String [W]
    | IfThen       [W]
    | DoLoop       [W]
    | DoLoopPlus   [W]
    | BeginUntil   [W]
    deriving (Show, Read, Eq)
    
eols = "\n\r\f\v"
spcs = " \t\n\r\f\v"

endOfWord = eof <|> (oneOf spcs >> spaces)

int :: Parser W
int = uint <|> sint

uint :: Parser W
uint = do
    ds <- many1 $ digit
    endOfWord
    return $ IntNum $ read ds
    
sint :: Parser W
sint = do
    char '-'
    ds <- many1 $ digit
    endOfWord
    return $ IntNum $ read $ "-" ++ ds

quoted :: Parser W
quoted = do
    char '.'
    char '"'
    oneOf spcs
    q <- manyTill anyChar (try (char '"' >> endOfWord))
    return $ Quoted q

stackComment :: Parser W
stackComment = do
    char '('
    endOfWord
    c <- manyTill anyChar (try ( oneOf spcs >> char ')' >> endOfWord))
    return $ StackComment c
    
lineComment :: Parser W
lineComment = do
    char '\\'
    endOfWord
    c <- manyTill anyChar (try (char '\n' >> many (oneOf spcs)))
    return $ LineComment c

definition :: Parser W
definition = do
    char ':'
    endOfWord
    name <- many1 $ noneOf spcs
    endOfWord
    ws <- manyTill ( choice [ try quoted
                            , try int
                            , try stackComment
                            , try lineComment
                            , try ifThen
                            , try doLoopPlus
                            , try doLoop
                            , try beginUntil
                            , word 
                            ] 
                   ) (try (char ';' >> endOfWord))
    return $ Definition name ws
    
ifThen :: Parser W
ifThen = do
    string "if"
    endOfWord
    ws <- manyTill ( choice [ try quoted
                            , try int
                            , try stackComment
                            , try lineComment
                            , try ifThen
                            , try doLoopPlus
                            , try doLoop
                            , try beginUntil
                            , word 
                            ]
                   ) (try (string "then" >> endOfWord))
    return $ IfThen ws
    
doLoop :: Parser W
doLoop = do
    string "do"
    endOfWord
    ws <- manyTill ( choice [ try quoted
                            , try int
                            , try stackComment
                            , try lineComment
                            , try ifThen
                            , try doLoopPlus
                            , try doLoop
                            , try beginUntil
                            , word 
                            ]
                   ) (try (string "loop" >> endOfWord))
    return $ DoLoop ws
    
doLoopPlus :: Parser W
doLoopPlus = do
    string "do"
    endOfWord
    ws <- manyTill ( choice [ try quoted
                            , try int
                            , try stackComment
                            , try lineComment
                            , try ifThen
                            , try doLoopPlus
                            , try doLoop
                            , try beginUntil
                            , word 
                            ]
                   ) (try (string "+loop" >> endOfWord))
    return $ DoLoopPlus ws
    
beginUntil :: Parser W
beginUntil = do
    string "begin"
    endOfWord
    ws <- manyTill ( choice [ try quoted
                            , try int
                            , try stackComment
                            , try lineComment
                            , try ifThen
                            , try doLoopPlus
                            , try doLoop
                            , try beginUntil
                            , word 
                            ]
                   ) (try (string "until" >> endOfWord))
    return $ BeginUntil ws
    
word :: Parser W
word = do
    w <- many1 $ noneOf spcs
    endOfWord
    return $ Word w
    
program = many1 ( choice [ try definition
                         , try int
                         , try quoted
                         , try stackComment
                         , try lineComment
                         , word
                         ] )
                     
testForthParser = do 
    src <- readFile {- "test.fs" -} {-"factorial-old.fs"-} "tree-demo.fs"
    case parse program "" src of
        Left err -> print err
        Right ws -> printTree "" ws-- mapM_ print ws
        
-- Prith the program tree, ok --------------------------------------------------

--           Indent     Words
printTree :: String -> [W] -> IO ()
printTree _ [] = return ()
printTree indent ((Definition name inners):outers) = putStr indent
    >> putStr "Definition "
    >> print name
    >> printTree (indent ++ "\t") inners
    >> printTree  indent outers
printTree indent ((DoLoop inners):outers) = putStr indent
    >> putStrLn "DoLoop"
    >> printTree (indent ++ "\t") inners
    >> printTree  indent outers
printTree indent ((DoLoopPlus inners):outers) = putStr indent
    >> putStrLn "DoLoopPlus "
    >> printTree (indent ++ "\t") inners
    >> printTree  indent outers
printTree indent ((BeginUntil inners):outers) = putStr indent
    >> putStrLn "BeginUntil "
    >> printTree (indent ++ "\t") inners
    >> printTree  indent outers
printTree indent ((IfThen inners):outers) = putStr indent
    >> putStrLn "IfThen "
    >> printTree (indent ++ "\t") inners
    >> printTree  indent outers
printTree indent (x:xs) = putStr indent
    >> print x 
    >> printTree indent xs
        
-- Forth -> Haskell ------------------------------------------------------------

{-  TODO:   ввести проверку на чистоту функции. Если функция чистая, 
            использовать композицию. Если с ПЭ, то использовать связывание ??? 
            Пока -- через связывание 
-}

fs2hs _ ws = 
    pass1 ws

pass1 :: [W] -> String
pass1 [] = "\n"
pass1 ((Definition name ws):rest) = 
    transDefinition name ws ++ pass1 rest
pass1 (w:ws) = pass1 ws -- ignore word

transDefinition :: String -> [W] -> String
transDefinition name ws = name 
    ++ " = "
    ++ transComposition ws
    ++ "\n"
        
transComposition :: [W] -> String
transComposition ws =
    foldl sep (head ts) (tail ts)
    where
        ts = reverse $ map transWord (filter inUse ws)
        sep w1 w2 = w1 ++ " . " ++ w2
        
inUse :: W -> Bool
inUse (StackComment _) = False
inUse (LineComment _) = False
inUse (Quoted _) = False
inUse (Word ".") = False
inUse (Word ".s") = False
inUse _ = True

       
transWord :: W -> String
transWord (IntNum n) = "push " ++ show n

transWord (Word "+") = "add"
transWord (Word "-") = "sub"
transWord (Word "*") = "mul"
transWord (Word "/") = "div'"

transWord (Word "<" ) = "lt"
transWord (Word ">" ) = "gt"
transWord (Word "<=") = "le"
transWord (Word ">=") = "ge"
transWord (Word "=" ) = "eq"
transWord (Word "<>") = "ne"

transWord (Word "or") = "or'"

transWord (Word "drop") = "drop'"
transWord (Word "2dup") = "dup2"
transWord (Word "2over") = "over2"

transWord (Word "I") = "push i" -- in loops
transWord (Word "i") = transWord (Word "I") -- synonym for I

transWord (Word ".") = "nop" -- don't use now

transWord (IfThen ws) = "ifThen ( "
    ++ transComposition ws
    ++ " )"
transWord (DoLoop ws) = "doLoop (\\ i -> "
    ++ transComposition ws
    ++ " )"
transWord (DoLoopPlus ws) = "doLoopPlus (\\ i -> "
    ++ transComposition ws
    ++ " )"
transWord (BeginUntil ws) = "until' ( "
    ++ transComposition ws
    ++ " )"

-- TODO:    придумать +loop

transWord (Word w) = w  -- most universal

transWord (LineComment  c) = "nop" -- ignore
transWord (StackComment c) = "nop" -- ignore

transWord x =  error $ "failed!" ++ (show x)  
 

--  TODO:   анализ писать сюда
    

main = do
    args <- getArgs
    src  <- readFile $ args !! 0
    lib  <- readFile "fs2hs-lib-3-4.hs"
    case (parse program "" src) of
        Left err -> print err
        Right ws -> printTree "" ws 
                    >> writeFile (args !! 1) (fs2hs "" ws)
                    >> appendFile (args !! 1) lib
        
-- eof
