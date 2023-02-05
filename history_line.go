package main

import (
	"fmt"
	"strconv"
	"strings"
	"time"
)

const timeFormat = "2006-01-02T15:04:05-0700"

// HistoryLine is a single record in mahjongg history
type HistoryLine struct {
	line      string
	gameDate  time.Time
	levelName string
	seconds   int
}

// NewHistoryLine creates a new HistoryLine structure from a line in
// the mahjongg history file
func NewHistoryLine(line string) (HistoryLine, error) {
	
	tokens := strings.Split(line, " ")
	historyLine := HistoryLine{}
	historyLine.line = line
	gameDate, err := time.Parse(timeFormat, tokens[0])
	if err != nil {
		return historyLine, err
	}
	historyLine.gameDate = gameDate
	historyLine.levelName = tokens[1]
	historyLine.seconds, _ = strconv.Atoi(tokens[2])
	return historyLine, err
}

// FormatTime creates a string with hh:mm:ss from the specified number of seconds
func FormatTime(seconds int) string {
	mm := int(seconds / 60)
	ss := seconds % 60
	timeString := fmt.Sprintf("%02d:%02d", mm, ss)
	if mm >= 60 {
		hh := int(mm/60)
		mm = mm % 60
		timeString = fmt.Sprintf("%02d:%02d:%02d", hh, mm, ss)
	}
	return timeString
}

// DateString returns the time as a date-only string in yyyy-mm-dd format
func DateString(t time.Time) string {
	return fmt.Sprintf("%04d-%02d-%02d", t.Year(), t.Month(), t.Day())
}

// Returns the game date (a time object)
func (hl HistoryLine) GameDate() time.Time {
	return hl.gameDate
}

