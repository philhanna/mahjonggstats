package mj

import (
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestNewController(t *testing.T) {
	type args struct {
		view *View
		args map[string]any
	}
	tests := []struct {
		name string
		args args
		want Controller
	}{
		// TODO: Add test cases.
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			assert.Equal(t, 0, 0)
			if got := NewController(tt.args.view, tt.args.args); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("NewController() = %v, want %v", got, tt.want)
			}
		})
	}
}
