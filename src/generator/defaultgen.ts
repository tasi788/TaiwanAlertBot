import {
    AlertRoot,
    GeneratorText
} from '../types';

export async function defaultgen(report: AlertRoot): Promise < GeneratorText > {
    let info = Array.isArray(report.alert.info) ? report.alert.info[0] : report.alert.info
    let color = ''
    try {
        color = info.parameter.map((p) => p.valueName === 'alert_color' ? p.value : '').join('')
        if (color === '') {
            color = info.parameter.map((p) => p.valueName === 'alert_title' ? p.value : '').join('')
        }
    } catch (e) {
        color = '未知'
    }

    let text = `發布單位：#${info.senderName}\n` +
        `警報活動：#${info.event}\n` +
        `警報顏色：#${color}\n` +
        `警報標題：${info.headline}\n\n` +
        `警報描述：${info.description}\n\n` +
        `警報發布時間：${info.effective.getFullYear()}年 ${(info.effective.getMonth() + 1)}月 ${info.effective.getDate()}日 ${info.effective.getHours()}:${info.effective.getMinutes()}\n` +
        `警報過期時間：${info.expires.getFullYear()}年 ${(info.expires.getMonth() + 1)}月 ${info.expires.getDate()}日 ${info.expires.getHours()}:${info.expires.getMinutes()}\n\n`
    return new GeneratorText(text, []);
}