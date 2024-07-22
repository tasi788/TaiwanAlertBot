import { DateTime } from "luxon";
import sharp from "sharp";

let timezone = "Asia/Taipei";

export async function temp(): Promise <Array<string>> {
    let time = DateTime.local().setZone(timezone)
    let date = time.toFormat('yyyy-MM-dd')
    
    let images = []
    //  2024-07-22_1500.GTP8.jpg
    for (let i = 0; i < time.hour; i++) {
        let hour = time.set({ hour: i, minute: 0 }).toFormat('HHmm')
        let url = `https://www.cwa.gov.tw/Data/temperature/${date}_${hour}.GTP8.jpg`
        images.push(url)
    }
    return images
}


export async function makeGIF() {
    let images_url = await temp()
    let images = []
    
    images_url.forEach((url) => {
        // download and push to images
    })

    // const image = sharp(images {
    //     animated: true,
    //   })
    //     .gif({ loop: 0 })
    //     .toBuffer();
    

    

}
