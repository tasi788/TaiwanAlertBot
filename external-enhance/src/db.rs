use pickledb::{PickleDb, PickleDbDumpPolicy, SerializationMethod};
use std::path::Path;

pub struct DB {
    db: PickleDb,
}

impl DB {
    pub fn new() -> Self {
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

    pub fn query(&self, q: &str) -> bool {
        self.db.get::<bool>(q).unwrap_or(false)
    }

    pub fn add(&mut self, q: &str) -> bool {
        self.db.set(q, &true).unwrap();
        println!("已寫入 {}", &q);
        true
    }
}
