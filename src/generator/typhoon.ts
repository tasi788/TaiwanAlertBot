import {
    AlertRoot, GeneratorText
} from '../types';

import { DateTime } from 'luxon';

export async function typhoon(report: AlertRoot): Promise<GeneratorText> {
    let tyinfo = report as unknown as TyphoonAlert;
    let info = tyinfo.alert.info;
    let text = "";
    tyinfo.alert.info.description['typhoon-info'].section.forEach((section: any) => {
        switch (section.title) {
            case "警報報數":
                text += `報數：第 ${section.text} 報\n`;
                break;
            case "颱風資訊":
                text += `命名：（${section.typhoon_name}）${section.cwa_typhoon_name} #`;
                section.analysis.scale.forEach((scale: any) => {
                    if (scale.lang == "zh-TW") { text += scale.text}
                });
                text += "\n"
        }
    });
    tyinfo.alert.info.description.section.forEach((section: any) => {
        switch (section.title) {
            case "颱風動態":
                text += `動態：${section.text}\n`;
                break;
            case "移速與預測":
                text += `移速與預測：${section.text}\n`;
                break;
            case "警戒區域及事項":
                text += `⚠️ 警戒區域及事項：\n${section.text}\n`
                break;
            case "注意事項":
                text += `🚨 注意事項：\n${section.text}\n`
        }
    });
    text += `\n警報發布時間：${info.effective.year}年 ${(info.effective.month)}月 ${info.effective.day}日 ${String(info.effective.hour).padStart(2, '0')}:${String(info.effective.minute).padStart(2, '0')}\n`
    return new GeneratorText(text, []);
}

export interface TyphoonAlert {
    alert: Alert;
}

export interface Alert {
    identifier: string;
    sender: string;
    sent: DateTime;
    status: string;
    msgType: string;
    scope: string;
    references: string;
    info: Info;
    _xmlns: string;
}

export interface Info {
    language: string;
    category: string;
    event: string;
    responseType: string;
    urgency: string;
    severity: string;
    certainty: string;
    eventCode: EventCode;
    effective: DateTime;
    onset: DateTime;
    expires: DateTime;
    senderName: string;
    headline: string;
    description: Description;
    web: string;
    parameter: EventCode[];
    area: Area[];
}

export interface Area {
    areaDesc: string;
    polygon?: string;
    geocode?: EventCode;
}

export interface EventCode {
    valueName: string;
    value: string;
}

export interface Description {
    "typhoon-info": TyphoonInfo;
    section: DescriptionSection[];
}

export interface DescriptionSection {
    title: string;
    __text: string;
}

export interface TyphoonInfo {
    section: TyphoonInfoSection[];
}

export interface TyphoonInfoSection {
    title: string;
    __text?: string;
    typhoon_name?: string;
    cwa_typhoon_name?: string;
    analysis?: Analysis;
    prediction?: Analysis;
}

export interface Analysis {
    time: DateTime;
    position: string;
    max_winds: Gust;
    gust: Gust;
    pressure: Gust;
    radius_of_15mps: Gust;
    scale?: Scale[];
}

export interface Gust {
    _unit: string;
    __text: string;
}

export interface Scale {
    _lang: string;
    __text: string;
}
