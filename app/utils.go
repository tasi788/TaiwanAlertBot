package main

import (
	"strings"
)

// Color process hex color to string
func Color(color string) string {
	tmp := ""
	if strings.Contains(color, "#") == true {
		if color == "#EE9200" {
			tmp = "🔶 #000000橙色"
		}
		if color == "#3300FF" {
			tmp = "🔵 #藍色"
		}
	} else {
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
