package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"strings"

	mj "github.com/philhanna/mahjonggstats"
)

func main() {

	const usage = `usage: mahjonggstats [OPTIONS]

Displays statistics from Gnome mahjongg.

options:
  -h, --help                  Show this help message and exit
  -n, --name=NAME             Include only level name NAME
  -l, --level-names-only      Show level names only
  -s, --sort=[G|N|T|M][A|D]   Sort by number of games, name, average, or min, asc/desc
  -v, --verbose               Show complete statistics

`
	// Custom usage message
	flag.Usage = func() { fmt.Fprint(os.Stderr, usage) }

	var name string
	var levelNamesOnly bool
	var sortOpt string
	var verbose bool

	flag.StringVar(&name, "n", "", "select only this level name")
	flag.StringVar(&name, "name", "", "(long version of -n)")
	flag.BoolVar(&levelNamesOnly, "l", false, "show level names only")
	flag.BoolVar(&levelNamesOnly, "level-names-only", false, "(long version of -l)")
	flag.StringVar(&sortOpt, "s", "MA", "Sort by number of games, name, average time, min, asc/desc")
	flag.StringVar(&sortOpt, "sort", "MA", "Sort by number of games, name, average time, min, asc/desc`")
	flag.BoolVar(&verbose, "v", false, "show detailed summary")
	flag.BoolVar(&verbose, "verbose", false, "(long version of -v)")
	flag.Parse()

	// Validate the sort option
	sortField, direction, err := ValidateSortOption(sortOpt)
	if err != nil {
		log.Fatal(err)
	}

	args := make(map[string]any)
	args["n"] = name
	args["l"] = levelNamesOnly
	args["sf"] = sortField // G, N, T, or M
	args["sd"] = direction // True if sort order must be reversed
	args["v"] = verbose

	model := mj.NewHistory()
	view, err := mj.NewView(&model, args)
	if err != nil {
		log.Fatal(err)
	}
	controller := mj.NewController(&view, args)
	controller.Run()
}

// ValidateSortOption validates the sort option. Length must be <= 2
// characters.  First character represents the sort field, which can be G
// for games played, N for game name, T for mean time, or M for min time, with M being
// the default.  Second character (if present) must be A for ascending,
// or D for descending, with A being the default. Option values are case
// insensitive.
func ValidateSortOption(sortOpt string) (string, bool, error) {

	// Make options string uppercase
	s := strings.ToUpper(sortOpt)

	// Pad it with defaults
	switch len(s) {
	case 0:
		s += "MA"
	case 1:
		s += "A"
	}

	// Validate sort field
	switch s[0] {
	case 'G', 'N', 'T', 'M':
		// OK
	default:
		return "", false, fmt.Errorf(`invalid sort option. Field must be G|N|T|M, not %c`, s[0])
	}

	// Validate sort order
	switch s[1] {
	case 'A', 'D':
		// OK
	default:
		return "", false, fmt.Errorf(`invalid sort option. Order must be A|D, not %c`, s[1])
	}

	// Everything is OK
	return string(s[0]), s[1] == 'D', nil
}
