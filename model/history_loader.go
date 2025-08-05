package model

// ---------------------------------------------------------------------
// Type definitions
// ---------------------------------------------------------------------

// HistoryLoader specifies the method(s) that a history line loader must
// implement. The History type implements the interface, and so do any
// mock objects used for testing.
type HistoryLoader interface {
	Load() []HistoryLine
}
