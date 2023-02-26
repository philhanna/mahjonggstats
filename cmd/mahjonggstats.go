package main

import (
	"flag"
	"fmt"
	"os"

	mj "github.com/philhanna/mahjonggstats"
)

func main() {

	const usage = `usage: mahjonggstats [OPTIONS]

Displays statistics from Gnome mahjongg.

options:
  -h, --help                  Show this help message and exit
  -n, --name NAME             Include only level name NAME
  -l, --level-names-only      Show level names only
  -v, --verbose               Show complete statistics

`
	// Custom usage message
	flag.Usage = func() { fmt.Print(usage) }

	var name string
	var levelNamesOnly bool
	var verbose bool

	// Short options
	flag.StringVar(&name, "n", "", "select only this level name")
	flag.StringVar(&name, "name", "", "(long version of -n)")
	flag.BoolVar(&levelNamesOnly, "l", false, "show level names only")
	flag.BoolVar(&levelNamesOnly, "level-names-only", false, "(long version of -l)")
	flag.BoolVar(&verbose, "v", false, "show detailed summary")
	flag.BoolVar(&verbose, "verbose", false, "(long version of -v)")
	flag.Parse()

	args := make(map[string]any)
	args["n"] = name
	args["l"] = levelNamesOnly
	args["v"] = verbose

	model := mj.NewHistory()
	view, err := mj.NewView(&model, args)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	controller := mj.NewController(&view, args)
	controller.Run()
}
