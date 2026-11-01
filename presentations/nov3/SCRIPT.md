# Nov 3 script

Generated from the deck's speaker notes. Read the quoted lines aloud. "If asked" entries are backup answers, read only if the topic comes up.

## Julian

### Slide 27: EPS project update: what changed since your feedback

**[Title]**

"Good afternoon. Benjamin can't join us today, so the four of us will present. We'll show what we did with your feedback from October 27 and your comments on the proposal."

**[Research question]**

"Our question hasn't changed. Does tying EPS workers to plant size keep weak plants alive, and how much would output change if the same quota ignored plant size?"

**[Subtitle]**

"We'll cover the cap schedule, a new data source, bunching, three targets we corrected, and our result. The short version: the gain from removing the size rule is now about 0.3 percent, right at the line we set in the proposal."

### Slide 28: Your feedback: what you asked, and what we did

**[Title]**

"This is everything you raised, and where each item stands."

**[Rows 1 and 2]**

"You said we should at least see bunching in the model, and suggested a fatter tail. We've done both. Plants with 50 or more workers are now 1.8 percent, against 2.1 in the data."

**[Row 3]**

"You said 0.4 percent looked small. Bunching raised it to about 1 percent, but correcting three targets brought it down to about 0.33 percent. So this one is still open."

**[Rows 4 and 5]**

"You questioned our cap numbers, and you told us to look at the data. We fixed the first and found firm-level data for the second."

**[Row 6]**

"On H-1B, we agree: paperwork is harder for small firms. Our fixed cost of using EPS plays that role."

**[Row 7]**

"On population: Korean labor is fixed, and the experiments only add or remove EPS workers. We don't have a population growth rate yet."

**[Row 8]**

"We also list all our assumptions, on slide 37."

**[Footer]**

"One thing to check with you. Your written summary mentioned about 0.5 percent from removing EPS, but our October 27 slide said 7.5 percent. It's now 7.2 percent. We want to be sure we mean the same number."

**[If asked: Helpman-style]**

"Your note said Helpman-style. Our model builds on Hopenhayn 1992, so we took it to mean that."

### Slide 29: Cap schedule: re-checked at the source and redrawn

**[Title]**

"You asked us to re-check the cap schedule, so we checked it on the EPS website."

**[Blue box, first line]**

"Plants with 1 to 10 Korean workers can hire their Korean count plus 10. Plants with 11 to 50 can hire 30, but never more than twice their Korean workers. Our sentence left out that limit, which is why the numbers didn't add up."

**[Blue box, second line]**

"So 10 Koreans can hire 20, which is 67 percent. 11 Koreans can hire 22, also 67 percent. The 81 percent we quoted is for a plant with 3 Koreans."

**[Left chart]**

"This is the new figure. It shows the cap in workers, so you can check the numbers directly."

**[Right chart]**

"This is the same rule as a share of workers. The old figure plotted this correctly. The problem was our sentence."

**[Legend]**

"We use both schedules. The survey and the COVID shock date from 2019, so those targets use the 2019 caps. The census targets and all our experiments use the 2024 caps."

**[If asked: anything left out of the cap]**

"Root industries may hire 20 percent above the cap, and the model leaves that out. It's on our assumptions slide."

**[Hand over]**

"Mimi will now show the new data we found."

## Mimi

### Slide 30: New data: EPS and Korean workers at each surveyed firm

**[Title]**

"You told us to look for meaningful data. We found a firm-level survey of EPS employers."

**[Table]**

"KDI ran it with the World Bank in 2019. It covers 772 manufacturers, and it's published with Dong, Lee and Yang's 2024 paper. Lee, Peri and Yang use the same survey."

**[Cards]**

"The average firm has about 20 workers: 15 and a half Korean and 5 EPS."

**[Table, last row]**

"It has limits. It covers only firms that use EPS, only the 2019 caps, the response rate is 27.6 percent, and the public file has no closures."

**[Blue box]**

"So it's real firm-level data, but a sample of users, not all plants."

**[If asked: 38 percent versus other shares]**

"38 percent is a simple average across firms. Weighted by employment it's 24 percent. Our averages don't adjust for the sampling design, because we found no sampling weights in the public file."

**[If asked: data handling]**

"The file is public, but we keep it out of our repository and report only aggregates."

### Slide 31: Cap use: firms use about 60% of their cap, at nearly every size

**[Title]**

"This is the number we were missing: how close firms are to their caps."

**[First card and table]**

"On average, firms use 62 percent of their cap, and it's about the same at most sizes. Our model's rule, where every plant gets the same share of its cap, fits that flat pattern. The level is lower, though: 49 percent in the model. We don't target this number. The bottom row has only 16 firms."

**[Cards 2 and 3]**

"But firms differ a lot. 42 percent use less than half their cap, while 18 percent are at or above it."

**[Last card]**

"The survey also asks how many more workers firms would hire with no limit. 44 percent would hire more, so most would not. That's 60 percent of firms exactly at their cap, but also 41 percent of firms using under half."

**[Blue box]**

"In our model, every user wants more. That's the assumption we most need to fix."

**[If asked: why below the cap but wanting more]**

"Dong, Lee and Yang describe a points ranking with a cut-off and a limit of 3 to 6 new permits per round. Our model has neither. We'd like to ask the authors whether that's the reason."

**[If asked: how firms exceed the cap]**

"11 percent are above it. One known reason is that root industries may hire 20 percent more. We haven't checked the others."

**[If asked: other gaps from the survey]**

"The model has too few EPS firms with 20 to 49 workers, 10 percent against 25. It also has too little spread in EPS shares, a standard deviation of 0.15 against 0.22."

### Slide 32: Bunching: the data show a small spike; the model piles up far more

**[Title]**

"You asked us to compare bunching in the model with the data. Our October 27 test used the census, which can't separate Korean and foreign workers. This survey can."

**[Chart, bars]**

"The bars show the share of EPS firms at each count of Korean workers, which is what the cap is based on."

**[Chart, around 5 and 6]**

"Under the 2019 rule, the cap rises from 5 to 7 when a firm goes from 5 to 6 Korean workers. In the data, counts dip at 5, then jump at 6, to about one and a half times the trend. But we don't see a clear spike after 10, 30 or 50, and counts of 14 and 15 jump by a similar amount without being cap steps. So this is suggestive, not a test."

**[Chart, line]**

"The line is our model. It bunches at the right place, but far too much: 36 percent of its EPS users sit just past 5, against 6 to 7 percent in the data, and none sit at 4 to 5 or 7 to 10."

**[Third bullet]**

"We think that's because the model has no frictions, and every plant gets the same share of its cap. We haven't tested that yet. Realistic rationing should show whether it helps."

**[Limits bullet]**

"A real test needs all plants, which is why we want the Ministry's data."

**[If asked: how strong is the spike]**

"48 firms in the firm list and 53 in the survey answers, with z-statistics of 2.1 to 2.9. We also checked other counts, and that's why we don't call it a test."

**[Hand over]**

"Sara will show the model at larger sizes, then how all this changed our calibration and results."

## Sara

### Slide 33: Model bunching: plants pile up at the cap steps

**[Title]**

"Now the model at larger sizes. You said we should see bunching in the model, and our last version showed none."

**[Blue box]**

"We changed two things. A Pareto tail, so plants actually reach these sizes, and a size grid that includes every cap step."

**[Chart]**

"The blue line is the current rule. The orange line is the same quota with no size rule."

**[Table]**

"Each number is the density of plants just past a step, divided by the density just below it. One means no bunching. Under the current rule, the four steps are 1.6 to 1.9. Without the rule, they fall to 0.8 to 0.9."

**[Bottom row of the table]**

"Just under 300, the number is below one, because plants stop growing before they lose eligibility."

**[Caution]**

"This is the model only, under the 2024 caps. We have no data to compare at these sizes, because the survey has too few firms past 50. So this is a prediction, and the Ministry's table could test it."

**[If asked: which workers count]**

"In the model, the cap depends on core Korean workers. The law counts all insured Koreans. That's on our assumptions slide."

### Slide 34: Calibration: three targets corrected to match how the data measure them

**[Title]**

"When we read the survey closely, we found three of our targets didn't match how the data measure them. These were our mistakes."

**[Right box, first bullet]**

"Their 36.9 percent is a simple average across firms. We were comparing it with an employment-weighted share."

**[Second bullet]**

"Their firm size is 20.8 total workers. We were targeting 13, which had no clear source."

**[Third bullet]**

"Their closure estimates all control for firm size. Ours didn't."

**[Table, shaded rows]**

"The corrected calibration now fits these three closely, for example 21.4 workers per EPS firm against 20.8."

**[Table, other rows]**

"The rest is close, not exact: small plants 0.75 against 0.70, average size 8.1 against 7.5, and plants with 50 or more workers 1.8 percent against 2.1. The 8 percent exit rate is our assumption, and we still need to check it against official data."

**[Closure slope row]**

"One caution. The slope matches only on our calibration grid, which has 24 by 11 points. On a finer grid, 48 by 21, with the same parameters, it falls to about 0.05. That's within about one and a half standard errors of their estimate, but it isn't a clean match. Re-fitting it is our next step, and that could move our result."

**[If asked: 13 parameters]**

"We now have 13 parameters and 8 targets, so the targets can't pin down each parameter separately, and we haven't shown this is the only fit. That's why the robustness checks matter."

**[If asked: the COVID shock]**

"You suggested it could help identify parameters. That's where the closure slope comes from. It's only one target, and right now it's our most fragile one."

**[If asked: how the search ended]**

"We stopped it by hand once improvements became tiny, so this is the best fit we found, not a proven best. The loss is 0.034, against 0.64 for the old parameters."

**[If asked: parameters at their limits]**

"The size of productivity shocks is 0.051, right at the lower limit of 0.05 that we allowed. We need to check that in the robustness runs."

### Slide 35: Results: with corrected targets the gain is about +0.3%, at our kill line

**[Title]**

"This is what the corrections do to our answer."

**[Second card]**

"With the same quota and no size rule, net output rises by 0.33 percent. The last version gave 0.99 percent. You were right that bunching can raise the gain, but matching the data brings most of it back down."

**[Other cards]**

"Removing EPS completely lowers output by 7.2 percent. A 50 percent larger quota raises it by 3.7 percent."

**[Table, first three rows]**

"Without the size rule, fewer plants use EPS, 6 percent instead of 11. They're smaller, 14 workers instead of 22, and they rely on EPS much more. Manual-intensive plants fall from 11 percent to 8."

**[Table, last row]**

"We want to be clear about this row. Gross output falls by 0.9 percent. Net output rises because fixed, entry and recruiting costs fall by 5.5 percent. So the gain comes from saving costs, not from producing more."

**[Blue box]**

"The gain is 0.089 of a 50 percent quota expansion, or 0.101 on a finer grid, where the gain is 0.37 percent. That's at the one-tenth line we set in the proposal, and we're keeping that line. Since the answer depends on the grid, the robustness checks have to settle it. If it stays below, we refocus on the size of the quota. That would still be a finding: the size rule matters much less than the quota."

**[If asked: how the quota is allocated with no size rule]**

"A permit price clears the market, so the plants that value a worker most get one. We count the fee as a transfer, not a cost."

**[If asked: does the rule keep weak plants alive]**

"Total plants fall by only 0.9 percent, but manual-intensive plants fall by about a quarter. So it changes which plants survive more than how many. The Korean wage falls 1.7 percent. We haven't computed a separate aggregate productivity number yet."

**[If asked: why users got smaller]**

"In version 5, they got larger without the rule, from 15 to 25 workers. With the corrected targets that reversed, and we don't know why yet. So we don't rest our story on it."

**[If asked: which correction lowered the gain]**

"We changed all three at once and haven't separated them. We also haven't split the cost saving by source."

**[Hand over]**

"Donny will cover what we still need, and our assumptions."

## Donny

### Slide 36: Still to request: what the survey cannot tell us, and who holds it

**[Title]**

"Since we found the survey, you might ask whether we still need to contact anyone. We think yes, for four things."

**[Rows 1 and 2]**

"The survey covers only EPS users, under the 2019 caps. A real bunching test needs all plants and the current caps. The Ministry, HRD Korea and KEIS hold those records, so we'd ask for a table of counts, not plant records."

**[Row 3]**

"The 2021 survey wave has the closures behind our target, and it isn't public. Prof. Lee and Prof. Yang are both here at Yonsei."

**[Row 4]**

"Firms sit below their caps yet still want more workers, so we'd like to ask how rationing works in practice."

**[Blue box]**

"We wanted to explain this to you before contacting anyone. Is this the right request? And KEIS has a research data system that may need a faculty lead. Would that be possible?"

**[If asked: have you contacted anyone]**

"No. Nothing has been sent. We have a draft email to Prof. Lee and Prof. Yang, and a draft disclosure request to the Ministry."

**[If asked: what exactly the Ministry request says]**

"Manufacturing only, 2015 to 2024, by number of insured Korean workers: plants and workers with E-9 visas, all insured plants, and total caps. Aggregates only, and small cells can be masked."

### Slide 37: Assumptions: what we are assuming, checked against the survey

**[Title]**

"You warned us about assumptions we might not know we were making. Here they are, and now we can check several against data."

**[Row 1]**

"EPS workers cost about a Korean wage. The survey supports this: 96 percent, with dorm and meals. Our proposal quoted a higher figure, so this replaces it."

**[Rows 2 and 3]**

"Rationing. The same share of the cap works on average, but it's too strong across firms, and more than half of firms don't want more workers. These matter most."

**[Row 4]**

"We treat EPS and Korean manual workers as equally productive. Employers rate EPS workers at 74 to 96 percent, rising with experience."

**[Rows 5 and 6]**

"The cap applies to core Koreans in the model, but to all insured Koreans in the law. We also leave out the points ranking and permit limits."

**[Rows 7 and 8]**

"Korean labor is fixed with no population growth, and this is a steady-state exercise about output, not welfare."

**[Footer]**

"We also set a few numbers ourselves rather than estimating them: the discount factor, returns to scale, the persistence of productivity, and the size and length of the shock behind the closure slope."

### Slide 38: Next steps, and what we would like your feedback on

**[Left box]**

"Next, we run the robustness checks, including the closure slope on a finer grid. These decide the kill condition. We use the survey to make rationing more realistic, and we add its numbers on EPS productivity and costs. We'll add population growth if time allows."

**[Right box]**

"We have three questions for you. Can we contact Prof. Lee, Prof. Yang and the Ministry as planned? How should we model rationing? And if the gain stays below our line, is refocusing on the quota acceptable?"

**[Close]**

"Thank you. Literature search, data processing, coding and drafting were assisted by Claude, from Anthropic, and the team checked the results."

**[During questions]**

"Leave this slide up. Every symbol in the equations is defined here."
