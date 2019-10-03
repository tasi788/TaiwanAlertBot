package main

import (
	"encoding/json"
	"encoding/xml"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strings"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api"
	"github.com/tidwall/gjson"
)

// getData process http post from NCDR
func getData(w http.ResponseWriter, req *http.Request) {
	log.Println(req.Method)
	xmlresp := "<?xml version=\"1.0\" encoding=\"utf-8\" ?> <Data><Status>True</Status></Data>"

	if req.Method != "POST" {
		type ErrorResponse struct {
			Status string
			Reason string
		}
		loadResp := ErrorResponse{"Error", "Method Not Allowed"}
		resp, err := json.Marshal(loadResp)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.Write(resp)
		return
	}

	file, _ := ioutil.ReadAll(req.Body)
	process(file)
	w.Write([]byte(xmlresp))
}

func notify(text string, alert Alert, resp []byte) {
	file, _ := ioutil.ReadFile("config.cfg")
	token := gjson.Get(string(file), "bot").String()
	bot, _ := tgbotapi.NewBotAPI(token)

	switch {
	case alert.Info[0].Event == "颱風":
		var TyAlert TyAlert
		xml.Unmarshal(resp, &TyAlert)
		TyInfo := TyAlert.Info[0].Description[0].TyphoonInfo[0]
		text += "\n" +
			"報數：第 " + TyInfo.Section[0].Value + " 報\n" +
			"命名：" + TyInfo.Section[3].CwbTyphoonName + fmt.Sprintf("（%v） #%v\n", TyInfo.Section[3].TyphoonName, TyInfo.Section[3].Analysis[0].Scale[0].Text) +
			"動態：" + strings.ReplaceAll(TyAlert.Info[0].Description[0].Section[3].Value, "\n", "") + "\n" +
			"走向預測：" + strings.ReplaceAll(TyAlert.Info[0].Description[0].Section[2].Value, "\n", "")
	case alert.Info[0].Event == "停班停課":
		desc := strings.Split(alert.Info[0].Description, "]")[1]
		desc = strings.ReplaceAll(desc, "。", "\n")
		text += "\n" +
			desc + "\n" +
			"*備註*\n" +
			alert.Info[0].Instruction

	default:
		text += "\n" +
			"警報描述：" + alert.Info[0].Description
	}

	text += "\n\n" + "警報發布時間：" + alert.Info[0].Effective.Format("2006年01月02日 15:04")

	ChatIdListTmp := gjson.Get(string(file), alert.Info[0].Event).Array()
	ChatIdList := []int64{gjson.Get(string(file), "others").Int()}

	for x := range ChatIdListTmp {
		ChatIdList = append(ChatIdList, ChatIdListTmp[x].Int())
	}

	for ChatId := range ChatIdList {
		msg := tgbotapi.NewMessage(ChatIdList[ChatId], text)
		sent, err := bot.Send(msg)
		if err != nil {
			log.Println("========")
			log.Println(err.Error())
			log.Println("To:", sent.Chat.ID, "Msg_ID:", sent.MessageID)
			log.Println("========")
		} else {
			log.Println("To:", sent.Chat.ID, "Msg_ID:", sent.MessageID)
		}
	}
}

func process(resp []byte) {
	var alert Alert
	xml.Unmarshal(resp, &alert)

	AlertColor := ""
	for n := range alert.Info[0].Parameter {
		if alert.Info[0].Parameter[n].ValueName == "alert_color" {
			AlertColor = Color(alert.Info[0].Parameter[n].Value)
			break
		} else {
			AlertColor = "無顏色"
		}
	}

	text := "發布單位：#" + alert.Info[0].SenderName + "\n" +
		"警報活動：" + "#" + alert.Info[0].Event + "\n" +
		"警報顏色：" + AlertColor + "\n" +
		"警報標題：" + alert.Info[0].Headline + "\n"
	notify(text, alert, resp)
}

func main() {
	file, _ := ioutil.ReadFile("config.cfg")
	token := gjson.Get(string(file), "bot").String()
	bot, err := tgbotapi.NewBotAPI(token)
	if err != nil {
		panic(err)
	}
	log.Println(bot.Self.UserName)

	http.HandleFunc("/post", getData)
	http.ListenAndServe(":80", nil)
}
