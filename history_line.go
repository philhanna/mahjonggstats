package main

import (
	"fmt"
	"strconv"
	"strings"
	"time"
)

// HistoryLine is a single record in mahjongg history
type HistoryLine struct {
	line      string
	gameDate  time.Time
	levelName string
	seconds   int
}

// NewHistoryLine creates a new HistoryLine structure
func NewHistoryLine(line string) HistoryLine {
	const layout = time.RFC3339

	tokens := strings.Split(line, " ")
	historyLine := HistoryLine{}
	historyLine.line = line
	historyLine.gameDate, _ = time.Parse(layout, tokens[0])
	historyLine.levelName = tokens[1]
	historyLine.seconds, _ = strconv.Atoi(tokens[2])
	return historyLine
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

func (hl HistoryLine) GameDate() time.Time {
	return hl.gameDate
}
