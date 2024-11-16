mod bot;
mod db;

use bot::Bot;
use chrono::Utc;
use core::option::Option;
use db::DB;
use regex::Regex;
use reqwest::Url;
use scraper::{Html, Selector};
use serde::{Deserialize, Serialize};
use std::{env, thread, time};
use std::fmt::format;

#[derive(Debug)]
struct NCREERecord {
    timestamp: String,
    eq_no: String,
    datetime: String,
    detail: String,
    depth: String,
    magnitude: String,
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

    fn fetch_ncree(&self) -> Option<Vec<NCREERecord>> {
        let url = Url::parse("https://seaport.ncree.org/eq_data/LOG/total_event.csv").unwrap();
        match reqwest::blocking::get(url.as_str()) {
            Ok(r) => {
                let data = r.text().unwrap();

                let mut reader = csv::ReaderBuilder::new()
                    .delimiter(b',')
                    .has_headers(false)
                    .flexible(true)
                    .from_reader(data.as_bytes());
                let records: Vec<NCREERecord> = reader
                    .records()
                    .filter_map(|record| {
                        record.ok().map(|r| NCREERecord {
                            timestamp: r.get(0).unwrap_or("").to_string(),
                            eq_no: r.get(1).unwrap_or("").to_string(),
                            datetime: r.get(2).unwrap_or("").to_string(),
                            detail: r.get(5).unwrap_or("").to_string(),
                            depth: r.get(4).unwrap_or("").to_string(),
                            magnitude: r.get(3).unwrap_or("").to_string(),
                        })
                    })
                    .collect();

                Some(records)
                // Some(reader.records())
            }
            Err(_) => None,
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
    // let eqdata = client.fetch();
    let mut db = DB::new();

    // init first time
    // match client.fetch() {
    //     Some(r) => {
    //         for i in r {
    //             let text = format!("{}-{}", i.name, i.etime);
    //             db.add(&text);
    //         }
    //     }
    //     _ => {}
    // }
    //
    // match client.fetch_ncree() {
    //     Some(r) => {
    //         for i in r {
    //             db.add(i.eq_no.as_str());
    //             db.add(i.timestamp.as_str());
    //         }
    //     }
    //     _ => {}
    // }
    println!("Ready to Wait!");

    loop {
        let eqdata = client.fetch();
        let proxy_url = env::var("proxy_url").unwrap();
        match eqdata {
            Some(r) => {
                for i in r {
                    let keyname = format!("{}-{}", i.name, i.etime);
                    if !db.query(&keyname) {
                        let mut url_list: Vec<String> = vec![];
                        for c in vec![i.file3, i.file6] {
                            let url = format!("https://satis.ncdr.nat.gov.tw/eqsms/data/{}", c);
                            match reqwest::blocking::get(&url) {
                                Ok(response) => {
                                    if let Some(size) = response.headers().get("content-length") {
                                        if let Ok(size) =
                                            size.to_str().unwrap_or("0").parse::<u64>()
                                        {
                                            // 檢查是否超過 9MB (10 * 1024 * 1024 bytes)
                                            if size > 5 * 1024 * 1024 {
                                                url_list
                                                    .push(format!("{}/x0.3/{}", &proxy_url, &url));
                                            } else {
                                                url_list.push(format!("{}/{}", &proxy_url, &url));
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
                        let mut text = String::new();
                        text += format!("震央地點：{} {}\n", i.elocation, i.edegree).as_str();
                        text += format!("時間：{} {}", i.name, i.etime).as_str();
                        if bot.send_message(url_list, &text) == true {
                            db.add(&keyname);
                        }
                    }
                }
            }
            _ => {}
        }
        let ncree = client.fetch_ncree();
        match ncree {
            Some(r) => {
                let mut text = String::new();
                for data in r {
                    text = format!("地震深度：{}\n", data.depth);
                    text += format!("地震強度：芮氏 規模{}\n", data.magnitude).as_str();
                    text += format!("圖表簡述：{}\n", data.detail).as_str();
                    text += format!("發生時間：{}\n\n", data.datetime).as_str();

                    let eqno = data.eq_no;
                    if !db.query(eqno.as_str()) {
                        // https://seaport.ncree.org/eq_data/ASCII/113489/TSHAKEMAP/TIF/113489_PGA.png
                        // https://seaport.ncree.org/eq_data/ASCII/113489/TSHAKEMAP/TIF/113489_PGV.png
                        let url_list = vec![
                            format!("https://seaport.ncree.org/eq_data/ASCII/{}/TSHAKEMAP/TIF/{}_PGA.png", eqno, eqno),
                            format!("https://seaport.ncree.org/eq_data/ASCII/{}/TSHAKEMAP/TIF/{}_PGV.png", eqno, eqno),
                        ];
                        let ncree_text = format!(
                            "{}\n圖表資源來自 [國家地震工程研究中心](https://ncree.org/)",
                            &text
                        );
                        if bot.send_message(url_list, &ncree_text) == true {
                            println!("寫入資料 {}", &eqno);
                            db.add(&eqno);
                        }
                    }
                    if !db.query(data.timestamp.as_str()) {
                        // https://scweb.cwa.gov.tw/zh-tw/earthquake/details/2024110100181955487
                        let url = format!(
                            "https://scweb.cwa.gov.tw/zh-tw/earthquake/details/{}",
                            data.timestamp
                        );
                        match reqwest::blocking::get(&url) {
                            Ok(r) => {
                                let document = Html::parse_document(&r.text().unwrap());
                                let style_selector = Selector::parse("style").unwrap();
                                let pattern = Regex::new(r#"url\(['"]*([^'"\)]+)['"]*\)"#).unwrap();
                                let mut img_list = vec![];
                                for style_element in document.select(&style_selector) {
                                    let style_content = style_element.text().collect::<String>();
                                    for cap in pattern.captures_iter(&style_content) {
                                        // https://scweb.cwa.gov.tw/webdata/drawTrace/outcome/2024/2024489/4-FULB.gif
                                        // => /webdata/drawTrace/outcome/2024/2024487/4-ESL.gif

                                        if let Some(url) = cap.get(1) {
                                            match Url::parse(
                                                format!(
                                                    "https://scweb.cwa.gov.tw/{}",
                                                    url.as_str()
                                                )
                                                .as_str(),
                                            ) {
                                                Ok(url) => {
                                                    img_list.push(url.to_string());
                                                }
                                                Err(_) => {
                                                    println!("地動震波圖網址擷取失敗")
                                                }
                                            }
                                        }
                                    }
                                }
                                let ncree_text = format!(
                                    "{}\n圖表資源來自 [中央氣象署](https://ncree.org/)",
                                    &text
                                );
                                if bot.send_message(img_list, &ncree_text) == true {
                                    db.add(data.timestamp.as_str());
                                }
                            }
                            Err(_) => {}
                        }
                    }
                }
            }
            _ => {}
        }
        thread::sleep(time::Duration::from_secs(60));
    }
}
