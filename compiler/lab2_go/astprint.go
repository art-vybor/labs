package main

import (
	"fmt"
	"go/ast"
	"go/parser"
	"go/token"
	"os"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Printf("usage: astprintf <filename.go>\n")

		return
	}

	fset := token.NewFileSet()
	if file, err := parser.ParseFile(
		fset,
		os.Args[1],
		nil,
		parser.ParseComments,
	); err == nil {
		ast.Fprint(os.Stdout, fset, file, nil)
	} else {
		fmt.Printf("Error: %v", err)
	}
}
