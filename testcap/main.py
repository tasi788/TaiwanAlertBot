import httpx
from httpx import URL
import asyncio
import json
import pathlib

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError


class NCDR:
    def __init__(self) -> None:
        self.url = "https://alerts.ncdr.nat.gov.tw/calamityAlertSearch_history.aspx/QueryDetail"
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
        self.client = httpx.AsyncClient()
        self.path = pathlib.Path("./data")

    async def fetch(self, issue_id: str):
        data = {
            "QueryTemp": json.dumps(
                {
                    "LiveCategory": "all",
                    "IssueID": f"{issue_id}",
                    "AlertTypeID": "all",
                    "AlertDate": "2025-08-19",
                    "ddlSentdate": "1",
                    "CountyID": "all",
                    "CountyName": "all",
                    "TownName": "all",
                    "Sort": None,
                    "Days": "7",
                    "PageCount": 10,
                    "PageIndex": 1,
                }
            )
        }

        response = await self.client.post(self.url, headers=self.headers, json=data)
        try:
            row = json.loads(response.json()["d"])
        except json.JSONDecodeError:
            print("json decode error...")
            print(response.text)
            return

        for i in row:
            url = URL(i["FilePath"])
            filename = url.path.split("/")[-1]

            r = await self.client.get(url.__str__())
            if not r.text.startswith('<?xml'):
                print("bad xml...", filename)
                continue

            print("writing file...", filename)
            self.path.joinpath(filename).write_bytes(r.content)


if __name__ == "__main__":
    n = NCDR()
    asyncio.run(n.fetch("2"))
