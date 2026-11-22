// Usage: node html2pdf.js in.html out.pdf "footer text"
const { chromium } = require('playwright');
(async () => {
  const [inp, out, foot] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + inp);
  await p.pdf({ path: out, format: 'A4', printBackground: true, displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: `<div style="font-size:7pt;width:100%;text-align:center;color:#595959;font-family:Arial">${foot} · <span class="pageNumber"></span>/<span class="totalPages"></span></div>`,
    margin: { top: '16mm', bottom: '18mm', left: '14mm', right: '14mm' } });
  await b.close();
})();
