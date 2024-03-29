package mj

import (
	"strings"
	"testing"
)

func levelHistory(levelName string) []HistoryLine {
	lines := strings.Split(testdata, "\n")
	var hls []HistoryLine
	for _, line := range lines {
		hl, _ := NewHistoryLine(line)
		if hl.LevelName == levelName {
			hls = append(hls, hl)
		}
	}
	return hls
}

func TestLevelHistory_Mean(t *testing.T) {
	type fields struct {
		levelName string
		records   []HistoryLine
	}
	tests := []struct {
		name   string
		fields fields
		want   float64
	}{
		{"good", fields{"easy", levelHistory("easy")}, 254.0},
		{"single entry", fields{"ziggurat", levelHistory("ziggurat")}, 228},
		{"empty", fields{"BOGUS", levelHistory("BOGUS")}, 0},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			lh := LevelHistory{
				LevelName: tt.fields.levelName,
				Records:   tt.fields.records,
			}
			have := lh.Mean()
			want := tt.want
			if !almostEqual(have, want) {
				t.Errorf("have=%f,want=%f", have, want)
			}
		})
	}
}

func TestLevelHistory_StandardDeviation(t *testing.T) {
	type fields struct {
		levelName string
		records   []HistoryLine
	}
	tests := []struct {
		name   string
		fields fields
		want   float64
	}{
		{"good", fields{"easy", levelHistory("easy")}, 61.98386},
		{"single entry", fields{"ziggurat", levelHistory("ziggurat")}, 0},
		{"empty", fields{"BOGUS", levelHistory("BOGUS")}, 0},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			lh := LevelHistory{
				LevelName: tt.fields.levelName,
				Records:   tt.fields.records,
			}
			have := lh.StandardDeviation()
			want := tt.want
			if !almostEqual(have, want) {
				t.Errorf("have=%f,want=%f", have, want)
			}
		})
	}
}

func TestLevelHistory_Confidence(t *testing.T) {
	type fields struct {
		levelName string
		records   []HistoryLine
	}
	tests := []struct {
		name   string
		fields fields
		wantLo float64
		wantHi float64
	}{
		{"good", fields{"easy", levelHistory("easy")}, 132.51162, 375.48838},
		{"single entry", fields{"ziggurat", levelHistory("ziggurat")}, 228, 228},
		{"empty", fields{"BOGUS", levelHistory("BOGUS")}, 0, 0},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			lh := LevelHistory{
				LevelName: tt.fields.levelName,
				Records:   tt.fields.records,
			}
			haveLo, haveHi := lh.Confidence()
			if !almostEqual(haveLo, tt.wantLo, 1e-2) {
				t.Errorf("test name %s, haveLo=%.2f, wantLo=%.2f", tt.name, haveLo, tt.wantLo)
			}
			if !almostEqual(haveHi, tt.wantHi, 1e-2) {
				t.Errorf("test name %s, haveHi=%.2f, wantHi=%.2f", tt.name, haveHi, tt.wantHi)
			}
		})
	}
}
