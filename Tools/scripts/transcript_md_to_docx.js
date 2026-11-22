// Converts interview transcript .md files ("<name> - תמלול ראיון*.md") to RTL Word files
// in the voice-note style: title, source line, then one paragraph per segment: "[HH:MM:SS] text".
// Internal notes (do-not-use-on-camera, unclear names) stay in the md only.
//
// Usage: node transcript_md_to_docx.js "<קבצי md dir>" "<תמלולים בוורד dir>" [name filter]
// Needs the npm "docx" package: set NODE_PATH to a folder where it is installed
// (e.g. `npm install docx@9.5.1` in a scratchpad folder, then NODE_PATH=<that>/node_modules).
const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, AlignmentType } = require('docx');

const [srcDir, outDir, filter] = process.argv.slice(2);
fs.mkdirSync(outDir, { recursive: true });

const FONT = 'Arial';
const run = (text, opts = {}) => new TextRun({ text, font: FONT, rightToLeft: true, size: 24, ...opts });
const para = (runs, opts = {}) => new Paragraph({ bidirectional: true, alignment: AlignmentType.RIGHT, spacing: { after: 80 }, children: runs, ...opts });
const strip = (s) => s.replace(/\*\*/g, '').replace(/\*/g, '');

const files = fs.readdirSync(srcDir).filter((f) => f.includes('תמלול ראיון') && f.endsWith('.md') && (!filter || f.includes(filter)));
for (const f of files) {
  const lines = fs.readFileSync(path.join(srcDir, f), 'utf8').split('\n');
  const name = f.split(' - ')[0];
  const children = [para([run(`תמלול - ${name}`, { bold: true, size: 32 })], { spacing: { after: 160 } })];

  // Header: first metadata paragraph only (date, topic, source). Internal notes stay in the repo.
  const sep = lines.indexOf('---');
  const header = lines.slice(1, sep).map((l) => l.trim()).filter(Boolean);
  if (header.length) {
    children.push(para([run(strip(header[0]), { size: 22, color: '555555' })]));
    if (!header[0].includes('תמלול אוטומטי')) {
      children.push(para([run('תמלול אוטומטי. לפני ציטוט, לבדוק מול ההקלטה לפי חותמת הזמן.', { size: 22, color: '555555' })]));
    }
  }
  children.push(para([], { spacing: { after: 120 } }));

  let segs = 0;
  for (const raw of lines.slice(sep + 1)) {
    const l = raw.trim();
    if (!l || l === '---') continue;
    const m = l.match(/^\*\*\[(\d{2}:\d{2}:\d{2})\]\*\*\s*(.*)$/);
    if (m) {
      segs++;
      children.push(para([run(`[${m[1]}] `, { bold: true, color: '1F4E79' }), run(strip(m[2]))]));
    } else if (l.startsWith('# ')) {
      children.push(para([run(strip(l.slice(2)), { bold: true, size: 28 })], { spacing: { before: 360, after: 120 }, keepNext: true }));
    } else if (l.startsWith('## ')) {
      children.push(para([run(strip(l.slice(3)), { bold: true, size: 26 })], { spacing: { before: 240, after: 100 }, keepNext: true }));
    } else {
      children.push(para([run(strip(l), { italics: true, size: 22 })]));
    }
  }

  const doc = new Document({
    styles: { default: { document: { run: { font: FONT, size: 24 } } } },
    sections: [{ properties: { page: { margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } }, children }],
  });
  Packer.toBuffer(doc).then((buf) => {
    const out = path.join(outDir, `תמלול - ${name}.docx`);
    fs.writeFileSync(out, buf);
    console.log(`${name}\t${segs}\t${buf.length}`);
  });
}
