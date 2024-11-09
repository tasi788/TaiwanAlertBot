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
        `警報發布時間：${info.effective.year}年 ${(info.effective.month)}月 ${info.effective.day}日 ${String(info.effective.hour).padStart(2, '0')}:${String(info.effective.minute).padStart(2, '0')}\n` +
        `警報過期時間：${info.expires.year}年 ${(info.expires.month)}月 ${info.expires.day}日 ${String(info.expires.hour).padStart(2, '0')}:${String(info.expires.minute).padStart(2, '0')}\n\n`
    return new GeneratorText(text, []);
}