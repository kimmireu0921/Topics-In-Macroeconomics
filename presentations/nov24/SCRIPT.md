# Nov 24 script (slides 63–78)

Generated from the speaker notes of the published slides (`presentations/nov24/build.py`).

## Mimi

### Slide 63: EPS project: the model, written up in full

**Title**  
"Good afternoon. Last week you asked us to test our 21 percent rule against the data, and to send you a complete write-up of the model. Today we do both."

**Plan**  
"First the test and what it told us. Then the full model, one slide per part. Then the calibration, the checks, and one main result."

### Slide 64: Your feedback last week, and what we changed

**Title**  
"Here is each comment from last week and what we did. The main change: the 21 percent rule is gone. Instead, plants are randomly eligible for EPS, and eligible plants can hire up to their full legal cap, counted on all Korean workers as in the law."

**Perfect substitutes**  
"We kept perfect substitutes for now, so that we change one thing at a time. With the full cap, the model already matches how much of their cap firms use. We come back to it at the end."

### Slide 65: The test you asked for: how much of its legal cap does each EPS firm use?

**Title**  
"You asked for a histogram: among firms with at least one EPS worker, the share of their legal cap they use. Orange is the survey, 772 firms in 2019."

**Survey**  
"Firms are spread out. The median firm uses 60% of its cap. Only 17% are at or below 21 percent, and 18% are at or above the cap. So the data do not support our old rule, which put every plant at 21 percent. The dashed line shows where it was."

**Model**  
"Blue is the new model. Eligible plants may use their whole cap. Small plants whose manual work is below their cap use less, so the model spreads out too: 62% on average and 11% at the cap. The average is a target; the shape is not. One gap: the survey has firms below 30 percent of their cap, the model almost none."

**If asked: the spikes**  
"Many survey firms have a cap of 5. One, two, three or four workers is 20, 40, 60 or 80 percent."

**If asked: over 100 percent**  
"11% of survey firms are above their cap. The model cannot produce that. They may have been counted on a different date, or have extra permits; we asked the Ministry."

## Benjamin

### Slide 66: The model (1/5): plants, timing and what is fixed

**Plants**  
"This is a Hopenhayn model. When a plant enters it draws three things that never change: its type, light or manual-intensive; a permanent productivity level from a Pareto tail; and whether it is eligible for EPS. On top, productivity moves each year with a small shock."

**Timing**  
"Each year plants hire and produce. Then some exit by chance, and others close if the future is not worth it. New plants enter until entry is worth its cost; that pins down the wage."

**Fixed**  
"Korean labour and the EPS quota are fixed. We compare steady states."

**If asked: one sector?**  
"Light plants put almost no weight on manual work and never use EPS, so they act as the rest of the economy. The EPS question is about the manual-intensive plants."

### Slide 67: The model (2/5): output and labour costs

**Equation 1**  
"A plant combines core Korean workers with manual work. Manual work can be done by a Korean manual worker or an EPS worker, one for one. Manual-intensive plants put much more weight on manual work."

**Equation 2**  
"Korean manual workers cost more than the wage, most of all at small plants: 2.70 times the wage with no core Koreans, 1.09 at 150. An EPS worker costs the wage, plus a fixed cost of using EPS at all."

**Footer**  
"We measure welfare as net output: output minus the premium, the fixed costs and entry costs."

**If asked: 2.7 times the wage?**  
"It is not a wage. It is the full cost of getting manual work done with Korean workers at a plant with no core staff: unfilled jobs, overtime, recruiting. It is calibrated, not measured, and it matters for our result, which is why we show the result with the premium treated as pay."

### Slide 68: The model (3/5): today's EPS rules

**Equation**  
"Today's rule in the model: an eligible plant may hire EPS workers up to its legal cap, which depends on all its Korean workers, core and manual, as in the law. Plants with 300 or more Korean workers are not eligible. A plant that is not eligible hires none."

**Tables**  
"These are the two cap schedules. We use 2024 for today's economy and 2019 for the survey and the 2020 shock, because those firms faced the 2019 caps."

**Boxes**  
"Who is eligible is random: a share e of new plants. That stands in for the points system and waiting lists. e is not a parameter; it adjusts so the quota is used, like the 21 percent did before. It comes out at 22% of new plants."

**If asked: why random**  
"Your suggestion, and the data: firms far below their cap still want more, so access, not the cap, limits most of them. A random draw is the simplest way to ration access."

## Julian

### Slide 69: The model (4/5): the plant's problem

**Static**  
"Each year the plant chooses core workers, manual work, and how much of the manual work EPS workers do. An EPS worker is cheaper than a Korean manual worker, so an eligible plant that uses EPS uses as many as its cap allows, unless its manual work is smaller than the cap."

**Dynamic**  
"The value of a plant is today's profit plus the option to stay. The taste shock just makes exit smooth."

**Entry**  
"New plants enter until the expected value of entering equals the entry cost. The expectation is over type, productivity and eligibility."

### Slide 70: The model (5/5): equilibrium, and the two experiments

**Equilibrium**  
"An equilibrium is a wage, the variable that clears the quota, an entry mass and a distribution of plants, such that plants optimize, entry is free, and both Korean labour and the quota are fully used."

**Table**  
"Today, eligible plants hire up to their cap, and the eligible share clears the quota. In the price experiment any plant can buy permits at a price p that clears the same quota. In the equal-limit check, the same lucky plants are eligible, but each gets the same limit L, so only the link to size is removed."

**Box**  
"So the question is: with the same quota, does output rise if workers go to the plants that value them most?"

### Slide 71: Calibration: 4 parameters set, 13 chosen to fit 8 targets

**Title**  
"Four parameters are set from earlier work. Thirteen are chosen together so the model fits eight targets as closely as possible."

**How to read**  
"The last column says which target mostly moves each parameter. For example, the manual-intensive share of entrants mostly sets how many plants use EPS."

**If asked: 13 for 8**  
"It is not exactly identified one by one; we minimize the sum of squared percentage gaps."

## Sara

### Slide 72: Calibration: targets, sources and fit

**Table**  
"These are the eight targets, the data, the model, and the source of each. One is new: the average share of its cap an EPS firm uses, from the survey."

**Box**  
"One thing we no longer target: how much more often EPS firms close after the 2020 stop. Lee, Peri and Yang find 0.15; our model gives 0.00. In the new model eligible plants keep their permits, so they are rarely close to closing. This is a gap we state openly."

**If asked: why did you drop it**  
"The best of 256 random parameter draws all gave nearly zero, so keeping it would only pull the other targets off. It was also fragile in the old model."

### Slide 73: A check we did not target: which EPS firms, and how reliant on EPS

**Left**  
"Where EPS firms are, by total workers: blue is the model, orange the survey."

**Left, read**  
"Where EPS firms are by size is close: most are under 20 workers in both."

**Right**  
"The EPS share of workers at those firms, by size. We target only the averages, so the shape is a check. Both fall with size, but the model is too flat among small firms: it does not give the smallest firms the very high EPS shares the survey shows."

**If asked: why too flat**  
"In the model, a small eligible plant fills its manual work with EPS workers up to its cap, and small caps are low. In the survey the smallest firms rely on EPS for about half their workers."

### Slide 74: Who uses EPS today, in the new model

**Table**  
"The highlighted row is who uses EPS: manual-intensive plants that drew eligibility. Light plants never use it. Manual-intensive plants without eligibility do their manual work with Korean workers at a premium."

**Exit**  
"Exit rates are similar across groups, 6.5 to 6.9 percent: eligibility helps a plant, but not enough to change much who closes. That is also why the closure slope is near zero."

## Donny

### Slide 75: Main result: the link to size barely matters; who gets access does

**Title**  
"Here is the main result, and it changes how we see our question. We compare steady states with the same quota, allocated in different ways."

**Equal limit**  
"First row: keep the same eligible plants but give each the same limit, so there is no link to size. Net output does not change, under either cap schedule. The reason is that the caps rarely bind: only 1.6% of EPS users are at their 2024 cap. What limits plants is access, not size."

**Price**  
"Second row: let any plant buy permits at a price p that uses up the same quota. Net output rises by +0.39% with the 2024 caps as the baseline, +0.33% with 2019. Workers move to the plants that value them most."

**Caveat**  
"Last column: the gain comes from saving the extra cost of Korean manual workers at plants that are short of them. If that extra cost is only higher pay, not a real cost, the gain is about zero, +0.02%."

**Scale**  
"For scale, EPS as a whole adds about 5.8% of net output."

**If asked: does the size rule keep weak plants alive**  
"In this model, no: the caps rarely bind, so tying permits to size changes almost nothing. Whether a plant gets permits at all matters much more."

### Slide 76: Why: with a price, EPS workers move to mid-sized plants

**Left**  
"Two eligible plants, the median and the top 1 percent, today and with a price. Today both use EPS workers. With a price, neither does: for them an EPS worker saves less than the price."

**Right**  
"So where do the workers go? Today 31% of EPS workers are at plants with 30 or more core Koreans, where a Korean manual worker costs only a little more than the wage. With a price, all of them go to plants with 5 to 29 core Koreans, where Korean manual workers are scarcest."

**If asked: why not the smallest**  
"Using EPS has a fixed cost. Plants with fewer than 5 core Koreans have too little manual work to cover it at that price."

**If asked: why exactly 100 Koreans**  
"The top plant keeps just over 100 Korean workers, which raises its 2024 cap from 35 to 40 EPS workers. That is the bunching at a cap step."

### Slide 77: What we assume, and what it could change

**Title**  
"Here are the assumptions that matter most for the result, why we keep them, and what each could change."

**Highlighted**  
"The one that matters most for the number is the premium. Our gain is the extra cost of Korean manual workers that a price saves. If that is only higher pay, the gain disappears."

**Perfect substitutes**  
"We kept perfect substitutes, to change one thing at a time. With the full cap, the model matches how much of their cap firms use on average."

**If asked: the 41 percent**  
"Survey firms below their cap that still want more are rationed in a way our model does not have: here, access is all or nothing."

### Slide 78: Where we are, and our questions

**Left**  
"To sum up. We dropped the 21 percent rule, after the test you suggested. Plants are now randomly eligible and may hire up to their full legal cap. The model fits the targets. The link to size barely matters; a price raises net output by +0.39%, if the premium is a real cost."

**Right**  
"Four questions. First, is the model settled? We would like to freeze it now and write the paper. Second, since the caps rarely bind, should our question be about access rather than size? Third, should eligibility stay random? And how should we treat the premium?"

**Close**  
"Thank you. We worked with the AI assistant Claude (Anthropic), used for literature search, fact-checking, coding, model runs and drafting, in line with the course AI policy."
