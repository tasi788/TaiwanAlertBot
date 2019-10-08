package main

import (
	parser "TaiwanAlertBot/parser"
	"encoding/json"
	"encoding/xml"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"

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

func process(resp []byte) {
	var alert parser.Alert
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

func redirect(w http.ResponseWriter, req *http.Request) {
	log.Println(req.Method)
	http.Redirect(w, req, "https://www.google.com", 301)
}

func main() {
	file, _ := ioutil.ReadFile("config.cfg")
	token := gjson.Get(string(file), "bot").String()
	bot, err := tgbotapi.NewBotAPI(token)
	if err != nil {
		panic(err)
	}
	log.Println(bot.Self.UserName)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	log.Println(fmt.Sprintf("http://localhost:%s", port))
	http.HandleFunc("/post", getData)
	http.HandleFunc("/", redirect)

	http.ListenAndServe(fmt.Sprintf(":%s", port), nil)
}
