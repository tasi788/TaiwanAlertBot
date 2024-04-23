export interface TelegramMethods {
    sendMessage(chatId: number, text: string, topic: number): Promise<void>;
    sendPhoto(chatId: number, photo: string, caption: string): Promise<void>;
    sendDocument(chatId: number, document: string, caption: string): Promise<void>;
}

export class Telegram implements TelegramMethods {
    private token: string;
    private url: string = 'https://api.telegram.org/bot';
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
            // parse_mode,
            topic
        });
        await fetch(this.url + '/sendMessage', {
            ...this.payload,
            body: data
        })
    }

    async sendPhoto(chatId: number, photo: string, caption: string): Promise<void> {
        // Implementation code for sending a photo using this.token
    }

    async sendDocument(chatId: number, document: string, caption: string): Promise<void> {
        // Implementation code for sending a document using this.token
    }
}