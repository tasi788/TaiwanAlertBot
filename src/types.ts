import { DateTime } from 'luxon';

export interface AlertRoot {
    alert: Alert;
}

export interface Alert {
    identifier: string;
    sender:     string;
    sent:       DateTime;
    status:     string;
    msgType:    string;
    scope:      string;
    info:       Info[] | Info;
    _xmlns:     string;
}

export interface Info {
    language:     string;
    category:     string;
    event:        string;
    responseType: string;
    urgency:      string;
    severity:     string;
    certainty:    string;
    eventCode:    EventCode;
    effective:    DateTime;
    onset:        DateTime;
    expires:      DateTime;
    senderName:   string;
    headline:     string;
    description:  string;
    web:          string;
    parameter:    EventCode[];
    resource:    Resource[];
    area:         Area[];
}

export interface Area {
    areaDesc: string;
    geocode?: EventCode[] | EventCode;
}

export interface EventCode {
    valueName: ValueName | string;
    value:     string;
}

export enum ValueName {
    AlertColor = "alert_color",
    AlertTitle = "alert_title",
    ProfileCAPTWPEvent10 = "profile:CAP-TWP:Event:1.0",
    SeverityLevel = "severity_level",
    TaiwanGeocode103 = "Taiwan_Geocode_103",
    WebsiteColor = "website_color",
}

export interface Resource {
    resourceDesc: string;
    mimeType:     string;
    uri:          string;
}


export interface GeneratorText {
    text: string;
    image: string[];
}

export class GeneratorText implements GeneratorText {
    constructor(text: string, image: string[]) {
        this.text = text;
        this.image = image;
    }
}