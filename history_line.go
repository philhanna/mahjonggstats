package main

import (
	"strings"
	"time"
	"strconv"
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
