function doGet() {
  return ContentService.createTextOutput("Future Farmers API Aktif! Veri göndermeye hazırım.");
}

// 2. Veri alma ve işleme
function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    
    // TABLO ID (Sabit - Dokunma)
    var sheetId = "1Nd6NLzE74TFiJv1QSnnsWC2lqFt5bwKf2qaKEX6C2No"; 
    var sheet = SpreadsheetApp.openById(sheetId).getActiveSheet();
    
    // KLASOR ID (Bunu az önce kopyaladığın ID ile değiştir!)
    var folderId = "1k0bgpAnXJpRoBaxByBVbJhE7NhH2c3-2"; 
    var folder = DriveApp.getFolderById(folderId);
    
    // Resim İşlemleri
    var fileUrl = "Resim yüklenmedi";
    if (data.Foto_Base64 !== "Test_Verisi") {
      var contentType = "image/jpeg";
      var decodedImg = Utilities.base64Decode(data.Foto_Base64);
      var blob = Utilities.newBlob(decodedImg, contentType, "Gozlem_" + data.Tarih.replace(/[: ]/g, "_") + ".jpg");
      var file = folder.createFile(blob);
      file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
      fileUrl = file.getUrl();
    }
    
    // Veriyi tabloya ekle
    sheet.appendRow([data.Tarih, data.Gozlem_Turu, data.Rakim, data.Hava_Durumu, data.Stres_Skoru, data.Notlar, fileUrl]);
    
    return ContentService.createTextOutput("Başarılı").setMimeType(ContentService.MimeType.TEXT);
    
  } catch(error) {
    return ContentService.createTextOutput("Hata: " + error.toString()).setMimeType(ContentService.MimeType.TEXT);
  }
}
