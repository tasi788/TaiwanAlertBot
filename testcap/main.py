import httpx
import asyncio
import json
import pathlib
from yarl import URL


class NCDR:
    def __init__(self) -> None:
        self.url = "https://alerts.ncdr.nat.gov.tw/calamityAlertSearch_history.aspx/QueryDetail"
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
        self.client = httpx.AsyncClient()
        self.path = pathlib.Path("./")

    async def fetch(self, issue_id: str):
        data = {
            "QueryTemp": json.dumps(
                {
                    "LiveCategory": "all",
                    "IssueID": f"{issue_id}",
                    "AlertTypeID": "all",
                    "AlertDate": "2024-01-01",
                    "ddlSentdate": "1",
                    "CountyID": "all",
                    "CountyName": "all",
                    "TownName": "all",
                    "Sort": None,
                    "Days": "30",
                    "PageCount": 10,
                    "PageIndex": 1,
                }
            )
        }
        # print(data)
        response = await self.client.post(self.url, headers=self.headers, json=data)
        row = json.loads(response.json()["d"])
        for i in row:
            url = URL(i["FilePath"])

            r = await self.client.get(url.__str__())
            filename = url.parts[-1]
            print("writing file...", filename)
            self.path.joinpath(filename).write_bytes(r.content)


if __name__ == "__main__":
    n = NCDR()
    asyncio.run(n.fetch("2"))
