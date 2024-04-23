import { XMLParser } from 'fast-xml-parser';
import { AlertRoot } from './types';

import { Telegram } from './telegram';

export interface Env {
	BOTTOKEN: string;
	WEBHOOK_PATH: string;
	CHATID: number;
}


export default {
	async fetch(request: Request, env: Env, ctx: ExecutionContext) {
		const kaomojis = ['(๑•́ ₃ •̀๑)', '(´_ゝ`)', '（’へ’）', '(눈‸눈)', '╮(′～‵〞)╭', '｡ﾟヽ(ﾟ´Д`)ﾉﾟ｡', 'L(　；ω；)┘三└(；ω；　)」', 'ヾ(;ﾟ;Д;ﾟ;)ﾉﾞ', '(◓Д◒)✄╰⋃╯'];
		const randomKaomoji = kaomojis[Math.floor(Math.random() * kaomojis.length)];
		const url = new URL(request.url);

		//  擋掉手賤的人
		if (request.method !== 'POST' || url.pathname != `/${env.WEBHOOK_PATH}`) {
			return new Response(randomKaomoji);
		}
		
		const body = await request.text();
		let alert = await this.parse(env, body);
		await this.broadcast(env, alert);
		return new Response('ok');
	},

	async broadcast(env: Env, alert: AlertRoot) {
		const bot = new Telegram(env.BOTTOKEN);
		
		// const bot = new Telegraf(env.BOTTOKEN)
		let text = "喵喵測試\n" +
				   `${alert.alert.info.event}`

		await bot.sendMessage(env.CHATID, text)
	},

	async parse(env: Env, context: string): Promise<AlertRoot> {
		const parser = new XMLParser();
		return parser.parse(context) as AlertRoot;
	}
};