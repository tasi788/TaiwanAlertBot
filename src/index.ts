import {
	XMLParser
} from 'fast-xml-parser';
import {
	AlertRoot,
	GeneratorText
} from './types';

import {
	Telegram
} from './telegram';
import {
	ExecutionContext
} from '@cloudflare/workers-types/experimental';
import {
	earthquake
} from './generator/earthquake';
import {
	defaultgen
} from './generator/defaultgen';

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
				"Met": 1928,
			},
			// 獨立 topics
			"event": {
				"地震": 678
			}
		}
		let text = "";
		let msg_id = 0;
		let context: GeneratorText;
		//  先發到所有警報區 
		switch (report.alert.info.event) {
			case '地震':
				context = await earthquake(report)
				msg_id = await bot.sendMediaGroup(env.CHATID, context.image, context.text, gather)

			default:
				context = await defaultgen(report)
				msg_id = await bot.sendMessage(env.CHATID, context.text, gather)
		}

		let topic_copylist: number[] = [];
		for (let category in topicList.category) {
			if (category === report.alert.info.category) {
				let topic: number = topicList.category[category as keyof typeof topicList.category];
				topic_copylist.push(topic);
			}
		}

		for (let event in topicList.event) {
			if (event === report.alert.info.event) {
				let topic: number = topicList.event[event as keyof typeof topicList.event];
				topic_copylist.push(topic);
			}
		}

		console.log(topic_copylist)
		console.log(msg_id)
		
		//  批次複製訊息
		for (let target_topics of topic_copylist) {
			if (context.image.length > 0) {
				//  地震圖
				await bot.copyMessages(env.CHATID, env.CHATID, [msg_id, msg_id + 1], target_topics)
			}
			await bot.copyMessage(env.CHATID, env.CHATID, msg_id, target_topics)
		}
	},

	async parse(env: Env, context: string): Promise < AlertRoot > {
		const parser = new XMLParser({
			tagValueProcessor: (attrName, val) => {
				if (['effective', 'onset', 'expires'].includes(attrName) === true) {
					return new Date(val);
				}
				return val;
			}
		});
		return parser.parse(context) as AlertRoot;
	}
};