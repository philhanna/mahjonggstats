package mj

import (
	"errors"
	"fmt"
	"sort"
	"time"
)

// ---------------------------------------------------------------------
// Type definitions
// ---------------------------------------------------------------------

// View presents the history on standard output.
type View struct {
	model      *History
	levelNames []string
	levels     []LevelHistory
}

// ---------------------------------------------------------------------
// Constructors
// ---------------------------------------------------------------------

// NewView creates a new View with the specified history model.
func NewView(model *History, args map[string]any) (View, error) {
	v := new(View)
	v.model = model

	// Restrict the levels if the -n option was specified
	if args["n"] != "" {
		name := args["n"].(string)
		lh, ok := model.Levels[name]
		if !ok {
			errmsg := fmt.Sprintf("mahjonggstats: Level %q not found in history", name)
			return *v, errors.New(errmsg)
		}
		v.levelNames = []string{name}
		v.levels = []LevelHistory{lh}
	} else {
		v.levelNames = append(v.levelNames, model.LevelNames()...)
		for _, level := range model.Levels {
			v.levels = append(v.levels, level)
		}
	}
	return *v, nil
}

// ---------------------------------------------------------------------
// Methods
// ---------------------------------------------------------------------

// ShowAllLevels displays the history for each level.
func (v View) ShowAllLevels() {
	for i, levelHistory := range v.levels {
		levelName := v.levelNames[i]

		mean := levelHistory.Mean()
		stndev := levelHistory.StandardDeviation()
		lo, hi := levelHistory.Confidence()
		count := levelHistory.Count()

		meanString := FormatTime(int(mean))
		stndevString := FormatTime(int(stndev))
		loString := FormatTime(int(lo))
		hiString := FormatTime(int(hi))
		countString := pluralize(count, "game")

		fmt.Printf("\n%d %s at level %q\n", count, countString, levelName)
		fmt.Printf("\tμ\t= %s\n", meanString)
		fmt.Printf("\tσ\t= %s\n", stndevString)
		fmt.Printf("\trange\t= %s to %s (at 95%% confidence level)\n", loString, hiString)

		// Slice of five if there are fewer:
		// https://go.dev/play/p/Kf85DFQ_8Lr

		// Create top5 with all the history, then sort it and select just the top 5.
		// This is actually the five *shortest* times.

		existing := len(levelHistory.Records)

		top5 := make([]HistoryLine, 0, len(levelHistory.Records)+5)
		for i, hl := range levelHistory.Records {
			if i < existing && len(top5) < 5{
				top5 = append(top5, hl)
			}
		}
		sort.Slice(top5, func(i, j int) bool {
			return top5[i].Seconds < top5[j].Seconds
		})

		scoreString := pluralize(len(top5), "score")
		fmt.Printf("\ttop %s:\n", scoreString)
		for _, h := range top5 {
			fmt.Printf("\t\t  %s\n", h.TimeDate())
		}
	}
}

// ShowHeading displays the number of games between the earliest and
// latest date.
func (v View) ShowHeading() {
	count := len(v.model.Records)
	start := v.model.EarliestDate().Format(time.DateOnly)
	end := v.model.LatestDate().Format(time.DateOnly)
	fmt.Printf("\nMahjongg history of %d games from %s to %s\n", count, start, end)
}

// ShowLevelNames displays the level names.
func (v View) ShowLevelNames() {
	for _, levelName := range v.levelNames {
		fmt.Println(levelName)
	}
}

// ShowSummary displays a summary of average times for each level.
func (v View) ShowSummary() {

	getPrefix := func(lh LevelHistory) string {
		count := lh.Count()
		gamesString := pluralize(count, "game")
		levelName := lh.LevelName
		return fmt.Sprintf("%d %s at level %q", count, gamesString, levelName)
	}

	prefixes := []string{}
	for _, lh := range v.levels {
		prefix := getPrefix(lh)
		prefixes = append(prefixes, prefix)
	}

	maxPrefixLength := 0
	for i, prefix := range prefixes {
		length := len(prefix)
		if i == 0 || length > maxPrefixLength {
			maxPrefixLength = length
		}
	}

	for _, lh := range v.levels {
		prefix := getPrefix(lh)
		part1 := fmt.Sprintf("%-*s", maxPrefixLength, prefix)
		part2 := fmt.Sprintf("average=%s", FormatTime(int(lh.Mean())))
		fmt.Println(part1 + " " + part2)
	}
}

func pluralize(count int, name string) string {
	if count == 1 {
		return name
	}
	return name + "s"
}
