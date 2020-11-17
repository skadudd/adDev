//app-script
//프로덕트 팀과 마케팅 팀의 로그를 병합하여 DB에 저장하는 코드.

const team = ['프디', '마케팅']
const sheetActive = SpreadsheetApp.getActive()

function myFunction() {
    for (v in team) {
        Logger.log(team[v])
        let logData = getData(team[v])
        let definedValue = nullIdentify(logData)
        clearSheet(team[v])

        if (definedValue) {
            Logger.log(definedValue)
            let teamLogData = appendSignatureOfTeam(definedValue, team[v])
            Logger.log('저장될 Log : ' + teamLogData)
            appendData(teamLogData)

        }

    };
}

function getData(thisTeam) {
    // let sheetActive = SpreadsheetApp.getActive()
    let sheet = sheetActive.getSheetByName(thisTeam);
    let logData = sheet.getRange(`A2:D${sheet.getLastRow()}`).getValues()


    return logData
}

function nullIdentify(logData) {

    if (logData[0][0] == '날짜') {
        return null
    } else {
        return logData
    }

}

function appendData(logData) {
    let sheet = sheetActive.getSheetByName('DB_Log');
    let data = logData
    sheet.getRange(sheet.getLastRow() + 1, 1, data.length, 5).setValues(data);

}

function appendSignatureOfTeam(definedValue, team) {

    for (v in definedValue) {
        definedValue[v].push(team)
    }
    return definedValue
}

function clearSheet(thisTeam) {
    Logger.log(2, thisTeam)
    let sheet = sheetActive.getSheetByName(thisTeam);
    sheet.getRange('A2:D100').clear()
    Logger.log("clear-sheet-completed")
    return;

}