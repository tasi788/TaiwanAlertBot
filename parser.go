package main

import (
	"encoding/xml"
)

type Alert struct {
	XMLName    xml.Name `xml:"alert"`
	Identifier string   `xml:"identifier"`
	Sender     string   `xml:"sender"`
	Sent       string   `xml:"sent"`
	Status     string   `xml:"status"`
	MsgType    string   `xml:"msgType"`
	Scope      string   `xml:"Scope"`
	Info       []Info   `xml:"info"`
}

type Info struct {
	XMLName   xml.Name `xml:"info"`
	Language  string   `xml:"language"`
	Category  string   `xml:"category"`
	Event     string   `xml:"event"`
	Urgency   string   `xml:"urgency"`
	Serverity string   `xml:"serverity"`
	Certainty string   `xml:"certainty"`
	// eventCode are unnecessary
	Effective   string      `xml:"effective"`
	Expires     string      `xml:"expires"`
	SenderName  string      `xml:"senderName"`
	Headline    string      `xml:"headline"`
	Description string      `xml:"description"`
	Instruction string      `xml:"instruction"`
	Web         string      `xml:"web"`
	Parameter   []Parameter `xml:"parameter"`
}

type Parameter struct {
	XMLName   xml.Name `xml:"parameter"`
	ValueName string   `xml:"valueName"`
	Value     string   `xml:"value"`
}
