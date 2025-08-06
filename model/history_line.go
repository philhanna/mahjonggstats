package model

import (
	"fmt"
	"strconv"
	"strings"
	"time"
)

const timeFormat = "2006-01-02T15:04:05-0700"

// ---------------------------------------------------------------------
// Type definitions
// ---------------------------------------------------------------------

// HistoryLine is a single record in mahjongg history.
// There is a file named "history" in ~/.local/share/gnome-mahjongg
// which contains a line for each completed game. This line contains:
//  1. A date and time stamp in the format yyyy-mm-ddTHH:MM:SS-9999
//  2. The name of the level (e.g., "easy", "overpass", etc.)
//  3. The number of seconds it took to complete the game.
//
// For example:
//
//	2023-01-04T22:12:03-0500 easy 209
//	2023-01-04T22:15:04-0500 easy 169
//	2023-01-04T22:20:38-0500 overpass 269
//	2023-01-06T14:31:35-0500 overpass 453
//	2023-01-06T16:36:48-0500 tictactoe 228
//	2023-01-06T16:42:17-0500 confounding 252
//	2023-01-06T17:01:03-0500 overpass 299
//	2023-01-06T17:07:52-0500 ziggurat 285
//	2023-01-06T17:13:49-0500 confounding 288
type HistoryLine struct {
	GameDateTime time.Time
	LevelName    string
	Seconds      int
}

// ---------------------------------------------------------------------
// Constructors
// ---------------------------------------------------------------------

// NewHistoryLine creates a new HistoryLine structure from a line in
// the mahjongg history file
func NewHistoryLine(line string) (HistoryLine, error) {

	tokens := strings.Split(line, " ")
	historyLine := HistoryLine{}
	gameDateTime, err := time.Parse(timeFormat, tokens[0])
	if err != nil {
		return historyLine, err
	}

	historyLine.GameDateTime = gameDateTime
	historyLine.LevelName = tokens[1]
	historyLine.Seconds, _ = strconv.Atoi(tokens[2])

	return historyLine, err
}

// ---------------------------------------------------------------------
// Methods
// ---------------------------------------------------------------------

// TimeDate returns the number of seconds found in this record in the
// format hh:mm:ss (MM/DD/YYYY)
func (hl HistoryLine) TimeDate() string {
	part1 := FormatTime(hl.Seconds)
	part2 := hl.GameDateTime.Format(time.RFC3339)[:10]
	return fmt.Sprintf("%s (%s)", part1, part2)
}

// String returns a string representation of the type
func (hl HistoryLine) String() string {
	var parts []string
	parts = append(parts, fmt.Sprintf("GameDateTime=%q", hl.GameDateTime.Format(timeFormat)))
	parts = append(parts, fmt.Sprintf("LevelName=%q", hl.LevelName))
	parts = append(parts, fmt.Sprintf("Seconds=%d", hl.Seconds))
	return strings.Join(parts, ", ")
}
