export interface Env {
	BOTTOKEN: string;
	WEBHOOK_PATH: string;
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
		return new Response('ok');
		

	},
};