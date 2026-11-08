# Nov 10 script

Generated from the deck's speaker notes. Read the quoted lines aloud. "If asked" entries are backup answers, read only if the topic comes up. Presenters: Sara 39–41, Donny 42–45, Julian 46–48, Benjamin 49–52, Mimi 53.

### Slide 39: EPS project update: understanding the baseline

Presenter: Sara

**[Title]**

"Good afternoon. Last week you asked us to understand the baseline model before running more experiments. So today nothing in the model has changed. We'll show how it behaves."

**[Plan]**

"We start with a short refresher, then cover who uses EPS, whether the limit binds, and why removing the size rule does not make large plants grow. We also ran the checks you asked for."

### Slide 40: Refresher: the question, the model and the data

Presenter: Sara

**[Question]**

"A quick reminder. Korea's Employment Permit System, EPS, limits each plant's foreign workers according to its number of Korean workers. We ask whether that keeps weak plants alive, and how much output would change if the same quota ignored size."

**[Model]**

"It's a Hopenhayn model. A plant has productivity s and hires core Koreans h and manual workers. Manual work can be done by Koreans, k, or EPS workers, m. Korean manual workers cost a premium that is smaller at larger plants. Under the current rule, a plant can have up to a share theta of its legal cap. In the no-size-rule experiment, plants pay a price p instead."

**[Data]**

"The census gives plant sizes, the survey covers firms that use EPS, and Lee, Peri and Yang give closures after the 2020–21 stop in new arrivals. We've asked the Ministry for the rest."

**[If asked: how many parameters]**

"13 parameters and 8 targets, so it is not exactly identified target by target. Some come from the structure and the search over them."

### Slide 41: Your questions from last week, and the short answers

Presenter: Sara

**[Title]**

"Here is what you asked last week, with our short answers. The next slides show each one."

**[Correction]**

"First, some corrections to what we told you. The EPS share of 36.9 percent is the average, across firms using EPS, of EPS workers divided by that firm's workers. It is not the share in the economy, which is 5.5 percent, or the share of firms using EPS, which is about 10 percent. Slide 43 shows all three, in the model and the data."

**[Correction on the cap]**

"We also said firms can go above the cap by request, by 3 to 6 workers. We have no source for that. In Dong, Lee and Yang, 3 to 6 is the maximum number of new permits. We've asked the Ministry for the rule."

**[Correction on the survey]**

"On slides 31 and 37 we said every user wants more. In the model that is 98 percent."

**[Hand over]**

"Donny will now show who uses EPS in the model, and the policy functions."

### Slide 42: Who uses EPS: manual-intensive plants, and no light plants

Presenter: Donny

**[Title]**

"You asked why only about 10 percent of plants use EPS. The answer is the two plant types."

**[Table]**

"89% of plants are light: they have almost no use for manual work, so they hire no manual workers and none uses EPS. The other 11% are manual-intensive, and 99% of those use EPS."

**[Why box]**

"An EPS worker costs less than a Korean manual worker because it saves the premium. A plant uses EPS if that saving beats the fixed cost. Light plants would not use EPS even if it were free."

**[Bottom box]**

"So the 10 percent mostly comes from a number we calibrate, not from the cap. That is a weakness: nothing measures that share directly. It is in our Ministry request."

**[If asked: is 89 percent with no manual workers realistic]**

"Probably not literally. It is a two-type simplification. Real plants have some manual work. We need the data to say how far off it is."

**[If asked: why hire EPS workers if they cost the same and are less productive]**

"Because Korean manual workers only come at a higher price, and the premium in equation 2 is that price. A Korean manual worker costs about 1.6 times the wage at a plant with 7 core Koreans and 1.3 times at 150. Employers rate EPS workers at 74 to 96 percent of a Korean worker. Even at 74 percent, an EPS worker costs about 1.35 times the wage per unit of work: still cheaper at small plants, but not at large ones. So lower productivity would make large plants want EPS even less, which supports our result."

### Slide 43: Do model users match the data? The shape, but not the small end

Presenter: Donny

**[Title]**

"You asked us to check that the model's EPS users look like the data's. Here they are by total workers, under the 2019 caps, which is when the survey was done."

**[Right columns]**

"The EPS share falls with size in both, from about half at the smallest firms to around 5 percent at the largest. We only targeted the average, so this shape is a check."

**[Left columns]**

"The miss is in where users are. The model has 55% of EPS firms under 10 workers, against 41% in the survey, and too few at 20 to 49."

**[If asked: why the miss]**

"We don't know yet. The model's plant sizes under 10 come from a target for the share of very small plants. The survey covers EPS users only, so we can't test this on non-users."

**[Bottom table]**

"You asked us to define the EPS share. There are three. First, the average across EPS firms of each firm's EPS workers divided by its workers: 36.9 percent in Lee, Peri and Yang, 37.2% in the model, measured the same way. Second, EPS workers as a share of all manufacturing workers: 5.5 percent, which sets the quota in the model. Third, the share of plants that use EPS: about 10 percent, and 10.7% in the model."

**[If asked: where do 5.5 and 10 percent come from]**

"They are our calibration targets. We are still checking their sources and will confirm them."

### Slide 44: Policy functions for manual-intensive plants

Presenter: Donny

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

"Productivity is on a grid, and the plan changes in steps. The caps also create jumps. Slide 52 checks the grid."

### Slide 45: Who is held back: almost every user, by the quota, not the cap

Presenter: Donny

**[Title]**

"You asked who is constrained, and where they would be without the limit."

**[Cards]**

"Optimal scale means the size a plant would choose with no limit, at today's prices. Light plants, 89% of all plants, are already there. 98% of EPS users would hire more, so they are below it, and 82% are at their limit. But that limit is theta times the cap, and theta is 0.21. No plant reaches the legal cap. In the model, the quota does the limiting, and the legal cap decides how it is shared."

**[Table]**

"With no limit, plants would be 1.4 to 1.9 times larger. But total demand would be 8.5 times the quota, so this can't happen at the same quota. It is a measure of how much plants want EPS workers."

**[If asked: 82 percent versus 98 percent]**

"The others sit just below their limit but would still hire more. Part of this may be the grid for manual workers, and we haven't checked. Under the 2019 caps, 91% are at the limit."

**[If asked: who else is below optimal scale]**

"The 0.1% of plants that are manual-intensive but have 300 or more core Koreans, so they are not eligible for EPS."

**[If asked: is theta realistic]**

"Theta is a simple stand-in for rationing. It gives every plant the same share of its cap. Real rationing uses a score and a cut-off, and we kept the model simple as you advised."

**[Hand over]**

"Julian will now show whether the cap binds, in the survey and in the model."

### Slide 46: Is the cap binding? Yes for 2019 caps, barely for 2024 caps

Presenter: Julian

**[Title]**

"You asked how many firms are at or near the cap, by size, under the 2019 and 2024 caps."

**[Blue bars]**

"Blue is firms at or above the 2019 cap, 18% overall. As you said, that is not small."

**[Orange bars]**

"Orange adds what they say they would hire with no limit: 24% would go past the 2019 cap, and that holds at every size."

**[Green bars]**

"Green applies the 2024 caps, which are much higher, to the same firms and answers. Now about 1% would go past. So after the 2024 change, the legal cap may barely bind."

**[Box]**

"You also asked whether the caps bind at all, since firms use only 62% of their cap on average and 42% use less than half. If the cap were what limits firms, firms far below it should not want more. But 41% of them do, almost as many as at the cap, 50%. So for most firms something else limits them, like the quota, the points ranking or the limit on new permits per round. That matches the model, where the quota limits plants, not the cap. And 56% of firms want no more workers at all: they are at their optimal scale."

**[Why it matters]**

"This matters for our question. You said that if no one is constrained there is no paper. Under the 2019 caps there clearly is a constraint. Under the 2024 caps we need newer data. Firms may also have wanted more after 2019, and the quota or the score may still limit them."

**[If asked: then what limits them]**

"The survey can't tell us. The candidates are the national quota, the points ranking and the 3 to 6 new permits per round. The Ministry tables we requested would separate them."

**[If asked: how firms are above the cap]**

"We can't fully explain it. Root industries may hire 20 percent more, and the public file doesn't show which firms those are. We've asked the Ministry for the rules and the counts."

### Slide 47: How much do plants want? Far more in the model than the survey

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

### Slide 48: The real limit, cap or quota? The model assumes the quota

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

### Slide 49: Why large plants barely grow: their next worker is Korean

Presenter: Benjamin

**[Title]**

"You expected large, productive plants to be held back, so removing the rule should make them grow. Here is why that does not happen in our model."

**[Point 1]**

"Large plants hire Korean manual workers. Once its EPS permits are used, a large plant's next worker is Korean. So the limit doesn't change what the next worker costs. It only saves money on workers the plant would hire anyway, so it doesn't change the plant's size much."

**[Chart]**

"The blue line is what one permit is worth: the wage times the premium. It falls with core Koreans, because we assume recruiting is easier at large plants. The orange line is the permit price. They cross at about 28 core Koreans."

**[Point 2]**

"Past that point the permit is not worth its price, so large plants drop EPS. Only a middle band of plants uses it."

**[Point 3]**

"A top 1 percent plant goes from 11 EPS workers to none and stays about the same size. You noticed that the average EPS user gets smaller, from 21.6 to 13.8 workers. That is because large plants leave the group of EPS users, not because they shrink."

**[If asked: so why does gross output fall]**

"With a price, permits move away from small plants, which lose cheap workers and produce less, and large plants swap EPS workers for Koreans instead of growing. So gross output falls to 99.1. Costs fall more, from 21.0 to 19.9, so net output rises. In our model the size rule mainly raises costs rather than limiting output, because EPS and Korean manual workers are perfect substitutes."

**[If asked: what if EPS workers are less productive]**

"Employers rate them at 74 to 96 percent of a Korean worker. At 74 percent, EPS work costs about 1.35 times the wage per unit, more than a Korean manual worker at a large plant, about 1.29. So large plants would want EPS even less, and our result would get stronger."

**[If asked: isn't the premium the key assumption]**

"Yes, it is, and we don't measure it directly. Slide 51 tests other values."

### Slide 50: Splitting the experiment: the size link and the permit charge

Presenter: Benjamin

**[Title]**

"Last week's no-size-rule experiment changed two things at once: it removed the size link, and it charged for permits. So we split them. This is a new experiment, with no new features in the model."

**[New column]**

"Permits stay free, the quota stays the same, and every plant gets the same limit, 3.9 workers. The limit is set so the quota is used."

**[Gross row]**

"With a price, gross output falls to 99.1. With a free, equal limit, it rises to 101.0. So your expectation that gross output rises does hold for this version. But it comes from sharing permits differently, and we can't say the charge alone explains it."

**[Other rows]**

"With an equal limit, more plants use EPS, and 62% of EPS workers are at plants with 5 or fewer Koreans. That means more plants survive, and costs rise. So the net gain falls to +0.19%, or +0.09% on the finer grid."

**[Last row]**

"A top 1 percent plant doesn't grow in either version. Only with no limit does it reach 479, and that takes 8.5 times the quota. At the same quota, more for large plants means less for small ones."

**[Kill line]**

"Our kill line was 0.10 of the gain from a 50 percent larger quota. With a price we are at 0.09 to 0.10. With an equal limit, 0.02 to 0.05, below the line."

### Slide 51: Does the premium drive the result? The direction holds

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

### Slide 52: The bumpy no-rule line was grid error; the bunching result holds

Presenter: Benjamin

**[Title]**

"You said the no-size-rule line should be smoother, and to check for approximation error. Last week we blamed the grid, but both lines used the same grid, so that was not a real answer. So we tested it."

**[Chart]**

"Blue is last week's line. Orange uses a finer grid for productivity and for plant size. It is much smoother."

**[Why]**

"On last week's grid, productivity moves in steps of about 5 percent. Plant size moves about three times as much, so a step is wider than our 8 percent histogram bins. That makes bumps. So you were right: this was approximation error."

**[Table]**

"Roughness measures how much the line jumps between bins. For the no-rule line it falls from 0.68 to 0.22. For the current rule it stays around 0.6, because its jumps are real: they are the cap steps."

**[Last columns]**

"The step ratios barely move. Under the current rule plants pile up past each step, at about 1.6 to 2. With no size rule the ratio stays near or below 1. So the bunching result holds on every grid."

**[If asked: does the +0.33 change on this grid]**

"We haven't solved the full equilibrium on the finest grid. On the 48 by 21 grid it is +0.37 percent. These runs hold prices fixed, so they check the shape of the distribution, not the gain."

**[Hand over]**

"Mimi will sum up and ask our questions."

### Slide 53: What we learned, and where we would like your advice

Presenter: Mimi

**[Left]**

"To sum up: the 10 percent of users mostly comes from the plant type share. The quota does the limiting. Large plants barely grow. And the gain is small and depends on how permits are shared."

**[Right]**

"We have four questions. First, should the paper focus on the 2019 caps, which clearly bind, or the 2024 caps, which may barely bind? Second, is this gain enough to continue, or should we refocus on the quota, which matters much more? Third, which comparison is the right one? And fourth, you told us not to complicate the model, so is relaxing perfect substitutes worth it?"

**[Bottom]**

"Next we follow up on the Ministry request, contact Prof. Lee and Prof. Yang, and measure what we can."

**[If asked: does the size rule keep weak plants alive]**

"Only slightly. The current rule keeps about 0.9 percent more plants than a price would, and the exit rate is 8.08 against 8.02 percent. An equal limit would keep 2.3 percent more plants than today. So the gain comes mainly from lower costs, not from weak plants exiting."

**[Close]**

"Thank you. We worked with the AI assistant Claude (Anthropic), used for literature search, fact-checking, coding, model runs and drafting, in line with the course AI policy."
