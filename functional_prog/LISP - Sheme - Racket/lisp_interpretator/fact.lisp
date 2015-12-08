(define (b x y) (+ x y))
(b 1 2)

{-"lambda" -> applyDefs env { defs = defs $ eval env {expr = List ((Atom "define"):k:(tail t))}, expr = List xs}
                    where
                        t = (tail $ toList x)
                        k = List((Atom "blabla"):toList(h))
                        h = head t -}

{-
sample env = getArgsToEval env [] --

getArgsToEval env ans = 
    case expr env of 
        (List (a:xs)) ->
            case lookup (toString a) (defs env) of
                Just f -> getArgsToEval (env {expr = List xs}) (ans)
                Nothing -> getArgsToEval (env {expr = List xs}) (a:ans)
        (List _ ) -> ans 
-- evalArgs :: Env -> Env
evalArgs' env ans =
    case expr env of 
        (List (a:xs)) ->
            case lookup (toString a) (defs env) of
                Just f  -> evalArgs' (env {expr = List xs}) (f:ans)
                Nothing -> evalArgs' env {expr = List xs} ((expr $ eval env{expr = a}):ans)
        (List []) -> ans
-}