package mj

import "math"

const testdata = `2022-07-31T01:51:05-0400 easy 308
2022-08-04T22:27:39-0400 easy 243
2022-08-05T23:50:36-0400 difficult 218
2022-08-06T22:57:13-0400 ziggurat 228
2022-08-06T23:02:17-0400 easy 171
2022-08-06T23:07:24-0400 easy 294`

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
