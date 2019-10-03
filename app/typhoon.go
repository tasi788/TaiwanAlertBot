package main

import (
	"encoding/xml"
)

type TyAlert struct {
	XMLName xml.Name `xml:"alert"`
	Info    []TyInfo `xml:"info"`
}

type TyInfo struct {
	XMLName     xml.Name        `xml:"info"`
	Parameter   []TyParameter   `xml:"parameter"`
	Description []TyDescription `xml:"description"`
}

// TyDescription sdf
type TyDescription struct {
	XMLName     xml.Name      `xml:"description"`
	TyphoonInfo []TyphoonInfo `xml:"typhoon-info"`
	Section     []TySections  `xml:"section"`
}

// TyphoonInfo 用ㄉ
type TyphoonInfo struct {
	XMLName xml.Name     `xml:"typhoon-info"`
	Section []TySections `xml:"section"`
}

type TySections struct {
	XMLName        xml.Name   `xml:"section"`
	Key            string     `xml:"title,attr"`
	Value          string     `xml:",chardata"`
	TyphoonName    string     `xml:"typhoon_name"`
	CwbTyphoonName string     `xml:"cwb_typhoon_name"`
	Analysis       []Analysis `xml:"analysis"`
}

// Analysis gggg
type Analysis struct {
	XMLName xml.Name `xml:"analysis"`
	Scale   []struct {
		Text string `xml:",chardata"`
		Lang string `xml:"lang,attr"`
	} `xml:"scale"`
}

type TyParameter struct {
	XMLName   xml.Name `xml:"parameter"`
	ValueName string   `xml:"valueName"`
	Value     string   `xml:"value"`
}
