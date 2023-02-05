package main

import "testing"

func TestLevelHistory_Confidence(t *testing.T) {
	type fields struct {
		levelName string
		records   []HistoryLine
	}
	tests := []struct {
		name   string
		fields fields
		want   float64
		want1  float64
	}{
		// TODO: Add test cases.
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			lh := LevelHistory{
				levelName: tt.fields.levelName,
				records:   tt.fields.records,
			}
			got, got1 := lh.Confidence()
			if got != tt.want {
				t.Errorf("LevelHistory.Confidence() got = %v, want %v", got, tt.want)
			}
			if got1 != tt.want1 {
				t.Errorf("LevelHistory.Confidence() got1 = %v, want %v", got1, tt.want1)
			}
		})
	}
}
