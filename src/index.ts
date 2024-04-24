import { XMLParser } from 'fast-xml-parser';
import { AlertRoot } from './types';

import { Telegram } from './telegram';
import { ExecutionContext } from '@cloudflare/workers-types/experimental';
import { earthquake } from './generator/earthquake';

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
		return new Response('<?xml version=\"1.0\" encoding=\"utf-8\" ?> <Data><Status>True</Status></Data>');
	},

	async broadcast(env: Env, report: AlertRoot) {
		const bot = new Telegram(env.BOTTOKEN);
		const gather = 1882;
		const topicList = {
			"category": {
				"Health": 1423,
				"Geo": 1439,
			},
			"event": {
				"地震": 678
			}
		}
		let text = "";
		let msg_id = 0;
		switch (report.alert.info.event) {
			case '地震':
				let context = await earthquake(report)
				msg_id = await bot.sendMediaGroup(env.CHATID, context.image, context.text, gather)
				
			default:
				break;
		}
		for (let category in topicList.category) {
			if (category === report.alert.info.category) {
				let topic: number = topicList.category[category as keyof typeof topicList.category];
				await bot.copyMessage(env.CHATID, env.CHATID, msg_id, topic)
			}
		}

		for (let event in topicList.event) {
			if (event === report.alert.info.event) {
				let topic: number = topicList.event[event as keyof typeof topicList.event];
				await bot.copyMessage(env.CHATID, env.CHATID, msg_id, topic)
			}
		}
		

		// await bot.sendMessage(env.CHATID, text, 1);
	},

	async parse(env: Env, context: string): Promise<AlertRoot> {
		const parser = new XMLParser();
		return parser.parse(context) as AlertRoot;
	}
};