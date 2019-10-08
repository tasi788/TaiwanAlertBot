package main

import (
	depart "TaiwanAlertBot/depart"
	parser "TaiwanAlertBot/parser"
	"net/http"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api"
	"github.com/tidwall/gjson"

	"io/ioutil"
	"log"
)

func notify(text string, alert parser.Alert, resp []byte) {
	file, _ := ioutil.ReadFile("config.cfg")
	token := gjson.Get(string(file), "bot").String()
	bot, _ := tgbotapi.NewBotAPI(token)
	var ImgURL string

	switch {
	case alert.Info[0].Event == "颱風":
		text = depart.Typhoon(resp)
	case alert.Info[0].Event == "停班停課":
		text = depart.Qk(alert)
	case alert.Info[0].Event == "地震":
		ImgURL, text = depart.Earthquake(resp)

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

	var sent tgbotapi.Message
	var err error
	for ChatId := range ChatIdList {
		if len(ImgURL) > 1 {
			ImgFile, _ := http.Get(ImgURL)
			Img, _ := ioutil.ReadAll(ImgFile.Body)
			sendPhoto := tgbotapi.FileBytes{
				Name:  "photo.png",
				Bytes: Img,
			}
			msg := tgbotapi.NewPhotoUpload(ChatIdList[ChatId], sendPhoto)
			msg.Caption = text
			msg.ParseMode = "html"
			sent, err = bot.Send(msg)
		} else {
			msg := tgbotapi.NewMessage(ChatIdList[ChatId], text)
			sent, err = bot.Send(msg)
		}

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
