package depart

import (
	parser "TaiwanAlertBot/parser"
	"strings"
)

// Qk ㄐㄐ要 cd
func Qk(alert parser.Alert) string {
	desc := strings.Split(alert.Info[0].Description, "]")[1]
	desc = strings.ReplaceAll(desc, "。", "\n")
	text := "\n" +
		desc + "\n" +
		"*備註*\n" +
		alert.Info[0].Instruction
	return text
}
