package main

import (
	"strings"
)

// Color process hex color to string
func Color(color string) string {
	tmp := ""

	switch strings.Contains(color, "#") == true {
	case color == "#EE9200":
		tmp = "🔶 #橙色"
	case color == "#3300FF":
		tmp = "🔵 #藍色"
	default:
		//tmp = "#無色"
		mapping := map[string]string{
			"藍色": "🔵",
			"橙色": "🔶",
			"紅色": "🔴",
			"黑色": "⚫",
			"黃色": "⭐",
			"綠色": "💚",
			"紫色": "😈",
		}
		tmp = mapping[color] + " #" + color

	}
	return tmp

}
