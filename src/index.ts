import { XMLParser } from 'fast-xml-parser';
import { AlertRoot } from './types';

import { Telegram } from './telegram';
import { ExecutionContext } from '@cloudflare/workers-types/experimental';

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
		let report = await this.parse(env, body);
		await this.broadcast(env, report);
		return new Response('ok');
	},

	async broadcast(env: Env, report: AlertRoot) {
		const bot = new Telegram(env.BOTTOKEN);
		const topicList = {
			"category": {
				"Health": 1423,
				"Geo": 1439,
			},
			"event": {
				"降雨": 123
			}
			
		}
		let text = `發布單位：#${report.alert.info.senderName}\n` +
				   `警報活動：#${report.alert.info.event}\n` +
				   `警報顏色：還沒寫\n` +
				   `警報標題：${report.alert.info.headline}\n` +
				   `警報描述：${report.alert.info.description}\n`

		// await bot.sendMessage(env.CHATID, text, 1);
	},

	async parse(env: Env, context: string): Promise<AlertRoot> {
		const parser = new XMLParser();
		return parser.parse(context) as AlertRoot;
	}
};