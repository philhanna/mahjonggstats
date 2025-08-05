package model

import "time"

// Model is the set of functions that must be implemented by a structure
// that contains the application history.
type Model interface {
	EarliestDate() time.Time	// Date of earliest history record
	LatestData() time.Time		// Date of latest history record
	LevelNames() []string		// Name of all layout types in the history
}
