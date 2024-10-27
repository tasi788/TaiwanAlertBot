use reqwest::Url;
use serde::Deserialize;
use serde::Serialize;

struct NCDR {
    url: Url,
}

impl NCDR {
    fn new() -> Self {
        NCDR {
            url: Url::parse("https://satis.ncdr.nat.gov.tw/eqsms/data/eqlist.txt").unwrap(),
        }
    }

    fn fetch(self) {
        match reqwest::blocking::get(self.url.as_str()) {
            Ok(r) => {
                println!("{:?}", r);
            }
            Err(_) => {
                println!("Fail");
            }
        }
    }
}

// #[derive(Default, Debug, Clone, PartialEq, Serialize, Deserialize)]
// #[serde(rename_all = "camelCase")]
// pub struct EQList {
//     pub name: String,
//     pub etime: String,
//     pub file1: String,
//     pub file2: String,
//     pub file3: String,
//     pub file4: String,
//     pub file5: String,
//     pub file6: String,
//     pub file7: String,
//     pub elocation: String,
//     pub edegree: String,
// }

fn main() {
    let client = NCDR::new();
    client.fetch();
    println!("Hello, world!");
}
