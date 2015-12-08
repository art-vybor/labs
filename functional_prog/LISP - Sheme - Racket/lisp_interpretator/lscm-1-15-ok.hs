-- lscm.hs -- LessSCheMe, 2nd -- utf-8

import Text.ParserCombinators.Parsec hiding (spaces)
import Text.Parsec.Token ( makeTokenParser
                         , integer
                         , float
                         , stringLiteral
                         )
import Text.Parsec.Language (haskellDef)
import System.Environment (getArgs)
import Debug.Trace

main = do
    srcPath <- getArgs
    src <- readFile $ srcPath !! 0
    case parse program "" src of
        Left  err  -> putStrLn $ show err
        Right expr -> {- print expr >> -} go (Env expr [])

-- Program parser

data Expr = List [Expr] | Atom String 
                        | None 
                        deriving (Show, Eq)

program = do
    spaces
    l <- (list <|> atom <|> comment) `sepEndBy` spaces
    return $ List $ filter (/= None) l

list = do
    oneOf "(["
    spaces
    l <- (list <|> atom <|> comment) `sepEndBy` spaces
    spaces
    oneOf ")]"
    return $ List $ filter (/= None) l

atom = do
    a <- many1 $ noneOf " \t\n\r\f\v\\;()[]"
    return $ Atom a
    
comment = do
    char ';'
    c <- manyTill (noneOf "\n") (try (char '\n'))
    return $ None

spaces = many $ oneOf " \t\n\r\f\v"

-- Atom parser (used in builtins)

lexer = makeTokenParser haskellDef

pureInteger (Atom s) = case parse (integer lexer) "" s of
    Right x -> x
    Left  _ -> error $ "An integer expected, found " ++ s
    
pureDouble x@(Atom s) = 
    if isInteger x 
        then case parse (integer lexer) "" s of
            Right x -> fromInteger x
            Left  _ -> error $ "An integer expected, found " ++ s
        else case parse (float   lexer) "" s of
            Right x -> x
            Left  _ -> error $ "A real expected, found " ++ s
    
pureString (Atom s) = case parse (stringLiteral lexer) "" s of
    Right x -> x
    Left  _ -> error $ "A string literal expected, found " ++ s
    
pureBool (Atom "#t") = True
pureBool (Atom "#f") = False

-- Atom typing

isInteger (Atom s) = case parse (integer lexer) "" s of
    Right _ -> True
    Left  _ -> False
isInteger x = error $ "isInteger " ++ (show x)
    
areIntegers (List l) = and $ map isInteger l

toIntegers (List xs) = map pureInteger xs
toDoubles  (List xs) = map pureDouble  xs

-- Evaluator

data Env = Env { expr :: Expr
               , defs :: [(String, Expr)]
               } deriving (Show)
               
go env = case expr env of
    (List (x:xs)) -> let env' = eval env{expr = x} 
                     in do
                        printExpr $ expr env' -- print env'
                        go env'{expr = List xs}
    _ {- other -} -> putStrLn "ok" 
    where
        printExpr (Atom a) = putStrLn a
        printExpr (List l) = mapM_ printExpr l
        printExpr  None    = return ()

eval env = 
    case expr env of
        (List (x@(List _):xs)) -> -- apply high-order-fn like ((f g) x y z)
            env -- temporary     
        
        (List ((Atom a):xs)) -> -- apply fn to the arguments
            case lookup a (defs env) of
                Just f  -> apply   f env{expr = List xs} 
                Nothing -> builtin a env{expr = List xs}
                                
        (List []) -> env -- end of recursive evaluation
    
        x@(Atom a) -> -- apply fn to zero of arguments
            case lookup a (defs env) of
                Just f  -> apply   f env{expr = List []}
                Nothing -> builtin a env{expr = List []}
                
        None -> env -- resrved


apply (List [Atom _, x@(Atom _)]) env = env{expr = x} -- without args

apply (List [List (_:formalArgs), List body]) env = -- to args
    env'{ defs = defs env } 
    where
        env' = eval env{defs = localDefs, expr = List body}
        localDefs = map def (zip formalArgs args) ++ defs env
        List args = expr $ evalArgs env
        def ((Atom name), (Atom value)) = (name, List [Atom name, Atom value])
       
apply expr env = {-trace ("\n" ++ show expr ++ "\n" ++ show env)-} 
    env -- apply a value `as is'    

evalArgs :: Env -> Env       
evalArgs env = env{expr = List xs'}
    where
        xs' = map (\x -> (expr . eval) env{expr = x}) xs
        List xs = expr env

-- Builtin functions 

builtin "define" env =
    env{ defs = (name, expr env):(defs env),  expr = None} 
    where
        name = case expr env of
            (List [Atom a, _]) -> a
            (List [List ((Atom a):_), _]) -> a

builtin "+" env = 
    if areIntegers (expr env')
        then env'{expr = Atom (show n)}
        else env'{expr = Atom (show d)}
    where
        n = foldl1 (+) (toIntegers (expr env'))
        d = foldl1 (+) (toDoubles  (expr env')) 
        env' = evalArgs env 
     
-- add builtins before this line --
builtin a env = env{expr = Atom a} -- value `as is'?! 
       
-- eof
