package mj

import "github.com/montanaflynn/stats"

// LevelHistory is a list of history lines for a particular level
type LevelHistory struct {
	levelName string
	records   []HistoryLine
}

// Constructor for LevelHistory
func NewLevelHistory(levelName string, records []HistoryLine) *LevelHistory {
	lh := new(LevelHistory)
	lh.levelName = levelName
	return lh
}

// Mean returns the mean of the time values for all records
func (lh LevelHistory) Mean() float64 {
	secondsList := make(stats.Float64Data, 0)
	for _, historyLine := range lh.records {
		seconds := float64(historyLine.Seconds)
		secondsList = append(secondsList, seconds)
	}
	mean, _ := secondsList.Mean()
	return mean
}

// StandardDeviation returns the standard deviation of the time values for all records
func (lh LevelHistory) StandardDeviation() float64 {
	secondsList := make(stats.Float64Data, 0)
	for _, historyLine := range lh.records {
		seconds := float64(historyLine.Seconds)
		secondsList = append(secondsList, seconds)
	}
	if len(secondsList) < 2 {
		return 0
	}
	stdev, _ := secondsList.StandardDeviationSample()
	return stdev
}

// Confidence returns the low and high estimates at a 95% confidence level
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
