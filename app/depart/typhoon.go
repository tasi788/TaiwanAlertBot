package depart

import (
	"encoding/xml"
	"fmt"
	"strings"
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

// Typhoon lol
func Typhoon(resp []byte) string {
	var TyAlert TyAlert
	xml.Unmarshal(resp, &TyAlert)
	TyInfo := TyAlert.Info[0].Description[0].TyphoonInfo[0]
	text := "\n" +
		"報數：第 " + TyInfo.Section[0].Value + " 報\n" +
		"命名：" + TyInfo.Section[3].CwbTyphoonName + fmt.Sprintf("（%v） #%v\n", TyInfo.Section[3].TyphoonName, TyInfo.Section[3].Analysis[0].Scale[0].Text) +
		"動態：" + strings.ReplaceAll(TyAlert.Info[0].Description[0].Section[3].Value, "\n", "") + "\n" +
		"走向預測：" + strings.ReplaceAll(TyAlert.Info[0].Description[0].Section[2].Value, "\n", "")
	return text

}