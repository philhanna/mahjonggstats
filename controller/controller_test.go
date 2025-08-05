package controller

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestNewController(t *testing.T) {
	c := NewController()
	assert.NotNil(t, c)
}
