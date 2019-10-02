package main

import (
	"strings"
)

// Color process hex color to string
func Color(color string) string {
	switch strings.Contains(color, "#") {
	case color == "#EE9200":
		return "🔶 #橙色"
	case color == "#3300FF":
		return "🔵 #藍色"
	default:
		return "#無色"
	}
	mapping := map[string]string{
		"藍色": "🔵",
		"橙色": "🔶",
		"紅色": "🔴",
		"黑色": "⚫",
		"黃色": "💛",
	}
	tmp := "#" + color + mapping[color]
	return tmp

}
