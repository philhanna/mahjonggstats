package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestValidateSortOption(t *testing.T) {
	tests := []struct {
		name    string
		sortOpt string
		wantErr bool
	}{
		{"Empty", "", false},
		{"GA", "GA", false},
		{"GD", "GD", false},
		{"NA", "NA", false},
		{"ND", "ND", false},
		{"TA", "TA", false},
		{"TD", "TD", false},
		{"G", "G", false},
		{"N", "N", false},
		{"T", "T", false},
		{"Mixed case", "nA", false},
		{"Lower case", "na", false},
		{"Bad field 1", "Y", true},
		{"Bad field 2", "XA", true},
		{"Bad order", "GU", true},
		{"Too long", "ABC", true},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			_, _, err := ValidateSortOption(tt.sortOpt)
			assert.Equal(t, tt.wantErr, err != nil)
		})
	}
}
