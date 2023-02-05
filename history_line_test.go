package main

import (
	"testing"
)

func TestFormatTime(t *testing.T) {
	type args struct {
		seconds int
	}
	tests := []struct {
		name string
		args args
		want string
	}{
		{"all day", args{60*60*24 - 1}, "23:59:59"},
		{"empty", args{0}, "00:00"},
		{"hour plus", args{3603}, "01:00:03"},
		{"one minute", args{60}, "01:00"},
		{"two seconds", args{2}, "00:02"},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := FormatTime(tt.args.seconds); got != tt.want {
				t.Errorf("FormatTime() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestHistoryLine_GameDate(t *testing.T) {
	tests := []struct {
		name string
		ok   bool
		line string
		want string
	}{
		{"good one", true, "2019-11-30T20:05:00-0500 Normal 234", "2019-11-30"},
		{"bad one", false, "2019-11-30T20:05:00-050 Normal 234", "2019-11-30"},
	}
	for _, tt := range tests {
		line := tt.line
		historyLine, err := NewHistoryLine(line)
		if !tt.ok {
			if err == nil {
				t.Errorf("Parsing %s should be an error", line)
			}
		} else {
			gameDate := historyLine.GameDate()
			have := DateString(gameDate)
			want := "2019-11-30"
			if have != want {
				t.Errorf("GameDate(): have = %v, want %v", have, want)
			}
		}
	}
}
