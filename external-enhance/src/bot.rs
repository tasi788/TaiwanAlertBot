use reqwest::Url;
use serde_json::{json, Value};

pub struct Bot {
    token: String,
    url: Url,
    client: reqwest::blocking::Client,
}

impl Bot {
    pub fn new(token: String) -> Self {
        let url = Url::parse(&format!("https://api.telegram.org/bot{}/", token)).unwrap();
        Bot {
            token,
            url,
            client: Default::default(),
        }
    }

    pub fn send_message(&mut self, photo: Vec<String>, caption: &str, threads: &str) -> bool {
        let mut media_group: Vec<Value> = Vec::new();
        for url in photo {
            let media_item = json!({
                "type": "photo",
                "media": &url
            });
            media_group.push(media_item);
        }

        media_group[0]["caption"] = caption.into();
        media_group[0]["parse_mode"] = "Markdown".into();
        // println!("media_group: {:?}", media_group);
        let url = self.url.join("sendMediaGroup").unwrap();
        let chat_id = "-1002118573662";
        let mut thread = vec![];
        if threads == "eq" {
            thread = vec![678, 1882, 1439]
        } else {
            thread = vec![700, 1882]
        }
        let mut request_body = json!({
            "chat_id": chat_id,
            "media": media_group
        });
        let mut result = false;
        for t in thread {
            request_body["message_thread_id"] = json!(t);
            // println!("thread: {:?}", request_body);
            let r = self.client.post(url.clone()).json(&request_body).send();
            match r {
                Ok(r) => {
                    if r.status().is_success() {
                        result = true
                    } else {
                        println!("{}", r.text().unwrap());
                    }
                }
                Err(_) => {}
            }
        }
        result
    }

    pub fn send_video(&mut self, video: &str, caption: &str, threads: &[&str]) -> bool {
        let url = self.url.join("sendVideo").unwrap();
        let chat_id = "-1002118573662";

        let mut request_body = json!({
            "chat_id": chat_id,
            "video": video,
            "caption": caption
        });

        let mut result = false;
        for thread in threads {
            request_body["message_thread_id"] = json!(thread);
            let r = self.client.post(url.clone()).json(&request_body).send();
            match r {
                Ok(r) => {
                    if r.status().is_success() {
                        result = true;
                    } else {
                        println!("{}", r.text().unwrap());
                    }
                }
                Err(_) => {}
            }
        }
        result
    }
}
