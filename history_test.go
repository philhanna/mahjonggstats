package mj

import (
	"fmt"
	"testing"
)

func TestHistoryLoad(t *testing.T) {
	h := NewHistory()
	for i, hl := range h.Records {
		fmt.Printf("%d: %v\n", i, hl)
	}
}