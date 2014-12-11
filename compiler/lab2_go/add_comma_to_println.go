package main

import (
    "go/format"
    "go/ast"
    "go/parser"
    "go/token"
    "os"
)

func main() {
    src_filename:= "hello.go"
    dst_filename:= "hello_new.go"

    fset := token.NewFileSet()
    file, _ := parser.ParseFile(fset, src_filename, nil, parser.ParseComments);

    ast.Inspect(file, func(n ast.Node) bool {
        if expr, ok := n.(*ast.CallExpr); ok {

            f_name := expr.Fun.(*ast.Ident).Name

            if f_name == "println" {

                args := expr.Args
                new_args := []ast.Expr{}

                for i, arg := range args {
                    if i != 0 {
                        new_args = append(new_args, 
                            &ast.BasicLit {
                                Kind: token.STRING,
                                Value: "\", \"",
                        })    
                    }
                    new_args = append(new_args, arg)                        
                }
                expr.Args = new_args
            }
        }

        return true
    })

    dst, _ := os.Create(dst_filename)
    format.Node(dst, token.NewFileSet(), file)
}