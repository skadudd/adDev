//App-Script
//특정 google Drive 폴더에서 csv 파일을 읽어 merge 후, GA에 업로드
//전체 함수 실행. 폴더에 파일 없을 시 실행되지 않음

function init() {
    Logger.log("update checking..")
    var contentIndirectory = updateChecker();

    if (contentIndirectory) {
        Logger.log('start func')
        getCSVAndAppend();
        uploadData();
        clearRange();
        clearDirectory();
        Logger.log('func is completed')
    } else {
        Logger.log("func doesn't started")
    }
}

//작동 전 폴더 내용 확인. 
function updateChecker() {
    let folderData = 0;
    var size = 0;

    var folder = DriveApp.getFolderById('1UlhVYBs34k6mef3Mk8vMbOEdU-mMsvQF');
    var files = folder.getFilesByType("text/csv");
    var folderContent = checker(files)
    Logger.log(folderContent)
    return folderContent
}

//폴더에서 CSV를 해당 Sheet에 삽입하는 함수

function getCSVAndAppend() {
    var folder = DriveApp.getFolderById('1UlhVYBs34k6mef3Mk8vMbOEdU-mMsvQF');
    var files = folder.getFilesByType("text/csv");

    var openSpreadsheet = SpreadsheetApp.openById('12de8UdJgInf9AzokkMyt7qAnb6EWBWqpFHPnKaCQIdQ');
    var activeSheet = SpreadsheetApp.getActiveSheet();

    if (files.hasNext()) {
        var file = files.next();
        var csv = file.getBlob().getDataAsString();
        var csvData = Utilities.parseCsv(csv);
        var get_rid_header = csvData.shift()

        var lastrow = activeSheet.getLastRow();
        activeSheet.getRange(lastrow + 1, 1, csvData.length, csvData[0].length).setValues(csvData);
    }
    Logger.log("get-CSV-completed")
    return
}

function checker(files) {
    if (files.hasNext()) {
        var file = files.next();
        Logger.log('Updated file name : ' + file.getName())
        return true
    } else {
        Logger.log('Drive is empty')
        return false
    }
}

//GA MVP_master 속성의 NSA_cost_data 카테고리에 업로드 됨.
function uploadData() {

    var accountId = "82314120";
    var webPropertyId = "UA-82314120-6";
    var customDataSourceId = "pExH97VWSRu5a7NDKhYExA";
    var ss = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var maxRows = ss.getLastRow();
    var maxColumns = ss.getLastColumn();
    var data = [];

    for (var i = 1; i < maxRows; i++) {
        data.push(ss.getRange([i], 1, 1, maxColumns).getValues());
    }
    var newData = data.join("\n");
    var blobData = Utilities.newBlob(newData, "application/octet-stream", "GA import data");
    try {
        var upload = Analytics.Management.Uploads.uploadData(accountId, webPropertyId, customDataSourceId, blobData);
        //SpreadsheetApp.getUi().alert("Uploading: OK");
    } catch (err) {
        SpreadsheetApp.getUi().alert("Cannot upload: Failed");
    }

    Logger.log("upload-data-to-GA-completed")
    return
}

//업로드 후 헤더 제외한 행 삭제
function clearRange() {
    //replace 'Sheet1' with your actual sheet name
    var sheet = SpreadsheetApp.getActive().getSheetByName('시트1');
    sheet.getRange('A2:G100').clearContent();
    Logger.log("clear-sheet-completed")
    return;
}

//업로드 후 DB 폴더 삭제
function clearDirectory() {
    var folder = DriveApp.getFolderById('1UlhVYBs34k6mef3Mk8vMbOEdU-mMsvQF');
    Logger.log(folder.getLastUpdated())
    var files = folder.getFilesByType("text/csv");

    while (files.hasNext()) {
        var file = files.next();
        file.setTrashed(true)
    }
    Logger.log("remove-files-completed")
    return
}