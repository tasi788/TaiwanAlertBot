use chrono::Utc;
use core::option::Option;
use pickledb::{PickleDb, PickleDbDumpPolicy, SerializationMethod};
use reqwest::Url;
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use std::path::Path;
use std::{env, thread, time};

struct Bot {
    token: String,
    url: Url,
    client: reqwest::blocking::Client,
}

impl Bot {
    fn new(token: String) -> Self {
        let url = Url::parse(&format!("https://api.telegram.org/bot{}/", token)).unwrap();
        Bot {
            token,
            url,
            client: Default::default(),
        }
    }

    fn send_message(&mut self, photo: Vec<String>) -> bool {
        let mut media_group: Vec<Value> = Vec::new();
        let proxy_url = env::var("proxy_url").unwrap();

        for file_path in photo {
            let url = format!("https://satis.ncdr.nat.gov.tw/eqsms/data/{}", file_path);
            match reqwest::blocking::get(&url) {
                Ok(response) => {
                    // 獲取 Content-Length header
                    if let Some(size) = response.headers().get("content-length") {
                        if let Ok(size) = size.to_str().unwrap_or("0").parse::<u64>() {
                            // 檢查是否超過 9MB (10 * 1024 * 1024 bytes)
                            if size > 9 * 1024 * 1024 {
                                let media_item = json!({
                                    "type": "photo",
                                    "media": format!("{}/{}",&proxy_url, &url)
                                });
                                media_group.push(media_item);
                                println!("media_group: {:?}", media_group);
                            } else {
                                let media_item = json!({
                                "type": "photo",
                                "media": &url
                            });
                                media_group.push(media_item);
                            }
                        }
                    }
                }
                Err(e) => {
                    println!("無法取得圖片: {}", e);
                    continue;
                }
            };
        }
        println!("media_group: {:?}", media_group);
        let url = self.url.join("sendMediaGroup").unwrap();
        let chat_id = "-1002118573662";
        let thread = vec![678, 1882];
        let mut request_body = json!({
            "chat_id": chat_id,
            "media": media_group
        });
        for t in thread {
            request_body["message_thread_id"] = json!(t);
            // println!("thread: {:?}", request_body);
            // println!("url: {:?}", url);
            let r = self.client.post(url.clone()).json(&request_body).send();
            match r {
                Ok(r) => {
                    println!("{}", r.text().unwrap());
                }
                Err(_) => {}
            }
        }
        true
    }
}

struct DB {
    db: PickleDb,
}

impl DB {
    fn new() -> Self {
        let path = Path::new("data.db");
        if !path.exists() {
            PickleDb::new(
                &path,
                PickleDbDumpPolicy::AutoDump,
                SerializationMethod::Json,
            );
        }
        let db = PickleDb::load(
            &path,
            PickleDbDumpPolicy::AutoDump,
            SerializationMethod::Json,
        )
        .unwrap();
        DB { db }
    }

    fn query(&self, q: &str) -> bool {
        self.db.get::<bool>(q).unwrap_or(false)
    }

    fn add(&mut self, q: &str) -> bool {
        self.db.set(q, &true).unwrap();
        true
    }
}

struct NCDR {
    base_url: Url,
}

impl NCDR {
    fn new() -> Self {
        NCDR {
            base_url: Url::parse("https://satis.ncdr.nat.gov.tw/eqsms/data/eqlist.txt").unwrap(),
        }
    }

    fn fetch(&self) -> Option<Vec<EQList>> {
        //  https://satis.ncdr.nat.gov.tw/eqsms/data/eqlist.txt?_dc=1730189712207&page=1&start=0&limit=25
        let binding = Utc::now().timestamp_micros().to_string();
        let now = binding.as_str();
        let mut url = self.base_url.clone();
        url.query_pairs_mut()
            .append_pair("dc", now)
            .append_pair("page", "1")
            .append_pair("start", "0")
            .append_pair("limit", "25");
        println!("Fetching {}", url);

        match reqwest::blocking::get(url.as_str()) {
            Ok(r) => {
                let text = r.text().unwrap();
                let result: Vec<EQList> = serde_json::from_str(&text).unwrap();
                Some(result)
            }
            Err(_) => {
                println!("Fetch Fail");
                None
            }
        }
    }
}

#[derive(Default, Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct EQList {
    pub name: String,
    pub etime: String,
    pub file1: String,
    pub file2: String,
    pub file3: String,
    pub file4: String,
    pub file5: String,
    pub file6: String,
    pub file7: String,
    pub elocation: String,
    pub edegree: String,
}

fn main() {
    if env::var("TOKEN").unwrap_or("".to_string()) == "" {
        panic!("The TOKEN must not be empty");
    }
    if env::var("proxy_url").unwrap_or("".to_string()) == "" {
        panic!("The proxy URL must not be empty");
    }

    let token = env::var("TOKEN").unwrap();

    let client = NCDR::new();
    let mut bot = Bot::new(token.to_string());
    let eqdata = client.fetch();

    let mut db = DB::new();

    // init first time
    // match eqdata {
    //     Some(r) => {
    //         for i in r {
    //             let text = format!("{}-{}", i.name, i.etime);
    //             db.add(&text);
    //         }
    //     }
    //     _ => {}
    // }

    loop {
        let eqdata = client.fetch();
        match eqdata {
            Some(r) => {
                for i in r {
                    let text = format!("{}-{}", i.name, i.etime);
                    // println!("{}", text);
                    if !db.query(&text) {
                        let _ = bot.send_message(vec![i.file3, i.file6]);
                        // db.add(&text);
                    }
                }
            }
            _ => {}
        }
        thread::sleep(time::Duration::from_secs(60));
    }
}
