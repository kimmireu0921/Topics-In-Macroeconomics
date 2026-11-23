// Nov 24 study guide (v8 model). Run: node build24.js <out.docx>
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType,
  HeadingLevel, AlignmentType, LevelFormat, BorderStyle, PageNumber, Footer, TableOfContents, PageBreak,
} = require("docx");

const FONT = "Arial";
const W = 9638; // A4 width minus 2 cm margins, in DXA
const t = (text, o = {}) => new TextRun({ text, font: FONT, ...o });
const P = (runs, o = {}) => new Paragraph({ children: Array.isArray(runs) ? runs : [t(runs)], spacing: { after: 120 }, ...o });
const H1 = (s) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [t(s)] });
const H2 = (s) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [t(s)] });
const H3 = (s) => new Paragraph({ heading: HeadingLevel.HEADING_3, children: [t(s)] });
const B = (s, lvl = 0) => new Paragraph({ numbering: { reference: "bul", level: lvl }, children: rich(s), spacing: { after: 60 } });
// **bold** inside strings
function rich(s) {
  return s.split(/(\*\*[^*]+\*\*)/).filter(Boolean).map((x) => x.startsWith("**") ? t(x.slice(2, -2), { bold: true }) : t(x));
}
const PR = (s) => P(rich(s));
const border = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const borders = { top: border, bottom: border, left: border, right: border };
function table(rows, widths) {
  const tot = widths.reduce((a, b) => a + b, 0);
  const cw = widths.map((w) => Math.round((w / tot) * W));
  cw[cw.length - 1] += W - cw.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: cw,
    rows: rows.map((r, i) => new TableRow({
      tableHeader: i === 0,
      children: r.map((c, j) => new TableCell({
        borders, width: { size: cw[j], type: WidthType.DXA },
        shading: i === 0 ? { fill: "1F3A5F", type: ShadingType.CLEAR, color: "auto" } : (i % 2 === 0 ? { fill: "F2F5F9", type: ShadingType.CLEAR, color: "auto" } : undefined),
        margins: { top: 60, bottom: 60, left: 100, right: 100 },
        children: [new Paragraph({ children: i === 0 ? [t(c, { bold: true, color: "FFFFFF", size: 19 })] : rich(c).map((rn) => rn) , spacing: { after: 0 } })],
      })),
    })),
  });
}
const gap = () => new Paragraph({ children: [t("")], spacing: { after: 60 } });
// Q&A block
function QA(q, a) {
  return [new Paragraph({ children: [t("Q. ", { bold: true, color: "A8432C" }), t(q, { bold: true })], spacing: { before: 80, after: 40 }, keepNext: true }),
          new Paragraph({ children: [t("A. ", { bold: true, color: "2F5D8A" }), ...rich(a)], spacing: { after: 100 }, indent: { left: 280 } })];
}
function slide(num, title, presenter, onSlide, say, changed, qas) {
  const out = [H2(`Slide ${num}: ${title}`), P([t("Presenter: ", { bold: true }), t(presenter)])];
  out.push(H3("What is on the slide"), ...onSlide.map((x) => B(x)));
  out.push(H3("Key points to say"), ...say.map((x) => B(x)));
  if (changed) out.push(H3("What changed from last week"), PR(changed));
  out.push(H3("Possible questions"));
  qas.forEach(([q, a]) => out.push(...QA(q, a)));
  return out;
}

// ------------------------------------------------------------------ content
const C = [];
C.push(new Paragraph({ children: [t("EPS project · Nov 24 study guide", { bold: true, size: 40, color: "14213D" })], spacing: { after: 120 } }));
C.push(P([t("The new model (v8), slide by slide, with likely questions", { size: 26, color: "3D4756" })]));
C.push(P([t("Slides 63–75 of the class deck. Every number below comes from the model and survey files in our repository (v8_results.json, v8_extra.json, v8_capuse_hist.json, premium_evidence.json).", { italics: true, size: 19, color: "5F6876" })]));
C.push(P([t("Contents", { bold: true })]));
["1. The change in one page", "2. The model in six equations", "3. Key numbers to know", "4. Slide by slide (63–75), with possible questions", "5. The hardest questions, in one place", "6. Glossary"].forEach((x) => C.push(P([t(x)], { spacing: { after: 40 }, indent: { left: 280 } })));
C.push(new Paragraph({ children: [new PageBreak()] }));

// Part 1: the change
C.push(H1("1. The change in one page"));
C.push(PR("**In one sentence:** the old rule (every plant may use only 21% of its legal cap) did not fit the data, so we replaced it with the professor's suggestion: a random share of plants is eligible for EPS, and eligible plants may hire up to their full legal cap."));
C.push(table([
  ["", "Before (Nov 17 talk, v6)", "Now (Nov 24 talk, v8)"],
  ["Who may hire EPS workers", "Every plant with 1–299 core Korean workers", "A random 22% of new plants (EPS-eligible); the rest cannot"],
  ["How many", "21% of its legal cap (θ = 0.21), the same for every plant", "Up to its full legal cap"],
  ["What the cap counts", "Core Korean workers h only", "All Korean workers h + k, as in the law"],
  ["What makes EPS use equal the quota", "θ (the share of the cap)", "The eligible share of new plants (e)"],
  ["Targets", "Two had no source (5.5%, 10%)", "All sourced; new target: average cap use 62% (survey)"],
  ["Closure slope (Lee, Peri and Yang)", "Targeted (0.15)", "Reported, not targeted (model 0.00)"],
  ["Price result (net output)", "+0.33%", "+0.39% (2024 caps), +0.33% (2019 caps)"],
  ["Equal-limit result", "+0.09% to +0.19%", "0.00%"],
  ["Price result, gross output", "−0.90%", "+0.23%"],
], [26, 37, 37]));
C.push(gap());
C.push(H2("Why we changed it"));
C.push(B("**The data rejected the 21% rule.** In the 2019 survey, the median EPS firm uses 60% of its legal cap; only 17% use 21% or less; 18% are at or above the cap."));
C.push(B("**The professor's written feedback:** the model made EPS workers far too attractive (every firm wanted many more than the caps allow), whereas only about 10% of plants use EPS and users fill 62% of their caps. He offered two fixes, a two-sector model or random eligibility, and said either is better than limiting every plant to a small share of its cap."));
C.push(B("**The law counts all Korean workers,** so the cap now uses h + k."));
C.push(H2("What did not change"));
C.push(B("Hopenhayn entry and exit, with a logit taste shock that smooths exit."));
C.push(B("Two plant types (light, manual-intensive) and a Pareto tail in productivity."));
C.push(B("The extra cost of Korean manual workers at small plants (the \"premium\")."));
C.push(B("Korean and EPS manual workers as perfect substitutes (one for one)."));
C.push(H2("What the new model says"));
C.push(B("**The link to size barely matters.** Replacing the size-based cap with an equal limit changes net output by 0.00%, under both the 2024 and the 2019 caps, because caps rarely bind: 1.6% of EPS users are at their 2024 cap (10.7% at the 2019 cap)."));
C.push(B("**Access matters.** Letting any plant buy permits at a price raises net output by 0.39% (2024 caps)."));
C.push(B("**Caveat:** the gain is the Korean premium saved. If the premium is only higher pay rather than a real cost, the gain is +0.02%."));

// Part 2: equations
C.push(new Paragraph({ children: [new PageBreak()] }));
C.push(H1("2. The model in six equations"));
C.push(PR("These six equations run along the bottom of slides 66–75; the ones a slide uses are in bold. Equations (3) and (4) are the ones that changed."));
C.push(table([
  ["", "Equation", "In words", "Slides"],
  ["(1)", "y = s·(h^ρ + λₜ ℓ^ρ)^(α/ρ), ℓ = k + m", "A plant's output uses core Korean workers h and manual work ℓ. Manual work is done by Korean manual workers k or EPS workers m, one for one. λ is high for manual-intensive plants", "68, 70, 71, 75"],
  ["(2)", "cost of k = w·(1 + ψ(1 + h)^−ξ); cost of m = w", "A Korean manual worker costs more than the wage at small plants (2.70× at h = 0, 1.09× at h = 150); an EPS worker costs the wage (plus a fixed cost of using EPS at all)", "68, 70, 74"],
  ["(3)", "Eligible (share e): m ≤ q(h + k), h + k < 300", "NEW. A random share e of new plants may hire EPS workers up to the legal cap, which counts all Korean workers; plants with 300+ Korean workers cannot. Others hire none", "66, 67, 70–73, 75"],
  ["(4)", "Price: m at w + p; equal limit: m ≤ L", "NEW. The two experiments: any plant buys permits at price p; or the same eligible plants each get the same limit L", "69, 70, 73, 74"],
  ["(5)", "Exit if β(1−δ)E[V(s′)] < 0; Σν V = cₑ", "A plant closes when the expected future is not worth staying for; new plants enter until the expected value of entering equals the entry cost", "68, 70"],
  ["(6)", "Σμ(h + k) = N, Σμ m = M", "Korean workers are all employed, and total EPS use equals the quota (e, p or L adjusts so it does)", "67, 69, 70"],
], [6, 30, 50, 14]));
C.push(gap());
C.push(H2("Symbols"));
C.push(table([
  ["Symbol", "Meaning", "Value (v8)"],
  ["s = x·z", "Productivity: permanent part x (Pareto tail) times a changing part z", "—"],
  ["h, k, m", "Core Korean workers; Korean manual workers; EPS workers", "—"],
  ["λₜ", "Weight on manual work, light (A) and manual-intensive (B)", "0.034 and 0.70"],
  ["ψ, ξ", "Size of the Korean manual premium; how fast it falls with h", "1.70; 0.59"],
  ["q(·)", "Legal cap by Korean workers (2024 or 2019 schedule)", "Tables on slide 67"],
  ["e", "Eligible share of new plants", "22% (2024), 27% (2019)"],
  ["p; L", "Permit price; equal limit", "0.17; 45 (2024)"],
  ["w", "Wage of Korean workers", "Set by free entry"],
  ["N; M", "Korean labour; EPS quota", "1; 5.29% of workers"],
  ["β, δ, σ_ε, α", "Discount factor; exogenous exit; exit taste shock; returns to scale", "0.96; 0.016; 0.1; 0.69"],
], [18, 56, 26]));
// Part 2: numbers
C.push(new Paragraph({ children: [new PageBreak()] }));
C.push(H1("3. Key numbers to know"));
C.push(table([
  ["Number", "Value", "Meaning"],
  ["Eligible share of new plants", "22% (2024 caps); 27% (2019 caps)", "Adjusts so that total EPS use equals the quota"],
  ["Quota M", "5.29% of manufacturing workers", "219,507 E-9 workers ÷ 4.15 million workers, 2024"],
  ["Plants using EPS", "Model 7.0%; data 8.0%", "Ministry: 40,766 workplaces, 2024"],
  ["Average share of cap used", "Model 62.4%; survey 62.4%", "Targeted (2019 caps)"],
  ["Users at their cap", "Model 11% (2019 caps), 1.6% (2024 caps); survey 18% at or above", "Caps rarely bind in the model"],
  ["Survey firms below 30% / above 100% of cap", "21% / 11%", "The model has none in either"],
  ["Korean manual cost ÷ wage", "2.70 (h = 0), 1.50 (h = 7), 1.23 (28), 1.09 (150)", "ψ = 1.70, ξ = 0.59"],
  ["Price p", "0.17, 18% of the wage", "Clears the quota when any plant may buy"],
  ["Net output: price", "+0.39% (2024), +0.33% (2019), +0.02% if premium is pay", "Main result"],
  ["Net output: equal limit", "0.00% (both cap schedules)", "No link to size: no effect"],
  ["Net output: no EPS at all", "−5.76%", "For scale: a price gains about 1/15 of what EPS adds"],
  ["Gross output: price", "+0.23%", "Plants +1.3%; users 7.0% → 8.7% of plants"],
  ["Closure slope", "Model 0.00; Lee, Peri and Yang 0.152", "Not targeted"],
  ["Plants by group", "Manual eligible 9.9%, manual not eligible 33.8%, light 56.3%", "Only manual eligible plants use EPS (71% of them)"],
], [30, 34, 36]));

// Part 3: slide by slide
C.push(new Paragraph({ children: [new PageBreak()] }));
C.push(H1("4. Slide by slide"));
C.push(...slide(63, "Cover", "Mimi",
  ["Title: \"EPS project: the new model and what it says\"; the research topic"],
  ["Today: the histogram the professor asked for, the new model in brief, and what it says"], null,
  [["Has the research question changed?", "Not yet. The model now says the size link barely matters and access does, so we ask him on the last slide whether the paper should be about access."]]));
C.push(...slide(64, "Your feedback, and what we changed", "Mimi",
  ["Five rows: each comment from Nov 17 and what we did"],
  ["The 21% rule is gone; replaced by random eligibility, which he suggested", "The cap counts all Korean workers, as in the law", "The inferred 2024 line and the larger-quota comparison are dropped"],
  "This slide is new; it replaces last week's list of questions.",
  [["Why random eligibility and not the two-sector model?", "He offered both. Our light plants already act as the other sector (they never use EPS), and random eligibility rations access among manual-intensive plants."],
   ["Did you change anything else?", "We recalibrated to sourced targets and added the survey's average cap use (62%) as a target. Everything else in the model is unchanged."]]));
C.push(...slide(65, "The histogram: EPS workers ÷ legal cap", "Mimi",
  ["Bar chart: survey (orange) vs model (blue), plants with at least one EPS worker, 2019 caps", "Dashed line: the old 21% rule", "Box: same average (62%, targeted); the model is more concentrated"],
  ["The data reject the 21% rule: the median firm uses 60% of its cap", "The model matches the average and the median (58% vs 60%)", "But it has no plants below 30% of the cap (survey 21%) and none above 100% (survey 11%)"],
  "Last week the model put 82% of users exactly at 21% of their cap. The survey bars were also corrected on Nov 20: firms at exactly 30%, 60% and 70% had been counted one bar too low.",
  [["Why does the model have no plants below 30% of their cap?", "Using EPS has a fixed cost in the model, so a plant that uses EPS hires several workers. A firm with 1 worker on a cap of 5 (20%) does not exist in the model. This is our best explanation; we have not tested it."],
   ["Why are 11% of survey firms above their cap?", "It is not timing: counting Korean workers in August instead of February still gives 11%. Possibly extra permits; we asked the Ministry."],
   ["Why the spikes at 20, 40, 60, 80%?", "Many survey firms have a cap of 5, so 1, 2, 3 or 4 workers is 20, 40, 60 or 80%."],
   ["Is the 62% targeted?", "Yes, the average is a calibration target. The shape is not."]]));
C.push(...slide(66, "What changed in the model since last week", "Benjamin",
  ["Table: before vs now (who may hire, how many, what the cap counts, what clears the quota, targets, main result)", "Footer: what stayed the same"],
  ["Before: every plant could use EPS, but only 21% of its cap", "Now: a random 22% of new plants is eligible, and eligible plants can use their full legal cap", "The headline result changed: removing the link to size now gains nothing"],
  "New slide, for classmates who were not part of the feedback discussion.",
  [["Why does the result change so much?", "Under the old rule every plant was held at 21% of its cap, so the cap always bound and removing the size link mattered. Now plants below their cap are not held back by it, so the size link barely matters."],
   ["Is the 22% a parameter?", "No. It adjusts until total EPS use equals the quota, the job θ used to do."]]));
C.push(...slide(67, "The model (1/3): plants and today's EPS rules", "Benjamin",
  ["Bullets: what each plant draws at entry; eligibility; the quota", "Two tables: 2024 and 2019 legal caps by Korean workers"],
  ["At entry a plant draws its type, its productivity and its eligibility, all permanent", "Eligible plants may hire up to q(h + k) if h + k < 300; others hire none", "2024 caps for today's economy; 2019 caps when we compare with the survey"],
  "Eligibility is new; the cap is now on h + k instead of h.",
  [["Why is eligibility permanent?", "It is the simplest version. Real permits last about three years; whether to redraw eligibility is one of our questions for him."],
   ["Why are 44% of plants manual-intensive when he said about 10%?", "Being manual-intensive is not the same as using EPS. Only the eligible ones (9.9% of plants) use EPS; the other 33.8% cannot get permits. The 44% comes from the calibration and is not checked against data."],
   ["The 300-worker rule: Korean workers only?", "The law also lets firms with capital of ₩8bn or less qualify; we do not model that exception."]]));
C.push(...slide(68, "The model (2/3): output, costs and the plant's choice", "Benjamin",
  ["Equations: production; cost of Korean manual and EPS workers; value function", "Table: cost of a Korean manual worker ÷ wage at h = 0, 7, 28, 150", "Footer: survey evidence"],
  ["Manual work is done by Korean manual workers or EPS workers, one for one", "Korean manual workers cost more than the wage at small plants: 2.70× at h = 0, 1.09× at h = 150", "An EPS worker costs the wage, so it saves that extra cost"],
  "The equations are unchanged; the premium is larger after recalibration (ψ 0.92 → 1.70).",
  [["Is 2.7 times the wage realistic?", "It is not a wage. In the survey, the smallest firms fill only 44% of the Korean manual hires they plan (89% at large firms), while their Korean wages are no higher (about 1.12 times EPS wages at every size). The cost is unfilled jobs."],
   ["Why perfect substitutes?", "One change at a time. Imperfect substitutes could be a robustness check; Dong, Lee and Yang (2024) suggest natives and immigrants are imperfect substitutes."],
   ["What sets ψ?", "Three targets: plants using EPS, the size of EPS firms and cap use. With ψ = 0.92, only 4.7% of plants would use EPS (data 8%)."]]));
C.push(...slide(69, "The model (3/3): equilibrium and the two experiments", "Julian",
  ["Table: today vs price vs equal limit (who may hire, how many, cost per EPS worker, what clears the quota)"],
  ["Same quota in every case; we compare steady states", "Price: any plant may buy permits at p", "Equal limit: the same eligible plants, each with the same limit L, so only the link to size is removed"],
  "The equal limit now keeps the same eligible plants.",
  [["What if the quota is not fully used?", "Then the eligible share would be 100% and results would change. In the model it is 22%. Evidence is mixed: a 2024 projection put arrivals near half the quota, while waiting lists were reported in 2026."],
   ["Who gets the permit revenue?", "It is returned to households, so it is not lost."]]));
C.push(...slide(70, "Calibration: 13 parameters, 8 targets", "Julian",
  ["Table: eight targets, data, model, source", "Box: the closure response is not matched"],
  ["Every target has a source; the fit is close", "We do not match the closure response to the 2020 stop (data 0.15, model 0.00)"],
  "New target (cap use 62%); the closure slope moved from target to check.",
  [["Why is the closure slope zero?", "Plants that use EPS are productive and far from closing, because the fixed cost of using EPS keeps marginal plants out. Even the best of 256 random parameter draws gave at most 0.07."],
   ["Why did you drop it as a target?", "Keeping it pulled the other targets off without moving the slope. It was already fragile in the old model (0.15 on the base grid, 0.05 on a finer one)."],
   ["Is it identified with 13 parameters and 8 targets?", "Not one by one; we minimise the sum of squared percentage gaps."]]));
C.push(...slide(71, "Who uses EPS: 7.0% of plants (data 8.0%)", "Sara",
  ["Table: four groups (manual or light × eligible or not): % of plants, % using EPS, workers per plant"],
  ["Only eligible manual-intensive plants use EPS (71% of them)", "This answers his concern that every firm wanted EPS workers"],
  "Last week 99% of manual-intensive plants used EPS.",
  [["Who are the manual-intensive plants that are not eligible?", "Firms that are rejected or never get permits. The Ministry data on applications against permits granted should show them."],
   ["Why do 29% of eligible manual plants not use EPS?", "They are small or unproductive, and EPS has a fixed cost."]]));
C.push(...slide(72, "An untargeted check: EPS firms by size", "Sara",
  ["Left: where EPS firms are by total workers (model 45/31/19% under 10/10–19/20–49; survey 41/26/25%)", "Right: EPS share of workers by size (model 36→12%; survey 52→6%)"],
  ["Where EPS firms are by size is close to the survey", "The EPS share falls with size in both, but the model is too flat among the smallest firms"],
  null,
  [["Why is the model too flat among small firms?", "Small plants have small caps, so their EPS share cannot rise much. In the survey the smallest firms rely on EPS for about half their workers."]]));
C.push(...slide(73, "Result: the link to size barely matters; access does", "Donny",
  ["Table: equal limit, price and no EPS: net output (2024 and 2019 caps), gross output, and net if the premium is only pay", "Box: why size does not matter, why a price helps, the caveat"],
  ["Equal limit: 0.00% under both cap schedules, because caps rarely bind", "Price: +0.39% (2024), +0.33% (2019)", "The gain is the premium saved: +0.02% if the premium is only pay"],
  "Last week: price +0.33%, equal limit +0.09–0.19%, gross output −0.90%. The equal limit now gives nothing and gross output rises.",
  [["Does the size rule keep weak plants alive?", "Not in this model: caps rarely bind (1.6% of users at the 2024 cap, 10.7% at the 2019 cap). Whether a plant gets permits at all matters more."],
   ["Isn't \"caps don't matter\" built into your assumptions?", "It follows from matching the 62% average cap use. The old 21% rule forced the opposite. The key assumption is that a firm below its cap has all the EPS workers it wants; the survey partly disagrees (41% of firms below half their cap still want more), and the Ministry data can test it."],
   ["Your whole gain depends on the premium?", "Yes: +0.02% if it is only pay. The survey supports a real cost: small firms leave jobs unfilled and do not pay Koreans more."],
   ["Is +0.39% big?", "EPS as a whole adds about 5.8% to net output, so a better allocation is worth about a fifteenth of that."],
   ["Why does gross output now rise when it fell before?", "Today only 22% of plants have access; a price opens it to others, freeing Korean workers for core jobs. Swapping parameters and structure shows the sign comes mainly from the new parameters."]]));
C.push(...slide(74, "Why: with a price, EPS workers move to mid-sized plants", "Donny",
  ["Top table: share of EPS workers by core Korean workers, today (10/24/35/31%) and with a price (0/31/69/0%)", "Bottom table: the median and top-1% eligible plants, today and with a price", "Box: the explanation"],
  ["Large plants (30+ core Koreans) hold 31% of EPS workers today but save little: Koreans are easy to find there", "With a price (0.17, 18% of the wage), the median and top plants stop using EPS", "The workers go to plants with 5–29 core Koreans, where Korean manual workers are scarcest"],
  null,
  [["Why does the median plant stop using EPS?", "It saves less than the price on each EPS worker."],
   ["Why not the smallest plants (under 5 core Koreans)?", "Using EPS has a fixed cost they cannot cover at that price."],
   ["Why does the top plant have exactly 100 Korean workers today?", "Just over 100 raises its 2024 cap from 35 to 40: bunching at a cap step."]]));
C.push(...slide(75, "What we assume, and our questions", "Donny",
  ["Left: four key assumptions", "Right: three questions for the professor"],
  ["The premium assumption matters most: the gain is the premium saved", "Most important question: is the model settled, so we can freeze it and write the paper?"],
  null,
  [["What would redrawing eligibility change?", "Unknown. It might put some users near the exit margin and raise the closure response. It is a model change, so we ask before doing it."],
   ["What will the Ministry data add?", "Applications against permits granted, by size: a test of whether firms below their cap are rationed."]]));

// Part 4: hard questions
C.push(new Paragraph({ children: [new PageBreak()] }));
C.push(H1("5. The hardest questions, in one place"));
[["Is the result circular (random eligibility makes caps irrelevant)?", "Not by assumption: it comes from matching the survey's 62% average cap use. Plants that use 62% of their cap on average are mostly not held back by it. It does rest on one assumption: a firm below its cap has all it wants."],
 ["Is the gain only an accounting choice?", "Partly. With perfect substitutes, moving EPS workers between plants changes only the premium saved, fixed costs and entry, so the gain is the premium. The survey supports treating it as a real cost (unfilled jobs, flat wages). We report both."],
 ["How robust is +0.39% to the premium?", "Holding other parameters fixed: ψ = 0.92 gives +0.13%; ψ = 1.36 gives +0.51%; ψ = 1.70 (ours) +0.39%; ψ = 2.04 +0.47%. So report a range."],
 ["Why not match the closure slope?", "In this model a temporary two-year cut barely changes a plant's value, so exit hardly responds. Matching it would need a new mechanism, which is too late."],
 ["Is the quota really binding?", "In the model, yes (22% eligible). In the data the evidence is mixed. If it were slack, results would change; the Ministry data may tell."],
 ["What exactly is a plant's state?", "The pair (x, z): permanent and changing productivity. Two plants with the same s but different x are different states in the code."]].forEach(([q, a]) => C.push(...QA(q, a)));

// Part 5: glossary
C.push(H1("6. Glossary"));
C.push(table([
  ["Term", "Meaning"],
  ["Legal cap q(n)", "Most EPS workers a plant may hire, set by law from its insured Korean workers n = h + k"],
  ["Eligible share e", "Share of new plants allowed to hire EPS workers; adjusts so EPS use equals the quota"],
  ["θ (old model)", "The share of its cap every plant could use (0.21); removed"],
  ["Quota M", "Total EPS workers allowed in the economy (5.29% of manufacturing workers)"],
  ["Premium (ψ, ξ)", "Extra cost of a Korean manual worker at small plants; ψ sets its size, ξ how fast it falls with size"],
  ["Price p", "Permit price in the experiment where any plant may buy permits"],
  ["Equal limit L", "The same EPS limit for every eligible plant; removes only the link to size"],
  ["Gross output", "Everything plants produce"],
  ["Net output", "Gross output minus the premium, fixed costs and entry costs (our welfare measure)"],
  ["Closure slope", "How much more EPS-exposed firms closed after the 2020 stop (Lee, Peri and Yang: 0.152)"],
  ["Steady state", "The long-run economy where the distribution of plants no longer changes; we compare these"],
], [28, 72]));

const doc = new Document({
  creator: "EPS project team",
  title: "Nov 24 study guide",
  styles: {
    default: { document: { run: { font: FONT, size: 21 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 32, bold: true, color: "14213D" }, paragraph: { spacing: { before: 300, after: 160 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 26, bold: true, color: "1F3A5F" }, paragraph: { spacing: { before: 260, after: 100 }, keepNext: true, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 22, bold: true, color: "2F5D8A" }, paragraph: { spacing: { before: 140, after: 60 }, keepNext: true, outlineLevel: 2 } },
    ],
  },
  numbering: { config: [{ reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 260 } } } },
                                                        { level: 1, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 800, hanging: 260 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [t("Nov 24 study guide · page ", { size: 17, color: "8A94A6" }), new TextRun({ children: [PageNumber.CURRENT], size: 17, color: "8A94A6", font: FONT })] })] }) },
    children: C,
  }],
});
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(process.argv[2], b); console.log("written", process.argv[2]); });
