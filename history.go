package mj

import (
	"bufio"
	"os"
	"path/filepath"
)

// DEFAULT_FILENAME is the history file name in the user home directory
const DEFAULT_FILENAME = ".local/share/gnome-mahjongg/history"

// ---------------------------------------------------------------------
// Type definitions
// ---------------------------------------------------------------------

// History is a collection of HistoryLine records for this user from the
// gnome mahjongg history file.
type History struct {
	Records []HistoryLine
	Levels  map[string][]HistoryLine
}

// Loader specifies the method(s) that a history line loader must
// implement. The History type implements the interface, and so do
// any mock objects used for testing.
type Loader interface {
	Load() []HistoryLine
}

// ---------------------------------------------------------------------
// Constructors
// ---------------------------------------------------------------------

// NewHistory creates a new History containing all user history records.
func NewHistory(loaders ...Loader) History {
	
	h := new(History)

	// Load history either from the real file or a mock object
	var loader Loader
	if len(loaders) == 0 {
		loader = *h
	} else {
		loader = loaders[0]
	}
	h.Records = loader.Load()
	
	return *h
}

// ---------------------------------------------------------------------
// Methods
// ---------------------------------------------------------------------

// Loads all history records.
//
// This method can be patched with a mock object that provides
// hard-coded data.
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
