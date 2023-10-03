package mj

// ---------------------------------------------------------------------
// Type definitions
// ---------------------------------------------------------------------

// Controller contains the view and command line arguments.
type Controller struct {
	view           *View
	name           string
	levelNamesOnly bool
	verbose        bool
}

// ---------------------------------------------------------------------
// Controllers
// ---------------------------------------------------------------------

// NewController creates a new Controller object using the specified
// view and command line arguments.
func NewController(view *View, args map[string]any) Controller {
	c := new(Controller)
	c.view = view
	c.name = string(args["n"].(string))
	c.levelNamesOnly = bool(args["l"].(bool))
	c.verbose = bool(args["v"].(bool))
	return *c
}

// ---------------------------------------------------------------------
// Methods
// ---------------------------------------------------------------------

// Run runs the application
func (c Controller) Run() {

	v := c.view

	// If the level names only option was specified, just print the
	// level names and return
	if c.levelNamesOnly {
		v.ShowLevelNames()
		return
	}

	// Print the number of games between the earliest and latest date
	if c.verbose && c.name == "" {
		v.ShowHeading()
	}

	// If quiet (not verbose), just print the history summary and return
	if !c.verbose {
		v.ShowSummary()
		return
	}

	// Print the history for each level
	v.ShowAllLevels()
}
