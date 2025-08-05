package model

import (
	"bufio"
	"os"
	"path/filepath"
	"sort"
	"time"
)

// DEFAULT_FILENAME is the history file name in the user home directory
const DEFAULT_FILENAME = ".local/share/gnome-mahjongg/history"

// ---------------------------------------------------------------------
// Type definitions
// ---------------------------------------------------------------------

// History represents all the mahjongg games played by this user.
type History struct {
	// The history line record array
	Records []HistoryLine

	// A map of level names to LevelHistory objects
	Levels map[string]LevelHistory
}

// ---------------------------------------------------------------------
// Constructors
// ---------------------------------------------------------------------

// NewHistory creates a new History containing all user history records.
func NewHistory(loaders ...HistoryLoader) History {

	h := new(History)

	// Load history records either from a mock object or the real
	// history file.
	switch {
	default: // No mock loader; use the real file.
		h.Records = h.Load()
	case len(loaders) > 0: // Mock loader was supplied.
		h.Records = loaders[0].Load()
	}

	// Create a map of level names to their associated history line
	// records
	namesToHistoryLines := make(map[string][]HistoryLine)
	for _, hl := range h.Records {
		levelName := hl.LevelName
		namesToHistoryLines[levelName] =
			append(namesToHistoryLines[levelName], hl)
	}

	// From this, construct level history objects for each level
	// name and store these in a map
	lm := make(map[string]LevelHistory)
	for levelName, historyList := range namesToHistoryLines {
		levelHistory := NewLevelHistory(levelName, historyList)
		lm[levelName] = levelHistory
	}

	h.Levels = lm

	return *h
}

// ---------------------------------------------------------------------
// Methods
// ---------------------------------------------------------------------

// Loads all history records.
//
// This method can be patched with a mock object that provides
// hard-coded data (see unit tests).
func (h History) Load() []HistoryLine {

	// Open the file relative to the user home directory.
	homeDir, _ := os.UserHomeDir()
	fileName := filepath.Join(homeDir, DEFAULT_FILENAME)
	fp, _ := os.Open(fileName)
	defer fp.Close()

	// Read the history file line by line and create HistoryLine
	// structs from it, adding them to the slice to be returned.
	lines := make([]HistoryLine, 0)
	scanner := bufio.NewScanner(fp)
	for scanner.Scan() {
		line := scanner.Text()
		hl, _ := NewHistoryLine(line)
		lines = append(lines, hl)
	}

	return lines
}

// EarliestDate returns the date of the earliest record in the history.
// Panics if there is no history.
func (h History) EarliestDate() time.Time {
	var minTime time.Time
	if len(h.Records) > 0 {
		for i, x := range h.Records {
			gameDateTime := x.GameDateTime
			if i == 0 || gameDateTime.Before(minTime) {
				minTime = x.GameDateTime
			}
		}
	}
	return minTime
}

// LatestDate returns the date of the latest record in the history.
// Panics if there is no history.
func (h History) LatestDate() time.Time {
	var maxTime time.Time
	for i, x := range h.Records {
		gameDateTime := x.GameDateTime
		if i == 0 || gameDateTime.After(maxTime) {
			maxTime = x.GameDateTime
		}
	}
	return maxTime
}

// LevelNames returns the list of all distinct level names in this
// history.  The list is sorted in ascending order of the mean game time
// of each level.
func (h History) LevelNames() []string {
	list := h.unsortedLevelNames()
	getMean := func(i int) float64 {
		nameI := list[i]
		mapI := h.Levels[nameI]
		meanI := mapI.Mean()
		return meanI
	}
	sort.Slice(list, func(i, j int) bool {
		meanI := getMean(i)
		meanJ := getMean(j)
		return meanI < meanJ
	})
	return list
}

// Returns the level names unsorted
func (h History) unsortedLevelNames() []string {
	var list []string
	for name := range h.Levels {
		list = append(list, name)
	}
	return list
}
