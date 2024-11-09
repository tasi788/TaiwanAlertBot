import {
    AlertRoot, GeneratorText
} from '../types';

export async function earthquake(report: AlertRoot): Promise<GeneratorText> {
    let info = Array.isArray(report.alert.info) ? report.alert.info[0] : report.alert.info
    let depth = info.parameter.map((p) => p.valueName === 'EventDepth' ? p.value : '').join('').replace("公里", " 公里")
    let magnitude = info.parameter.map((p) => p.valueName === 'EventMagnitudeDescription' ? p.value : '').join('').replace("規模", " 規模")

    let text = `發布單位：#${info.senderName}\n` +
        `震央位置：${info.parameter.map((p) => p.valueName === 'EventLocationName' ? p.value : '').join('')}\n` +
        `地震深度：${depth}\n` +
        `地震強度：${magnitude}\n` +
        `警報簡述：${info.description}\n\n` +
        `*備註*\n` +
        `相關詳細地震資訊請上<a href=\"${info.web}/\">地震測報中心</a>`

    let img = [
        info.resource.map((r) => r.resourceDesc === '地震報告圖' ? r.uri : '').join('') + '?ts=' + String(Date.now()),
        info.resource.map((r) => r.resourceDesc === '等震度圖' ? r.uri : '').join('') + '?ts=' + String(Date.now())
    ]

    return new GeneratorText(text, img);
}

