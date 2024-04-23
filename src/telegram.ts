export interface TelegramMethods {
    sendMessage(chatId: number, text: string, parse_mode: string): Promise<void>;
    sendPhoto(chatId: number, photo: string, caption: string): Promise<void>;
    sendDocument(chatId: number, document: string, caption: string): Promise<void>;
}

export class Telegram implements TelegramMethods {
    private token: string;
    private url: string = 'https://api.telegram.org/bot';

    constructor(token: string) {
        this.token = token;
        this.url += token;
    }

    async sendMessage(chatId: number, text: string, parse_mode: string|null = null): Promise<void> {
        // Implementation code for sending a message using this.token
    }

    async sendPhoto(chatId: number, photo: string, caption: string): Promise<void> {
        // Implementation code for sending a photo using this.token
    }

    async sendDocument(chatId: number, document: string, caption: string): Promise<void> {
        // Implementation code for sending a document using this.token
    }
}