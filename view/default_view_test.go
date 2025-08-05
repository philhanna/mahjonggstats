package view

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestNewDefaultView(t *testing.T) {
	assert.NotNil(t, NewDefaultView())
}
