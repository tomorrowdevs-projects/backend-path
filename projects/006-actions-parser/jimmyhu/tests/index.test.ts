import * as storyFunction from '../index';



test('Test Function parsing Json file', () => {
    let sunsetStory: object = {
        "actions": [
            {
            "type": "HTTPRequestAction",
            "name": "location",
            "options": {
                "url": "http://free.ipwhois.io/json/"
            }
            },
            {
            "type": "HTTPRequestAction",
            "name": "sunset",
            "options": {
                "url": "https://api.sunrise-sunset.org/json?lat={{location.latitude}}&lng={{location.longitude}}"
            }
            },
            {
            "type": "PrintAction",
            "name": "print",
            "options": {
                "message": "Sunset in {{location.city}}, {{location.country}} is at {{sunset.results.sunset}}."
            }
            }
        ]
    }
    expect(storyFunction.jsonParser('sunset.json')).toStrictEqual(sunsetStory);
})

test('Test Functions moustacheChecker', () => {
    let result: object[] = [
        {
            "raw": '{{location.city}}',
            "filtered": 'location.city'
        },
        {
            "raw": '{{location.latitude}}',
            "filtered": 'location.latitude'
        },
        {
            "raw": '{{location.longitude}}',
            "filtered": 'location.longitude'
        },
        {
            "raw": '{{sunset.results.sunset}}',
            "filtered": 'sunset.results.sunset'
        }
    ]
    expect(storyFunction.moustacheChecker("https://api.sunrise-sunset.org/json?city={{location.city}}&lat={{location.latitude}}&lng={{location.longitude}}&sunset={{sunset.results.sunset}}")).toStrictEqual(result);
})

test('Test Functions moustacheReplace', () => {
    let toSobstitute: storyFunction.IRegx[] = [
        {
            "raw": '{{location.city}}',
            "filtered": 'location.city'
        },
        {
            "raw": '{{location.latitude}}',
            "filtered": 'location.latitude'
        },
        {
            "raw": '{{location.longitude}}',
            "filtered": 'location.longitude'
        },
    ]
    let url: string = "https://api.sunrise-sunset.org/json?city={{location.city}}&lat={{location.latitude}}&lng={{location.longitude}}"
    let names: storyFunction.Inames<storyFunction.Inames<string|number>> = {
        "location": {
            "latitude": 1.1234567,
            "longitude": 1.1238567,
            "city": "London"
        }
    }
    let expectedURL = "https://api.sunrise-sunset.org/json?city=London&lat=1.1234567&lng=1.1238567"
    expect(storyFunction.moustacheReplace(url,toSobstitute,names)).toStrictEqual(expectedURL);
})

