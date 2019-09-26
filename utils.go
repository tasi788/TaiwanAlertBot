package main

import (
	"strings"
)

// Color process hex color to string
func Color(color string) string {
	switch strings.Contains(color, "#") {
	case color == "#EE9200":
		return "橘色"
	case color == "#3300FF":
		return "藍色"
	default:
		return "無色"
	}
	return color
}
