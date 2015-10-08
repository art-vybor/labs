--scheme interpretator by art-vybor
import System.Environment
import Text.ParserCombinators.Parsec

main = getArgs >>= return . (!! 0) >>= readFile >>= parseAll >>= go

-- types
data Expr = List [Expr] | Atom String | None deriving (Show, Eq)
data Env = Env { expr :: Expr, defs :: [(String, Expr)] } deriving (Show)
toString (Atom d) = d
toBool (Atom b) = read b :: Bool
toList (List l) = l

-- Parsing Lisp file
parseAll textFile = return $ expr where Right expr = parse program "" (textFile ++ "\n")

program = do
    spaces
    _list <- (list <|> atom <|> comment) `sepEndBy` spaces
    return $ List $ filter (/= None) _list
list = do
    oneOf "(["
    spaces
    _list <- (list <|> atom <|> comment) `sepEndBy` spaces
    oneOf ")]"
    return $ List $ filter (/= None) _list
atom = do
    a <- many1 $ noneOf " \t\n\r\f\v\\;()[]"
    return $ Atom a
comment = do
    char ';'
    c <- manyTill (noneOf "\n") (try (char '\n'))
    return $ None

-- execute
go program = exec Env { expr = program, defs = [] }	

exec :: Env -> IO()                     
exec env = case expr env of
    (List (x:xs)) -> let env' = eval env{expr = x} in do
                        printExpr $ expr env'
                        exec env'{expr = List xs}
    _ {- other -} -> putStrLn "ok" 

applyDefs env = 
    case expr env of
        (List (a:xs)) -> applyDefs env { defs = defs $ eval env {expr = a}, expr = List (xs)}
        (List []) -> env

calc a xs env = 
    case lookup a (defs env) of
                Just f  -> apply   f env{expr = List xs} 
                Nothing -> builtin a env{expr = List xs}

eval env = 
    case expr env of
        (List ((Atom a):xs)) -> calc a xs env  -- apply fn to the argument
        (Atom a) -> calc a [] env -- apply fn to zero of arguments
        (List ((List _):xs)) -> eval env { expr = last $ toList $ expr env, defs = defs env ++ defs (applyDefs env)} --define in define

apply (List [Atom _, Atom a]) env = env{expr = Atom a} -- without args
apply (List [List (_:formalArgs), List body]) env = env'{ defs = defs env } -- to args
    where
        env' = eval env{defs = localDefs, expr = List body}
        localDefs = map def (zip formalArgs (evalArgs' env)) ++ defs env
        def ((Atom name), (Atom value)) = (name, List [Atom name, Atom value])

evalArgs' env = map (\x -> expr $ eval env{expr = x}) (toList $ expr env)
evalArgs env = env {expr = List $ evalArgs' env }

-- built in functions
builtin "define" env =
    env { defs = (name, expr env):(defs env),  expr = None} 
    where name = case expr env of
            (List [Atom a, _]) -> a
            (List [List ((Atom a):_), _]) -> a

builtin "+" env = if areInts (expr env') then multiOpInts (+) env' else multiOpDoubles (+) env'
    where env' = evalArgs env
builtin "*" env = if areInts (expr env') then multiOpInts (*) env' else multiOpDoubles (*) env'
    where env' = evalArgs env
builtin "-" env = if areInts (expr env') then multiOpInts (-) env' else multiOpDoubles (-) env'
    where env' = evalArgs env

builtin "if" env =
     if toBool (expr $ eval $ env' {expr = head expr'})
        then eval (env' {expr = expr' !! 1})
        else eval (env' {expr = expr' !! 2})
    where
        expr' = toList(expr env')
        env' = evalArgs env

builtin ">" env = compare2 (>) env
builtin "<" env = compare2 (<) env
builtin "==" env = compare2 (==) env
builtin a env = env {expr = Atom a}

multiOpInts op env = env {expr = Atom (show $ foldl1 op (toInts (expr env)))}
multiOpDoubles op env = env {expr = Atom (show $ foldl1 op (toDoubles (expr env)))}

compare2 op env = env' {expr = Atom (show $ op (head $ toDoubles (expr env')) ( last $ toDoubles (expr env')))}
    where env' = evalArgs env

-- check types
isInt d = case reads d :: [(Integer, String)] of
  [(_, "")] -> True
  _         -> False
areInts (List l) = and $ map (isInt.toString) l
toInts (List xs) = map (\d -> read (toString d) :: Int) xs
toDoubles (List xs) = map (\d -> read (toString d) :: Double) xs

--Print Expression
printExpr :: Expr -> IO()  
printExpr (Atom a) = putStrLn a
printExpr (List l) = mapM_ printExpr l
printExpr  None    = return ()