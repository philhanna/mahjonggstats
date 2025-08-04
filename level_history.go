package mj

import "github.com/montanaflynn/stats"

// ---------------------------------------------------------------------
// Type definitions
// ---------------------------------------------------------------------

// LevelHistory is a list of history lines for a particular level.
type LevelHistory struct {
	LevelName string
	Records   []HistoryLine
}

// ---------------------------------------------------------------------
// Constructors
// ---------------------------------------------------------------------

// NewLevelHistory creates a new LevelHistory object with the specified
// name and history line records.
func NewLevelHistory(levelName string, records []HistoryLine) LevelHistory {
	lh := new(LevelHistory)
	lh.LevelName = levelName
	lh.Records = records
	return *lh
}

// ---------------------------------------------------------------------
// Methods
// ---------------------------------------------------------------------

// Count returns the number of history lines in this level
func (lh LevelHistory) Count() int {
	return len(lh.Records)
}

// Min returns the least value of seconds in the level history
func (lh LevelHistory) Min() int {
	if lh.Count() == 0 {
		return 0
	}
	var record = lh.Records[0]
	var least = record.Seconds
	for _, record = range(lh.Records) {
		seconds := record.Seconds
		if seconds < least {
			least = seconds
		}
	}
	return least
}

// Mean returns the mean of the time values for all records.
func (lh LevelHistory) Mean() float64 {
	secondsList := make(stats.Float64Data, 0)
	for _, historyLine := range lh.Records {
		seconds := float64(historyLine.Seconds)
		secondsList = append(secondsList, seconds)
	}
	mean, err := secondsList.Mean()
	if err != nil {
		mean = 0
	}
	return mean
}

// StandardDeviation returns the standard deviation of the time values
// for all records.
func (lh LevelHistory) StandardDeviation() float64 {
	secondsList := make(stats.Float64Data, 0)
	for _, historyLine := range lh.Records {
		seconds := float64(historyLine.Seconds)
		secondsList = append(secondsList, seconds)
	}
	if len(secondsList) < 2 {
		return 0
	}
	stdev, _ := secondsList.StandardDeviationSample()
	return stdev
}

// Confidence returns the low and high estimates of the time values for
// all records at a 95% confidence level.
func (lh LevelHistory) Confidence() (float64, float64) {
	mean := lh.Mean()
	stdev := lh.StandardDeviation()
	conf := 1.96 * stdev
	lo := mean - conf
	if lo < 0 {
		lo = 0
	}
	hi := mean + conf
	return lo, hi
}
