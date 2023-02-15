package main

import mj "github.com/philhanna/mahjonggstats"
import "flag"

func main() {
	var name string
	var levelNamesOnly bool
	var verbose bool

	flag.StringVar(&name, "n", "", "select only this level name")
	flag.BoolVar(&levelNamesOnly, "l", false, "show level names only")
	flag.BoolVar(&verbose, "v", false, "show detailed summary")
	flag.Parse()

	args := make(map[string]any)
	args["n"] = name
	args["l"] = levelNamesOnly
	args["v"] = verbose
	
	model := mj.NewHistory()
	view := mj.NewView(model)
	controller := mj.NewController(model, view, args)
	controller.Run()
}