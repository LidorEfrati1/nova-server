
const express = require('express');
const bodyParser = require('body-parser');
const { readSheet, writeSheet } = require('./sheets');
require('dotenv').config();

const app = express();
app.use(bodyParser.json());

app.post('/read', async (req, res) => {
    const { spreadsheetId, range } = req.body;
    try {
        const values = await readSheet(spreadsheetId, range);
        res.json({ values });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/write', async (req, res) => {
    const { spreadsheetId, range, values } = req.body;
    try {
        const result = await writeSheet(spreadsheetId, range, values);
        res.json({ result });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Nova Agent server running on port ${PORT}`);
});
