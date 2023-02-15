package mj

import "math"

const almostThreshold = 1e-5

func almostEqual(floats ...float64) bool {
	a := floats[0]
	b := floats[1]
	delta := almostThreshold
	if len(floats) > 2 {
		delta = floats[2]
	}
	return math.Abs(a-b) <= delta
}
