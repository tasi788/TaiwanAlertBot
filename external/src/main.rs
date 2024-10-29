use core::option::Option;
use reqwest::Url;
use serde::{Deserialize, Serialize};
use chrono::{Utc};


struct NCDR {
    base_url: Url,
}

impl NCDR {
    fn new() -> Self {
        NCDR {
            base_url: Url::parse("https://satis.ncdr.nat.gov.tw/eqsms/data/eqlist.txt").unwrap(),
        }
    }

    fn fetch(self) -> Option<Vec<EQList>> {
        //  https://satis.ncdr.nat.gov.tw/eqsms/data/eqlist.txt?_dc=1730189712207&page=1&start=0&limit=25
        //  1730189712207
        // 1730191175745
        //  1730191144
        //  1730191194813014
        let binding = Utc::now().timestamp_subsec_millis().to_string();
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
    let client = NCDR::new();
    let f = client.fetch();
    // https://satis.ncdr.nat.gov.tw/eqsms/data/Eq20241027_1419_P1.png
}
