package main

import "testing"

func TestFormatTime(t *testing.T) {
	type args struct {
		seconds int
	}
	tests := []struct {
		name string
		args args
		want string
	}{
		{"all day", args{60*60 *24 - 1}, "23:59:59"},
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
