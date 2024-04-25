export interface TelegramMethods {
    sendMessage(chatId: number, text: string, topic: number): Promise<number>;
    sendPhoto(chatId: number, photo: string, caption: string, topic: number): Promise<number>;
    sendMediaGroup(chat_id: number, media: string[], caption: string, topic: number): Promise<number>;
    copyMessage(chat_id: number, from_chat_id: number, message_id: number, topic: number): Promise<void>;
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
    
    async copyMessages(chat_id: number, from_chat_id: number, message_id: number, topic: number): Promise<void> {
        const data = JSON.stringify({
            chat_id: chat_id,
            from_chat_id: from_chat_id,
            message_ids: [message_id, message_id + 1],
            message_thread_id: topic
        });
        let r = await fetch(this.url + '/copyMessages', {
            ...this.payload,
            body: data
        })
        let resp = await r.json() as TelegramResonse
    }

    async sendMessage(chatId: number, text: string, topic: number): Promise<number> {
        // Implementation code for sending a message using this.token
        const data = JSON.stringify({
            chat_id: chatId,
            text,
            topic
        });
        let r = await fetch(this.url + '/sendMessage', {
            ...this.payload,
            body: data
        })
        let resp = await r.json() as TelegramResonse
        return resp.result[0].message_id
    }

    async sendMediaGroup(chatId: number, photo: string[], caption: string, topic: number): Promise<number> {
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
        let r = await resp.json() as TelegramResonse
        console.log(r)
        return r.result[0].message_id
    }

    async sendPhoto(chatId: number, photo: string, caption: string): Promise<void> {
        // Implementation code for sending a photo using this.token
    }


    async sendDocument(chatId: number, document: string, caption: string): Promise<void> {
        // Implementation code for sending a document using this.token
    }
}

export interface TelegramResonse {
    ok:     boolean;
    result: Result[];
}

export interface Result {
    message_id:        number;
    from:              From;
    chat:              Chat;
    date:              number;
    media_group_id:    string;
    photo:             Photo[];
    caption?:          string;
    caption_entities?: CaptionEntity[];
}

export interface CaptionEntity {
    offset: number;
    length: number;
    type:   string;
}

export interface Chat {
    id:       number;
    title:    string;
    username: string;
    is_forum: boolean;
    type:     string;
}

export interface From {
    id:         number;
    is_bot:     boolean;
    first_name: string;
    username:   string;
}

export interface Photo {
    file_id:        string;
    file_unique_id: string;
    file_size:      number;
    width:          number;
    height:         number;
}
