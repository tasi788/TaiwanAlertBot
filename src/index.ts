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
	DEBUG_PATH: string,
	CHATID: number;
}


export default {
	async fetch(request: Request, env: Env, ctx: ExecutionContext) {
		const kaomojis = ['(๑•́ ₃ •̀๑)', '(´_ゝ`)', '（’へ’）', '(눈‸눈)', '╮(′～‵〞)╭', '｡ﾟヽ(ﾟ´Д`)ﾉﾟ｡', 'L(　；ω；)┘三└(；ω；　)」', 'ヾ(;ﾟ;Д;ﾟ;)ﾉﾞ', '(◓Д◒)✄╰⋃╯'];
		const randomKaomoji = kaomojis[Math.floor(Math.random() * kaomojis.length)];
		const url = new URL(request.url);

		//  擋掉手賤的人
		if (request.method !== 'POST' || ![`/${env.WEBHOOK_PATH}`, `/${env.DEBUG_PATH}`].includes(url.pathname)) {
			return new Response(randomKaomoji);
		}

		const body = await request.text();
		let report = await this.parse(env, body);
		
		let context = await this.broadcast(env, report, url.pathname === `/${env.DEBUG_PATH}`);
		if (url.pathname === `/${env.DEBUG_PATH}`) {
			return new Response(context?.text);
		}
		return new Response('<?xml version=\"1.0\" encoding=\"utf-8\" ?> <Data><Status>True</Status></Data>');
	},

	async broadcast(env: Env, report: AlertRoot, debug: boolean = false): Promise < void | GeneratorText >{
		const bot = new Telegram(env.BOTTOKEN);
		const gather = 1882;
		const topicList = {
			"category": {
				"Health": 1423,
				"Geo": 1439,
				"Met": 1928,
				"Infra": 2546
			},
			// 獨立 topics
			"event": {
				"地震": 678,
				"市話通訊中斷": 2541,
				"行動電話中斷": 2541
			}
		}
		let text = "";
		let msg_id = 0;
		let context: GeneratorText;
		let info = Array.isArray(report.alert.info) ? report.alert.info[0] : report.alert.info;
		console.log(info.event)
		//  先發到所有警報區 
		switch (info.event) {
			case '地震':
				context = await earthquake(report)
				if (debug) {return context}
				msg_id = await bot.sendMediaGroup(env.CHATID, context.image, context.text, gather)
				break;

			default:
				context = await defaultgen(report)
				if (debug) {return context}
				msg_id = await bot.sendMessage(env.CHATID, context.text, gather)
		}

		let topic_copylist: number[] = [];
		for (let category in topicList.category) {
			if (category === info.category) {
				let topic: number = topicList.category[category as keyof typeof topicList.category];
				topic_copylist.push(topic);
			}
		}

		for (let event in topicList.event) {
			if (event === info.event) {
				let topic: number = topicList.event[event as keyof typeof topicList.event];
				topic_copylist.push(topic);
			}
		}
		
		//  批次複製訊息
		for (let target_topics of topic_copylist) {
			if (context.image.length > 0) {
				//  地震圖
				await bot.copyMessages(env.CHATID, env.CHATID, [msg_id, msg_id + 1], target_topics)
			} else {
				await bot.copyMessages(env.CHATID, env.CHATID, [msg_id], target_topics)
			}
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