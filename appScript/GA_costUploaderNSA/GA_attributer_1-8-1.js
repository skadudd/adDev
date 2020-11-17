//app-script
//GA api sheet 기반으로 작동하는 코드.

const dataSource = {
    "GOAL1_B": "RFQ_sourceAndCampaignPath",
    "GOAL3_B": "clickTru_sourceAndCampaignPath"
};
const dataSheet = {
    "GOAL1_B": "RFQ_sourceAndCampaignPath",
    "GOAL3_B": "clickTru_sourceAndCampaignPath"
}

let DATA_BASE = {};

function init() {
    for (v in dataSource) {
        let dataSourceName = dataSource[v]
        Logger.log("get Data from : " + dataSourceName)
        let pathData = getRawData(dataSourceName)
        if (pathData == null) {
            Logger.log('no conversion of ' + v)
            continue
        } else {

            runModel(pathData)

            let df = setDataFrame()

            appendDataToDB(df, dataSourceName)
            DATA_BASE = {}
        }
    }

    Logger.log('DB update complete')

};

function getRawData(dataSourceName) {
    var sheetActive = SpreadsheetApp.openById("1QosgdW1OlyY9Opte0o5jJbfUc9mdw1Lu8cvUGiCAoEk");
    var sheet = sheetActive.getSheetByName(dataSourceName);
    let pathData = sheet.getRange(`A16:D${sheet.getLastRow()}`).getValues();

    let nonScoreIdentifier = sheet.getRange('A16').getValues()

    Logger.log(nonScoreIdentifier)
    if (nonScoreIdentifier[0][0] == '') {
        return null
    } else {
        return pathData;
    }
}
/**
function getDB(d){
  var sheetActive = SpreadsheetApp.openById("1xue5bi12TqxqtSnkKuANfPlJZTPEXJyfPn_DC3EeqL0");
  var sheet = sheetActive.getSheetByName("d");
  
  return sheet
}
**/
function replaceCampaignNameNotset(obj) {
    if (obj === '(unavailable)') {
        return obj = '(not set)'
    } else {
        return obj
    }
}

function dividePath(flattenData) {
    let separatedFlattenData = []

    for (v in flattenData) {
        if (typeof flattenData[v] === 'string') {
            let divided = flattenData[v].split('/');
            divided.forEach(function(obj) {
                let objOfData = replaceCampaignNameNotset(obj)
                separatedFlattenData.push(objOfData);
            });
        } else {
            separatedFlattenData.push(flattenData[v])
        }
    }
    return separatedFlattenData
}

function setDataFrame() {
    //오브젝트 펼쳐서 1차원 어레이로 변환
    let df = []

    let objectData = DATA_BASE
    let flattenData = Object.entries(objectData).flat()
    let separatedFlattenData = dividePath(flattenData) //시간,소스,매체 분리
    let b = separatedFlattenData
    let len = b.length

    for (i = 0; i <= len; i++) {
        df.push([b[0], b[1], b[2], b[3]])
        b.shift()
        b.shift()
        b.shift()
        b.shift()
        if (!(b.length)) { break }
    };
    Logger.log("DATAFRAME of request is : ")
    Logger.log(df)
    return df;
};

function appendDataToDB(df, dataSourceName) {

    var sheetActive = SpreadsheetApp.openById("1xue5bi12TqxqtSnkKuANfPlJZTPEXJyfPn_DC3EeqL0");
    var sheet = sheetActive.getSheetByName(dataSourceName);
    let data = df

    Logger.log("number of processed data : " + data.length)

    sheet.getRange(sheet.getLastRow() + 1, 1, data.length, 4).setValues(data);
};

function runModel(pathData) {
    for (i = 0; i < pathData.length; i++) {
        let dateOfConversion = pathData[i][0]
        let sourceOfConversion = pathData[i][1]
        let campaignOfConversion = pathData[i][2]
        let numOfConversion = pathData[i][3]

        doAttribute_181(sourceOfConversion, campaignOfConversion, numOfConversion, dateOfConversion);
    };
    return
};



function doAttribute_181(source, campaign, score, convDate) {
    let date = convertRawDate(convDate)
    let stripSourcePath = source.split(">")
    let stripCampaignPath = campaign.split(">")
    let firstTouchOfCampaign = stripCampaignPath[0].replace(/\s/g, '');
    let lastTouchOfCampaign = stripCampaignPath[stripCampaignPath.length - 1].replace(/\s/g, '');

    if (stripCampaignPath.length == 1) {
        doCal(stripSourcePath, firstTouchOfCampaign, score, date)

    } else if (stripCampaignPath.length == 2) {
        doCal(stripSourcePath, firstTouchOfCampaign, lastTouchOfCampaign, score, date)
    } else if (stripCampaignPath.length >= 3) {
        doCal(stripSourcePath, stripCampaignPath, firstTouchOfCampaign, lastTouchOfCampaign, score, date)

    }
    return
}

function convertRawDate(convDate) {
    let convDate2 = convDate.toString()
    let dateHypen = convDate2.replace(/(\d{4})(\d{2})(\d{2})/, "$1-$2-$3")

    let dateNum = new Date(dateHypen);
    let date = dateNum.toISOString().slice(0, 10).replace(/-/g, "");
    return date;
};

function combineSourceAndPath(sourcePath, campaignPath, date) {
    if (sourcePath.constructor === Array) {
        let combinedPath = []

        for (v in sourcePath) {
            combinedPath.push(date + "/" + sourcePath[v] + "/" + campaignPath[v])
        }
        let mappedCombinedPath = combinedPath.map(function(x) { return x.replace(/\s/g, '') })
        return mappedCombinedPath

    } else {
        return combinedPath = date + "/" + sourcePath + "/" + campaignPath
    }
}

//가변인자함수
function doCal() {
    let date = arguments[arguments.length - 1]

    if (arguments.length == 4) {
        let sourcePath = arguments[0][0]
        let firstTouchOfCampaign = arguments[1]
        let score = arguments[2]
        let combinedPath = combineSourceAndPath(sourcePath, firstTouchOfCampaign, date);

        if (combinedPath in DATA_BASE) {
            DATA_BASE[combinedPath] += score
        } else {
            DATA_BASE[combinedPath] = score
        }
        return
    } else if (arguments.length == 5) {
        //let sourcePath = arguments[0][0].replace(/\s/g, '');
        let firstTouchOfCampaign = arguments[1]
        let lastTouchOfCampaign = arguments[2]
        let score = arguments[3]
        let combinedPath1 = combineSourceAndPath(arguments[0][0].replace(/\s/g, ''), firstTouchOfCampaign, date);
        let combinedPath2 = combineSourceAndPath(arguments[0][1].replace(/\s/g, ''), lastTouchOfCampaign, date);

        if (combinedPath1 in DATA_BASE) {
            DATA_BASE[combinedPath1] += score / 2
        } else {
            DATA_BASE[combinedPath1] = score / 2
        }
        if (combinedPath2 in DATA_BASE) {
            DATA_BASE[combinedPath2] += score / 2
        } else {
            DATA_BASE[combinedPath2] = score / 2
        }
        return
    } else if (arguments.length == 6) {
        let sourcePath = arguments[0]
        let campaignPath = arguments[1]
        let firstTouchOfCampaign = arguments[2]
        let lastTouchOfCampaign = arguments[3]
        let score = arguments[4]
        let combinedPath1 = combineSourceAndPath(arguments[0][0].replace(/\s/g, ''), firstTouchOfCampaign, date);
        let combinedPath2 = combineSourceAndPath(arguments[0][arguments[0].length - 1].replace(/\s/g, ''), lastTouchOfCampaign, date);

        if (combinedPath1 in DATA_BASE) {
            DATA_BASE[combinedPath1] += score * 0.1
        } else {
            DATA_BASE[combinedPath1] = score * 0.1
        }

        if (combinedPath2 in DATA_BASE) {
            DATA_BASE[combinedPath2] += score * 0.1
        } else {
            DATA_BASE[combinedPath2] = score * 0.1
        }

        campaignPath.shift();
        campaignPath.pop();
        sourcePath.shift();
        sourcePath.pop();

        let valueLength = campaignPath.length
        let combinedPath = combineSourceAndPath(sourcePath, campaignPath, date)

        for (v in combinedPath) {
            if ((combinedPath[v]) in DATA_BASE) {
                DATA_BASE[combinedPath[v]] += (score * 0.8) / valueLength
            } else {
                DATA_BASE[combinedPath[v]] = (score * 0.8) / valueLength
            };
        }
        return
    }
}