package mj

import (
	"log"
	"strings"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

// Mock object supplying known values for mahjongg history.
// Since it implements the Loader interface, it can be passed
// to the History constructor.
type MockHistoryLoader int

// Loads test data into history lines
func (m MockHistoryLoader) Load() []HistoryLine {
	var hls []HistoryLine
	lines := strings.Split(testdata, "\n")
	for _, line := range lines {
		hl, err := NewHistoryLine(line)
		if err != nil {
			log.Printf("Unexpected line in mock history data: %q\n", line)
		}
		hls = append(hls, hl)
	}
	return hls
}

func TestHistoryNew(t *testing.T) {
	h := NewHistory(new(MockHistoryLoader))
	assert.Equal(t, 6, len(h.Records))
	assert.Equal(t, 3, len(h.Levels))
	assert.Equal(t, 4, h.Levels["easy"].Count())
	assert.Equal(t, 1, h.Levels["ziggurat"].Count())
	assert.Equal(t, 1, h.Levels["difficult"].Count())
	assert.Equal(t, 0, h.Levels["BOGUS"].Count())
}

func TestHistoryEarliestDate(t *testing.T) {
	expected, _ := time.Parse(timeFormat, "2022-07-31T01:51:05-0400")
	h := NewHistory(new(MockHistoryLoader))
	actual := h.EarliestDate()
	assert.Equal(t, expected, actual)
}

func TestHistoryLatestDate(t *testing.T) {
	expected, _ := time.Parse(timeFormat, "2022-08-06T23:07:24-0400")
	h := NewHistory(new(MockHistoryLoader))
	actual := h.LatestDate()
	assert.Equal(t, expected, actual)
}

func TestHistoryLevelNames(t *testing.T) {
	h := NewHistory(new(MockHistoryLoader))
	actual := h.LevelNames()
	expected := []string{"difficult", "ziggurat", "easy"}
	assert.Equal(t, expected, actual)
}
