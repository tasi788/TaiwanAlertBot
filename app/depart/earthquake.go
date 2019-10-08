package depart

import (
	"encoding/xml"
	"fmt"
	"strings"
)

// TEarthquake parse Earthquake
type TEarthquake struct {
	XMLName xml.Name `xml:"alert"`
	Info    struct {
		Text      string `xml:",chardata"`
		Language  string `xml:"language"`
		Category  string `xml:"category"`
		Event     string `xml:"event"`
		Urgency   string `xml:"urgency"`
		Severity  string `xml:"severity"`
		Certainty string `xml:"certainty"`
		EventCode struct {
			Text      string `xml:",chardata"`
			ValueName string `xml:"valueName"`
			Value     string `xml:"value"`
		} `xml:"eventCode"`
		Effective   string `xml:"effective"`
		Onset       string `xml:"onset"`
		Expires     string `xml:"expires"`
		SenderName  string `xml:"senderName"`
		Headline    string `xml:"headline"`
		Description string `xml:"description"`
		Web         string `xml:"web"`
		Parameter   []struct {
			Text      string `xml:",chardata"`
			ValueName string `xml:"valueName"`
			Value     string `xml:"value"`
		} `xml:"parameter"`
		Resource []struct {
			Text         string `xml:",chardata"`
			ResourceDesc string `xml:"resourceDesc"`
			MimeType     string `xml:"mimeType"`
			URI          string `xml:"uri"`
		} `xml:"resource"`
		Area []struct {
			Text     string `xml:",chardata"`
			AreaDesc string `xml:"areaDesc"`
			Circle   string `xml:"circle"`
			Geocode  []struct {
				Text      string `xml:",chardata"`
				ValueName string `xml:"valueName"`
				Value     string `xml:"value"`
			} `xml:"geocode"`
		} `xml:"area"`
	} `xml:"info"`
}

// Earthquake 處理一些東東嘻嘻
func Earthquake(resp []byte) (string, string) {
	var vEarthquake TEarthquake
	xml.Unmarshal(resp, &vEarthquake)
	Info := vEarthquake.Info
	var Img string
	for n := range Info.Resource {
		if Info.Resource[n].ResourceDesc == "地震報告圖" {
			Img = Info.Resource[n].URI
		}
	}
	var QuakeLocation, Depth, Magnitude string
	for n := range Info.Parameter {
		ValueName := Info.Parameter[n].ValueName
		Value := Info.Parameter[n].Value
		if ValueName == "EventLocationName" {
			QuakeLocation = Value
		}
		if ValueName == "EventDepth" {
			Depth = Value
		}
		if ValueName == "EventMagnitudeDescription" {
			Magnitude = Value
		}
	}
	text := "發布單位：#" + Info.SenderName + "\n" +
		"震央位置：" + QuakeLocation + "\n" +
		"地震深度：" + strings.Replace(Depth, "公里", " 公里", -1) + "\n" +
		"地震強度：" + strings.Replace(Magnitude, "規模", "規模 ", -1) + "\n" +
		"警報簡述：" + Info.Description + "\n\n" +
		"*備註*\n" +
		fmt.Sprintf("相關詳細地震資訊請上<a href=\"%v/\">地震測報中心</a>", Info.Web)
	/*
		發布單位：#中央氣象局
		地震資料來源：中央氣象局
		警報類型：#地震
		震央位置：花蓮縣壽豐鄉
		地震強度：芮氏規模4.8
		地震深度：5.0公里
		警報簡述：08/18 12:05花蓮縣壽豐鄉發生規模4.8有感地震，最大震度花蓮縣磯崎5級。
	*/
	return Img, text
}
