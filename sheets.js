
const { google } = require('googleapis');

async function authorize() {
    const credentials = JSON.parse(process.env.GOOGLE_CREDS);
    const auth = new google.auth.GoogleAuth({
        credentials,
        scopes: ['https://www.googleapis.com/auth/spreadsheets'],
    });
    return await auth.getClient();
}

async function readSheet(spreadsheetId, range) {
    const auth = await authorize();
    const sheets = google.sheets({ version: 'v4', auth });
    const response = await sheets.spreadsheets.values.get({
        spreadsheetId,
        range,
    });
    return response.data.values;
}

async function writeSheet(spreadsheetId, range, values) {
    const auth = await authorize();
    const sheets = google.sheets({ version: 'v4', auth });
    const response = await sheets.spreadsheets.values.update({
        spreadsheetId,
        range,
        valueInputOption: 'RAW',
        requestBody: {
            values,
        },
    });
    return response.data;
}

module.exports = { readSheet, writeSheet };
