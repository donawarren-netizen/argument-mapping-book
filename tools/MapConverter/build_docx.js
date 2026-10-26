const fs = require("fs");
const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  HeadingLevel,
} = require("docx");

const LEVELS = [
  HeadingLevel.HEADING_1,
  HeadingLevel.HEADING_2,
  HeadingLevel.HEADING_3,
  HeadingLevel.HEADING_4,
  HeadingLevel.HEADING_5,
  HeadingLevel.HEADING_6,
];

// Word's built-in style IDs go up to Heading9. The `docx` library's
// HeadingLevel enum only covers 1-6, so levels 7-9 are applied via the raw
// style ID instead, with matching style definitions declared below.
const EXTRA_HEADING_STYLE_IDS = ["Heading7", "Heading8", "Heading9"];

const EXTRA_HEADING_STYLE_DEFS = EXTRA_HEADING_STYLE_IDS.map((id, i) => ({
  id,
  name: `Heading ${i + 7}`,
  basedOn: "Normal",
  next: "Normal",
  quickFormat: true,
  run: { color: "1F4D78", size: 20 }, // continues the darker/smaller trend of Heading6
}));

function main() {
  const [, , inputJsonPath, outputDocxPath] = process.argv;
  if (!inputJsonPath || !outputDocxPath) {
    console.error("Usage: node build_docx.js <outline.json> <output.docx>");
    process.exit(1);
  }

  const { outline } = JSON.parse(fs.readFileSync(inputJsonPath, "utf-8"));

  const INDENT_PER_LEVEL = 360; // twips (~0.25") per heading level

  const paragraphs = outline.map((entry) => {
    const lvl = Math.min(entry.level, 9);
    const paragraphProps = {
      outlineLevel: lvl - 1, // 0-indexed; enables Word's collapsible heading arrows
      indent: { left: (lvl - 1) * INDENT_PER_LEVEL },
      children: [new TextRun(entry.text)],
    };
    if (lvl <= 6) {
      paragraphProps.heading = LEVELS[lvl - 1];
    } else {
      paragraphProps.style = EXTRA_HEADING_STYLE_IDS[lvl - 7];
    }
    return new Paragraph(paragraphProps);
  });

  const doc = new Document({
    styles: {
      paragraphStyles: EXTRA_HEADING_STYLE_DEFS,
    },
    sections: [
      {
        properties: {
          page: { size: { width: 12240, height: 15840 } }, // US Letter
        },
        children: paragraphs,
      },
    ],
  });

  Packer.toBuffer(doc).then((buffer) => {
    fs.writeFileSync(outputDocxPath, buffer);
    console.log(`Wrote ${outputDocxPath}`);
  });
}

main();
