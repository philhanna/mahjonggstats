package mj

import (
	"testing"
)

func TestHistoryLine_constructor(t *testing.T) {
	type args struct {
		line string
	}
	tests := []struct {
		name          string
		args          args
		wantLevelName string
		wantSeconds   int
		wantErr       bool
	}{
		{
			"Good",
			args{"2023-01-04T22:12:03-0500 easy 209"},
			"easy",
			209,
			false,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			have, err := NewHistoryLine(tt.args.line)
			if have.LevelName != tt.wantLevelName {
				t.Errorf("Level name: want=%s,have=%s", tt.wantLevelName, have.LevelName)
			}
			if have.Seconds != tt.wantSeconds {
				t.Errorf("Seconds: want=%d,have=%d", tt.wantSeconds, have.Seconds)
			}
			if tt.wantErr && err == nil {
				t.Error("Should have returned an error")
			}
		})
	}
}

func TestHistoryLine_TimeDate(t *testing.T) {
	line := "2019-11-30T20:05:00-0500 Normal 234"
	hl, _ := NewHistoryLine(line)
	want := "03:54 (2019-11-30)"
	have := hl.TimeDate()
	if want != have {
		t.Errorf("want=%s,have=%s", want, have)
	}
}

func TestHistoryLine_String(t *testing.T) {
	hl, _ := NewHistoryLine("2023-01-04T22:12:03-0500 easy 209")
	want := `GameDateTime="2023-01-04T22:12:03-0500", LevelName="easy", Seconds=209`
	have := hl.String()
	if have != want {
		t.Errorf("have=%s, want=%s", have, want)
	}
}

func TestHistoryLine_GameDateTime(t *testing.T) {
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
		hl, err := NewHistoryLine(line)
		if !tt.ok {
			if err == nil {
				t.Errorf("Parsing %s should be an error", line)
			}
		} else {
			gameDate := hl.GameDateTime
			have := DateString(gameDate)
			want := "2019-11-30"
			if have != want {
				t.Errorf("GameDate(): have = %v, want %v", have, want)
			}
		}
	}
}

func TestHistoryLine_FormatTime(t *testing.T) {
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
