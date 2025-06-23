const express = require('express');
const MayaDate = require('maya-date');
const app = express();
const port = process.env.PORT || 3000;

app.get('/calculate-kin', (req, res) => {
  const dateStr = req.query.date;
  if (!dateStr) {
    return res.status(400).json({ error: "Provide date=YYYY-MM-DD" });
  }

  const date = new Date(dateStr);
  if (isNaN(date)) {
    return res.status(400).json({ error: "Invalid date format" });
  }

  const maya = new MayaDate(date);

  res.json({
    input: dateStr,
    longCount: maya.longCount,
    tzolkin: maya.tzolkin,
    haab: maya.haab
  });
});

app.get('/', (req, res) => {
  res.send('MayaDate API is running. Use /calculate-kin?date=YYYY-MM-DD');
});

app.listen(port, () => {
  console.log(`MayaDate API listening on port ${port}`);
});
