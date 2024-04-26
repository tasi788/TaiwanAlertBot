use reqwest;
use std::fs;
use glob::glob;


fn main() {
    // let file_path = "./data";
    let debug_path = std::env::var("DEBUG_PATH").expect("DEBUG_PATH not set");
    let filelist =  glob("./data/*.cap").expect("Failed to read glob pattern");
    
    for entry in filelist {
        println!("{:?}", entry);
        match entry {
            Ok(path) => {
                let url = format!("http://localhost:8787/{}", debug_path);
                if let Ok(file) = fs::read_to_string(&path) {
                    let resp = reqwest::blocking::Client::new()
                        .post(url)
                        .body(file)
                        .send();
                    match resp {
                        Ok(r) => {
                            if r.status().is_success() {
                                println!("{}", r.text().unwrap());
                            } else {
                                println!("Failed: {:?}", path);
                            }
                        },
                        Err(e) => println!("{:?}", e),
                    
                    }
                } else {
                    println!("Failed to read file: {:?}", path);
                }
            },
            Err(e) => println!("{:?}", e),
        }
    }
    
    
}
