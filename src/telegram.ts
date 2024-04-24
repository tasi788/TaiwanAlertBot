export interface TelegramMethods {
    sendMessage(chatId: number, text: string, topic: number): Promise<void>;
    sendPhoto(chatId: number, photo: string, caption: string, topic: number): Promise<void>;
    sendMediaGroup(chat_id: number, media: string[], caption: string, topic: number): Promise<void>;

}

export interface InputMediaPhoto {
    type: string;
    media: string;
    caption?: string;
    parse_mode?: string;
}

export class Telegram implements TelegramMethods {
    private token: string;
    private url: string = 'https://api.trashgr.am/bot';
    private payload: object = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    };

    constructor(token: string) {
        this.token = token;
        this.url += token;
    }

    async sendMessage(chatId: number, text: string, topic: number): Promise<void> {
        // Implementation code for sending a message using this.token
        const data = JSON.stringify({
            chat_id: chatId,
            text,
            topic
        });
        await fetch(this.url + '/sendMessage', {
            ...this.payload,
            body: data
        })
    }

    async sendMediaGroup(chatId: number, photo: string[], caption: string, topic: number): Promise<void> {
    // Implementation code for sending a media group using this.token
        let media: InputMediaPhoto[] = [{
            type: 'photo',
            media: photo[0],
            caption,
            parse_mode: 'html'
        }];
        if (photo.length > 1) {
            for (let i = 1; i < photo.length; i++) {
                media.push({
                    type: 'photo',
                    media: photo[i],
                });
            }
        }
        
        const data = JSON.stringify({
            chat_id: chatId,
            media: media,
            message_thread_id: topic
        });
        let resp = await fetch(this.url + '/sendMediaGroup', {
            ...this.payload,
            body: data
        })
        console.log(await resp.text())
    }

    async sendPhoto(chatId: number, photo: string, caption: string): Promise<void> {
        // Implementation code for sending a photo using this.token
    }


    async sendDocument(chatId: number, document: string, caption: string): Promise<void> {
        // Implementation code for sending a document using this.token
    }
}