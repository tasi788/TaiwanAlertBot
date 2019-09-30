package main

import (
	"encoding/json"
	"net/http"
)

/*
func getFilelist(path string) []string {
	goList := []string{}
	filepath.Walk(path, func(path string, f os.FileInfo, err error) error {
		if f.IsDir() == false && strings.Contains(path, ".xml") {
			goList = append(goList, path)
		}
		return nil
	})
	return goList
}
*/

// getData process http post from NCDR
func getData(w http.ResponseWriter, req *http.Request) {
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
	//req.

}
func main() {
	http.HandleFunc("/post", getData)
	http.ListenAndServe(":8001", nil)

	//fileList := getFilelist("cap")
	//for k := range fileList {
	//	xmlFile, err := os.Open(fileList[k])
	//	if err != nil {
	//		fmt.Println(err)
	//		return
	//	}
	//	defer xmlFile.Close()
	//	byteValue, _ := ioutil.ReadAll(xmlFile)

	//var alert Alert
	//xml.Unmarshal(byteValue, &alert)

	//AlertColor := ""
	//for n := range alert.Info[0].Parameter {
	//	if alert.Info[0].Parameter[n].ValueName == "alert_color" {
	//		AlertColor = alert.Info[0].Parameter[n].Value
	//	}
	//}
	/*
		doc, err := xmlquery.Parse(strings.NewReader(string(byteValue)))
		ch := xmlquery.FindOne(doc, "//description")
		fmt.Println(ch.InnerText())

		text := "發布單位：#" + alert.Info[0].SenderName + "\n" +
			"蛤：" + alert.Info[0].Event + "\n" +
			"警報標題：" + alert.Info[0].Headline + "\n" +
			"警報顏色：" + Color(AlertColor) + "\n" +
			"警報描述：" + alert.Info[0].Description + "\n\n"

		//
		//"警報描述：" + alert.Info[0].Description + "\n" +
		fmt.Println(text)
		//fmt.Println(alert.Info[0].Description[0].Section[0].Key)
		//fmt.Println(alert.Info[0].Description)
	}*/

}
