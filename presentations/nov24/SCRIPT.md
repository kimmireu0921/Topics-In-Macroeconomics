# Nov 24 script (slides 63–75)

Talking points from the speaker notes (`presentations/nov24/build.py`). Say them in your own words.

## Mimi

### Slide 63: EPS project: the new model and what it says

**Title**  
"Good afternoon. Today: the histogram you asked for, the new model in brief, and what it says."

### Slide 64: Your feedback, and what we changed

**Table**  
"Here is what you asked for and what we did. The main change: the 21 percent rule is gone, replaced by random eligibility, as you suggested."

### Slide 65: The histogram: EPS workers ÷ legal cap, plants with at least one EPS worker

**How to read**  
"Each pair of bars is a range: for example, the 40 to 50 percent pair shows the share of firms using between 40 and 50 percent of their legal cap. Orange is real firms from the 2019 survey, blue is our model, both under the 2019 caps and only firms with at least one EPS worker."

**Old rule and median**  
"The dashed line is last week's model: every plant at 21 percent of its cap. The dotted line is the survey median: half of real firms use less than 60 percent of their cap, half more. So the data clearly reject the 21 percent rule."

**Grey zones**  
"The two grey zones are where the model misses. Below 30 percent of the cap, the survey has 21% of firms and the model none. At or above the cap, the survey has 18 percent and the model 11, with none above the cap."

**Box**  
"The model matches the average, which we target. But it is too concentrated: it has no plants below 30 percent of their cap, where the survey has 21%, and none above the cap, where the survey has 11%."

**If asked: the spikes**  
"Many survey firms have a cap of 5, so one to four workers is 20, 40, 60 or 80 percent."

**If asked: why none below 30 percent**  
"Using EPS has a fixed cost in the model, so a plant that uses EPS hires several workers. We have not tested this yet."

## Benjamin

### Slide 66: What changed in the model since last week

**Title**  
"For those who were not here last week: here is exactly what changed. Before, every plant could use EPS, but only 21 percent of its cap. Now a random share of plants is eligible, and eligible plants can use their full legal cap, counted on all Korean workers as the law does."

**Why**  
"The data rejected the 21 percent rule: real firms use 60 percent of their cap on average, not 21. Random eligibility was one of the two fixes the professor suggested."

**Last row**  
"The headline result also changed. Last week, removing the link to size gained up to 0.19 percent. Now it gains nothing, because caps rarely bind once access is rationed. More on that at the end."

### Slide 67: The model (1/3): plants and today's EPS rules

**Bullets**  
"Each plant draws three things when it enters: its type, its productivity, and whether it is eligible for EPS. Eligibility is random, 22% of new plants, and that share adjusts until the quota is used. Eligible plants can hire up to their legal cap, counted on all Korean workers."

**Tables**  
"These are the legal caps. We use the 2024 schedule for today's economy and the 2019 schedule when we compare with the survey, because those firms faced the 2019 caps."

**If asked: why random**  
"The professor suggested it, and it matches the data: demand exceeds the quota, and which firm gets workers is partly luck in the points system."

### Slide 68: The model (2/3): output, costs and the plant's choice

**Left**  
"A plant combines core Korean workers with manual work, which can be done by a Korean manual worker or an EPS worker. Plants exit when the future is not worth it, and enter until entry pays."

**Right**  
"Korean manual workers are hard to find at small plants, so each one costs more than the wage: 2.7 times at a plant with no core Koreans, 1.1 times at 150. An EPS worker costs the wage, so it saves that extra cost."

**Footer**  
"The survey backs this: small firms fill less than half the Korean manual jobs they plan, but they do not pay Koreans more. The extra cost is unfilled jobs."

## Julian

### Slide 69: The model (3/3): equilibrium and the two experiments

**Table**  
"We compare today with two ways of allocating the same quota: a permit price open to any plant, and an equal limit for the same eligible plants. The equal limit removes only the link to size."

### Slide 70: Calibration: 13 parameters, 8 targets

**Table**  
"Every target has a source; the model fits all eight closely."

**Box**  
"One thing we do not match: how much more EPS firms closed after the 2020 stop. In our model, plants that use EPS are productive enough that a temporary cut does not push them out. We state this as a limitation."

## Sara

### Slide 71: Who uses EPS: 7.0% of plants (data 8.0%)

**Table**  
"This answers your concern that every firm wanted EPS workers. Now only the highlighted group uses them: about 7 percent of plants, against 8 percent in the data."

### Slide 72: An untargeted check: EPS firms by size

**Left**  
"Where EPS firms are by size: close to the survey."

**Right**  
"Their EPS share falls with size in both, but the model is too flat among the smallest firms."

**If asked: why flat at 36 percent**  
"Below about 20 workers the cap does not bind and all manual work is done by EPS workers. Then the EPS share is just the plant's share of manual work, which our production function fixes at about 36 percent at every size. In the data the smallest firms are more manual-heavy. Letting the manual weight vary with size would fix it; we report it as a gap."

## Donny

### Slide 73: Result: the link to size barely matters; access does

**Table**  
"Same quota, three ways. Removing the link to size changes nothing, under either cap schedule. Letting any plant buy permits raises net output by +0.39%."

**Box**  
"Size does not matter because caps rarely bind: only 1.6% of users are at their 2024 cap. A price helps because permits move to the plants that value them most. But the gain is the premium saved: if the premium is only higher pay, the gain is about zero."

**If asked: does the size rule keep weak plants alive**  
"In this model, no: the caps rarely bind. Whether a plant gets permits at all matters much more."

### Slide 74: Why: with a price, EPS workers move to mid-sized plants

**Top table**  
"Where EPS workers are, by core Korean workers. Today 31% are at plants with 30 or more core Koreans. With a price, they all move to plants with 5 to 29, where Korean manual workers are scarcest."

**Bottom table**  
"Two eligible plants, the median and the top 1 percent. Today both use EPS workers. With a price, neither does: for them an EPS worker saves less than the price."

**If asked: why not the smallest**  
"Using EPS has a fixed cost, which the smallest plants cannot cover at that price."

### Slide 75: What we assume, and our questions

**Left**  
"These four assumptions matter most for the result. The last one matters most: the gain is the premium saved."

**Right**  
"Three questions. Most important: is the model settled, so we can freeze it and write the paper? Second, since caps rarely bind, should the paper be about access rather than size? Third, should eligibility be redrawn over time?"

**Close**  
"Thank you. We worked with the AI assistant Claude (Anthropic), used for literature search, fact-checking, coding, model runs and drafting, in line with the course AI policy."
