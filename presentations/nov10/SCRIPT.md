# Nov 17 script (the Nov 10 slides, presented Nov 17)

Generated from the deck's speaker notes. These are talking points: the syllabus says not to read from a script or the slides word for word, so learn each point and say it in your own words. "If asked" entries are backup answers, used only if the topic comes up. Presenters: Sara 39–44, Mimi 45–49 and 62, Julian 50–53, Benjamin 54–61.

### Slide 39: EPS project update: understanding the baseline

Presenter: Sara

**[Title]**

"Good afternoon. Last time you asked us to understand the baseline model before running more experiments. The model has not changed since then. Today we show how it behaves."

**[Plan]**

"First a short refresher on the model and our data, including a check of where every target comes from. Then who uses EPS, whether the limit binds, why removing the size rule does not make large plants grow, and the checks you asked for."

### Slide 40: The model (1/2): what a plant makes, and what its workers cost

Presenter: Sara

**[Equation 1]**

"A plant has productivity s. It needs core Korean workers h and manual work. Manual work can be done by a Korean manual worker or an EPS worker, one for one. Light plants put almost no weight on manual work; manual-intensive plants put a lot."

**[Equation 2]**

"Korean manual workers cost more than the wage, most of all at small plants. At a plant with no core Koreans the cost is 1.92 times the wage; at 150 it is 1.29. An EPS worker costs the wage, so it saves that premium."

**[If asked: how many parameters]**

"13 parameters and 8 targets, so it is not exactly identified target by target."

### Slide 41: The model (2/2): the size rule, the experiment, entry and exit

Presenter: Sara

**[Rule and experiment]**

"Today a plant can have EPS workers up to a share theta of its legal cap, and theta is the same for every plant. In our experiment the cap is gone and every plant pays the same permit price p. Theta or p adjusts so the quota is used."

**[Entry and exit]**

"Plants close when the future is not worth it, and new plants enter until entry is worth its cost. That pins down the wage. Korean labor and the quota are fixed."

**[Box]**

"One simplification: our cap counts core Koreans only, while the law counts all Korean workers. We will change that for next time."

### Slide 42: Our data: what each source covers, and how we used it

Presenter: Sara

**[Title]**

"Before the results, here is every data source, the sample, and the rules we used to build each number."

**[Rows]**

"The census gives plant sizes. Some headcounts are hidden in size bands, so we give each hidden plant the average of its band. The survey covers only firms that use EPS, in 2019. Lee, Peri and Yang give the closure evidence. The Ministry and Statistics Korea give the EPS totals and the exit rate."

**[If asked: why 2024]**

"It is the latest year in the census, and it matches the 2024 caps in the model."

### Slide 43: Checking our targets: two had no source, so we replaced them

Presenter: Sara

**[Title]**

"We traced every calibration target to its source. Two had none: the EPS share of workers and the share of plants using EPS were rough figures from our first model. The exit rate was an assumption."

**[Table]**

"Here are the sourced values. The EPS share of workers barely changes. The share of plants using EPS falls from 10 to 8 percent, and the exit rate from 8 to 6.6 percent. Average size rises to 8.1 once we count the plants the census masks and the largest plants."

**[Box]**

"Today's results use the old targets. The model has too many EPS users and too much exit against the new values, so we are recalibrating. We will bring the new results next week."

**[If asked: are workplaces and plants the same]**

"Not exactly. The Ministry counts workplaces and the census counts establishments. They are close, but the 8 percent may be off slightly."

### Slide 44: Your questions from last time, and the short answers

Presenter: Sara

**[Title]**

"Here is what you asked, with our short answers. The next slides show each one."

**[Correction]**

"First, a correction. The EPS share of 36.9 percent is the average, across firms using EPS, of EPS workers divided by that firm's workers. It is not the share in the economy. Slide 47 shows all three meanings."

**[Correction on the cap]**

"We also said firms can go above the cap by request, by 3 to 6 workers. We have no source for that. In Dong, Lee and Yang, 3 to 6 is the maximum number of new permits. We've asked the Ministry for the rule."

**[Correction on the survey]**

"Earlier we said every user wants more. In the model that is 98%. In the survey it is 44%."

**[Hand over]**

"Mimi will now show who uses EPS in the model, and the policy functions."

### Slide 45: Who uses EPS: manual-intensive plants, and no light plants

Presenter: Mimi

**[Title]**

"You asked why only about 10 percent of plants use EPS. The answer is the two plant types."

**[Table]**

"89% of plants are light: they have almost no use for manual work, so they hire no manual workers and none uses EPS. The other 11% are manual-intensive, and 99% of those use EPS."

**[Why box]**

"An EPS worker costs less than a Korean manual worker because it saves the premium. A plant uses EPS if that saving beats the fixed cost. Light plants would not use EPS even if it were free."

**[Bottom box]**

"So the 10 percent mostly comes from a number we calibrate, not from the cap. The sourced value is 8 percent of plants, so the model has slightly too many users; the recalibration fixes that."

**[If asked: is 89 percent with no manual workers realistic]**

"Probably not literally. It is a two-type simplification. Real plants have some manual work. We need the data to say how far off it is."

**[If asked: why hire EPS workers if they cost the same and are less productive]**

"Because Korean manual workers only come at a higher price, and the premium in equation 2 is that price. A Korean manual worker costs about 1.6 times the wage at a plant with 7 core Koreans and 1.3 times at 150. Employers rate EPS workers at 74 to 96 percent of a Korean worker. Even at 74 percent, an EPS worker costs about 1.35 times the wage per unit of work: still cheaper at small plants, but not at large ones. So lower productivity would make large plants want EPS even less, which supports our result."

### Slide 46: Do model users match the data? The shape, but not the small end

Presenter: Mimi

**[Title]**

"You asked us to check that the model's EPS users look like the data's. Here they are by total workers, under the 2019 caps, when the survey was done."

**[Right columns]**

"The EPS share falls with size in both, from about half at the smallest firms to about 5 percent. We only targeted the average, so this shape is a check."

**[Left columns]**

"The miss is in where users are: 55% of the model's EPS firms are under 10 workers, against 41% in the survey, and too few are at 20 to 49. From 20 workers up, the model's EPS shares are also lower, for example 18% against 26% at 20 to 49."

**[If asked: why the miss]**

"We don't know yet. One theta for every plant may be the reason, but we haven't tested it."

### Slide 47: Three different “EPS shares”, in the data and in the model

Presenter: Mimi

**[Title]**

"You asked us to define the EPS share. There are three, and they measure different things."

**[Table]**

"The first, 36.9 percent, is the average across EPS firms of each firm's EPS share. The second, about 5 percent, is EPS workers in all manufacturing. It sets the quota. The third, 8 percent, is the share of plants that use EPS. The model has 10.7%, because it was calibrated to the old 10 percent."

**[Box]**

"They are consistent. EPS plants are about two and a half times the average size, so they hold about a fifth of all workers. A quarter of those workers are EPS workers, which gives about 5 percent of all workers."

### Slide 48: Policy functions for manual-intensive plants

Presenter: Mimi

**[Title]**

"These are the policy functions you asked for. Each panel has productivity on the horizontal axis, for manual-intensive plants. Blue is the current rule. Orange is what the plant would choose with no limit and free permits."

**[Left panel]**

"EPS workers are held low by the limit under the current rule. The median plant has 3, and the top 1 percent plant has 11. With no limit they would want 14 and 357."

**[Middle panel]**

"This is the key panel. The median plant hires no Korean manual workers. A top 1 percent plant hires 156. So for large plants, the next manual worker is Korean. With no limit, all of them switch to EPS."

**[Right panel]**

"Total workers. With no limit, the top 1 percent plant grows from 317 to 479, and the median from 10 to 19. Keep in mind the orange line is not an equilibrium, as the next slide shows."

**[If asked: why EPS falls to zero at the right]**

"Past 300 core Koreans a plant is not eligible under the current rule."

**[If asked: why the steps]**

"Productivity is on a grid, and the plan changes in steps. The caps also create jumps. Slide 60 checks the grid."

### Slide 49: Who is held back: almost every user, by the quota, not the cap

Presenter: Mimi

**[Title]**

"You asked who is constrained, and where they would be without the limit."

**[Cards]**

"Optimal scale is the size a plant would choose with no limit. Light plants are already there. 98% of EPS users would hire more, and 82% are at their limit. But the limit is theta times the cap, with theta 0.21, so no plant reaches the legal cap itself."

**[Box]**

"So the quota does the limiting. Without any limit plants would be 1.4 to 1.9 times larger, but they would want 8.5 times the quota."

**[If asked: 82 versus 98 percent]**

"The others sit just below their limit but would still hire more. Under the 2019 caps, 91% are at the limit."

**[If asked: is theta realistic]**

"Theta is a simple stand-in for rationing: every plant gets the same share of its cap. Real rationing uses a score and a cut-off."

**[Hand over]**

"Julian will now show whether the cap binds, in the survey and in the model."

### Slide 50: Is the cap binding? Yes for 2019 caps, barely for 2024 caps

Presenter: Julian

**[Title]**

"You asked how many firms are at or near the cap, by size, under the 2019 and 2024 caps."

**[Blue bars]**

"Blue is firms at or above the 2019 cap, 18% overall. As you said, that is not small."

**[Orange bars]**

"Orange adds what they say they would hire with no limit: 24% would go past the 2019 cap, at every size."

**[Green bars]**

"Green applies the 2024 caps, which are much higher, to the same firms and answers. Then about 1% would go past. So after 2024 the legal cap may barely bind."

**[If asked: how firms are above the cap]**

"We can't fully explain it. Root industries may hire 20 percent more, and the public file doesn't show which firms those are. We've asked the Ministry."

### Slide 51: Firms far below the cap still want more: something else limits them

Presenter: Julian

**[Title]**

"You also asked whether the caps bind at all, since firms use only 62% of their cap on average."

**[Table]**

"42% of firms use less than half their cap. If the cap were what limits firms, those firms should not want more. But 41% of them do, almost as many as at the cap, 50%."

**[Box]**

"So for most firms something else limits them. That matches the model, where the quota limits plants, not the cap. And 56% of firms want no more workers at all."

**[Why it matters]**

"You said that if no one is constrained there is no paper. Under the 2019 caps there clearly is a constraint. Under the 2024 caps we need newer data."

### Slide 52: How much do plants want? Far more in the model than the survey

Presenter: Julian

**[Title]**

"Here is the same comparison in levels: what plants have and what they want. Log scale, 2019 caps in both."

**[Left panel]**

"In the model, wanted EPS workers rise steeply with size, to about 204 per plant at 101 to 300 Korean workers."

**[Right panel]**

"In the survey, they barely rise: about 22. What plants have now is similar at small sizes, and lower in the model at large ones."

**[Takeaway]**

"You warned us not to get too worked up when the survey contradicts an assumption, and stated wants could be low. But this is a large gap. In the model, an EPS worker is a perfect substitute for a Korean worker at a lower cost, so large plants would replace all their Korean manual workers. Firms don't say that. So the model's demand is probably too high."

**[If asked: what would fix it]**

"We haven't tried. Productivity differences or EPS workers being imperfect substitutes could lower it, but you advised us to keep the model simple, so we want to discuss it first."

### Slide 53: The real limit, cap or quota? The model assumes the quota

Presenter: Julian

**[Title]**

"In the model the quota always binds. Theta adjusts until total EPS demand equals the quota. We looked into whether that is true."

**[Table]**

"These are the announced E-9 quotas. A December 2024 report projected about 80,000 for 2024, half of the 165,000 quota. That is a projection, across all sectors, and we don't yet have the final number."

**[Right box]**

"At the same time, the Ministry's 2026 notice says firms with low scores get a waiting number. So the quota may bind in some rounds and sectors but not others. We can't tell yet."

**[Bottom box]**

"As you advised, we used the formal disclosure process with the Ministry. Those tables would show whether the cap or the quota does the limiting, and at what size. The law gives them 10 days, extendable by 10."

**[If asked: what if the quota does not bind]**

"Then theta would be 1 and only the legal cap would limit plants, and that would change our experiment. With the 2024 caps few firms reach the cap. That is why this is on our list of questions for you."

**[Hand over]**

"Benjamin will now explain why large plants barely grow, and the checks we ran."

### Slide 54: Why large plants barely grow: their next worker is Korean

Presenter: Benjamin

**[Title]**

"You expected large, productive plants to be held back, so removing the rule should make them grow. Here is why that does not happen in our model."

**[Point 1]**

"Large plants already hire Korean manual workers. Once their EPS permits are used, the next worker is Korean. So the limit doesn't change what the next worker costs; it only saves money on workers the plant would hire anyway."

**[Chart]**

"The line is what one permit saves: the wage times the premium. It falls with core Koreans, because we assume recruiting is easier at large plants. The dashed line is the permit price. They cross at about 28 core Koreans."

**[Point 2]**

"Past that point a permit is not worth its price, so large plants drop EPS. Only a middle band of plants uses it."

**[If asked: what if EPS workers are less productive]**

"Employers rate them at 74 to 96 percent of a Korean worker. At 74 percent, EPS work costs about 1.35 times the wage per unit, more than a Korean manual worker at a large plant, about 1.29. So large plants would want EPS even less."

### Slide 55: The top 1% plant drops EPS and barely changes size

Presenter: Benjamin

**[Title]**

"Here is the top 1 percent plant in detail."

**[Rows 1 and 2]**

"Today it has 11 EPS workers. With a price it has none and hires more Korean manual workers instead. It goes from 317 to 328 workers."

**[Rows 3 and 4]**

"Why does it grow at all? At today's wage its price plan is exactly its plan with no EPS. So EPS plays no part. The growth comes from the wage, which is lower with a price because fewer manual-intensive plants survive."

**[Box]**

"Under today's rule the plant sits just past the 150 cap step to get the larger cap. That is the size rule making it a little bigger: bunching."

**[If asked: how precise are these sizes]**

"Sizes sit on a grid with steps of a few percent, so 308 against 317 is about one grid step."

### Slide 56: Three ways to share the same quota

Presenter: Benjamin

**[Title]**

"Last time's experiment changed two things at once. So we split it. Here are the three ways of sharing the same quota that we compare."

**[Table]**

"Today each plant gets a share theta of its cap. With a price, any plant can buy permits at 0.34. With an equal limit, permits are free and every plant gets the same 3.9 workers."

**[Box]**

"The equal limit removes the size link but keeps permits free, so comparing the two tells us what the charge does."

### Slide 57: A price raises net output; an equal limit raises gross output. Both gains are small

Presenter: Benjamin

**[Title]**

"Here are the results for the three."

**[Net and gross]**

"With a price, gross output falls to 99.1 but net output rises 0.33%. With an equal limit, gross output rises to 101.0, as you expected, but net output rises only 0.19%, or 0.09% on the finer grid."

**[Other rows]**

"With an equal limit more plants use EPS and most permits go to the smallest plants. A top 1 percent plant barely changes size in any version."

**[Box]**

"Both gains are small. A price is at our kill line and an equal limit is below it."

### Slide 58: Where the net gain comes from: fewer costly manual-intensive plants

Presenter: Benjamin

**[Title]**

"So where does the net gain come from? Net output is gross output minus real costs."

**[Table]**

"With a price, gross output falls by 0.9. But costs fall by about 1.2, and the biggest part is the fixed costs of running plants."

**[Box]**

"Those are manual-intensive plants that close when they must pay for permits. Each is expensive to run. So the size rule does keep some costly plants alive. That is your original question, and the answer is yes, but the effect is small."

**[If asked: what if the premium is just higher pay]**

"Then it is a transfer to Korean workers, not a cost, and the gain would be smaller. That is one of the assumptions we want your view on."

### Slide 59: Does the premium drive the result? The direction holds

Presenter: Benjamin

**[Title]**

"The premium is the assumption everything seems to depend on, and we can't measure it directly yet. So we varied it, holding everything else at our calibration."

**[Table]**

"Each row is a different slope. The flatter the premium, the larger a plant can be and still want EPS. Our value stops at about 28 core Koreans. The last row uses version 5's higher, flatter premium: about 400."

**[Key columns]**

"But gross output falls in all six rows. And a top 1 percent plant barely changes size, even when it keeps many EPS workers, as in the version 5 row."

**[Why]**

"The reason is equation (1). Manual work is k plus m, so EPS and Korean manual workers are perfect substitutes. A large plant replaces Korean workers rather than expanding, because the premium at large plants is small."

**[Honest limit]**

"These rows are not recalibrated, so the levels don't match the targets. They show direction only. To really test this we would need to measure the premium by size, or relax the perfect-substitutes assumption, and we would like your view on whether that is worth it."

### Slide 60: The bumpy no-rule line was grid error, as you suspected

Presenter: Benjamin

**[Title]**

"You said the no-size-rule line should be smoother and to check for approximation error. You were right."

**[Chart]**

"Blue is last time's line. Orange uses a finer grid for productivity and plant size. It is much smoother."

**[Box]**

"Productivity moves in steps of about 5 percent, and plant size moves about three times as much, so a step is wider than our 8 percent bins. That makes the bumps."

### Slide 61: The bunching at the cap steps is real: it holds on every grid

Presenter: Benjamin

**[Title]**

"So is the bunching we showed also grid error? No."

**[Last columns]**

"The pile-up just past each cap step is 1.5 to 2 times the density just below it under today's rule, on every grid. With no size rule it stays near or below 1."

**[Roughness]**

"The no-rule line gets smooth on finer grids, from 0.68 to 0.22. Today's rule levels off near 0.6, because its jumps are real: they are the cap steps."

**[If asked: does the +0.33 change on this grid]**

"These runs hold prices fixed, so they check the shape, not the gain. The +0.33 percent is on the 24 by 11 grid; on 48 by 21 it is +0.37 percent."

**[Hand over]**

"Mimi will sum up and ask our questions."

### Slide 62: What we learned, and where we would like your advice

Presenter: Mimi

**[Left]**

"To sum up: who uses EPS comes mostly from the plant-type share. The quota, not the cap, does the limiting in the model, and something other than the cap limits most firms in the survey. Large plants barely grow without the size rule. And the gain is small."

**[Right]**

"We have four questions. Should we focus on the 2019 caps, which clearly bind, or the 2024 caps, which may not? Is this gain enough to continue, or should we refocus on the quota? Which comparison is right? And should we make EPS workers less attractive in the model? Firms in the survey want far fewer than the model says, and adding the dorm and meal costs the survey records would be a simple way to do it."

**[Bottom]**

"For next week we will recalibrate to the sourced targets, fix the cap to count all Korean workers, and follow up with the Ministry."

**[If asked: does the size rule keep weak plants alive]**

"Slightly. Today's rule keeps about 0.9 percent more plants than a price would, mostly manual-intensive plants that are costly to run."

**[Close]**

"Thank you. We worked with the AI assistant Claude (Anthropic), used for literature search, fact-checking, coding, model runs and drafting, in line with the course AI policy."
