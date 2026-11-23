# Nov 24 script (slides 63–74)

Talking points from the speaker notes (`presentations/nov24/build.py`). Say them in your own words.

## Mimi

### Slide 63: EPS project: the new model and what it says

**Title**  
"Good afternoon. Today: the histogram you asked for, the new model in brief, and what it says."

### Slide 64: Your feedback, and what we changed

**Table**  
"Here is what you asked for and what we did. The main change: the 21 percent rule is gone, replaced by random eligibility, as you suggested."

### Slide 65: The histogram: EPS workers ÷ legal cap, plants with at least one EPS worker

**Chart**  
"Orange is the survey, blue the model, both under the 2019 caps and only plants with at least one EPS worker. The dashed line is our old 21 percent rule: the data clearly reject it."

**Box**  
"The model matches the average, which we target. But it is too concentrated: it has no plants below 30 percent of their cap, where the survey has 21%, and none above the cap, where the survey has 11%."

**If asked: the spikes**  
"Many survey firms have a cap of 5, so one to four workers is 20, 40, 60 or 80 percent."

**If asked: why none below 30 percent**  
"Using EPS has a fixed cost in the model, so a plant that uses EPS hires several workers. We have not tested this yet."

## Benjamin

### Slide 66: The model (1/3): plants and today's EPS rules

**Bullets**  
"Each plant draws three things at entry: its type, its productivity, and whether it is eligible for EPS. Eligibility is random, 22% of new plants, and that share adjusts until the quota is used. Eligible plants can hire up to their legal cap, counted on all Korean workers."

### Slide 67: The model (2/3): output, costs and the plant's choice

**Equations**  
"Output uses core workers and manual work; manual work is done by Korean manual workers or EPS workers. Korean manual workers cost more than the wage, most at small plants. Plants exit when staying is not worth it, and enter until entry pays."

**If asked: 2.7 times the wage**  
"It is not a wage. In the survey, small firms fill only 44 percent of planned Korean manual hires, while their Korean wages are no higher. The cost is unfilled jobs."

## Julian

### Slide 68: The model (3/3): equilibrium and the two experiments

**Table**  
"We compare today with two ways of allocating the same quota: a permit price open to any plant, and an equal limit for the same eligible plants. The equal limit removes only the link to size."

### Slide 69: Calibration: 13 parameters, 8 targets

**Table**  
"Every target has a source; the model fits all eight closely."

**Box**  
"One thing we do not match: how much more EPS firms closed after the 2020 stop. In our model, plants that use EPS are productive enough that a temporary cut does not push them out. We state this as a limitation."

## Sara

### Slide 70: Who uses EPS: 7.0% of plants (data 8.0%)

**Table**  
"This answers your concern that every firm wanted EPS workers. Now only the highlighted group uses them: about 7 percent of plants, against 8 percent in the data."

### Slide 71: An untargeted check: EPS firms by size

**Left**  
"Where EPS firms are by size: close to the survey."

**Right**  
"Their EPS share falls with size in both, but the model is too flat among the smallest firms."

## Donny

### Slide 72: Result: the link to size barely matters; access does

**Table**  
"Same quota, three ways. Removing the link to size changes nothing, under either cap schedule. Letting any plant buy permits raises net output by +0.39%."

**Box**  
"Size does not matter because caps rarely bind: only 1.6% of users are at their 2024 cap. A price helps because permits move to the plants that value them most. But the gain is the premium saved: if the premium is only higher pay, the gain is about zero."

**If asked: does the size rule keep weak plants alive**  
"In this model, no: the caps rarely bind. Whether a plant gets permits at all matters much more."

### Slide 73: Why: with a price, EPS workers move to mid-sized plants

**Table**  
"Today 31% of EPS workers are at plants with 30 or more core Koreans, where Korean workers are easy to find. With a price, they all go to plants with 5 to 29 core Koreans, where Korean manual workers are scarcest."

**If asked: why not the smallest**  
"Using EPS has a fixed cost, which the smallest plants cannot cover at that price."

### Slide 74: What we assume, and our questions

**Left**  
"These four assumptions matter most for the result. The last one matters most: the gain is the premium saved."

**Right**  
"Three questions. Most important: is the model settled, so we can freeze it and write the paper? Second, since caps rarely bind, should the paper be about access rather than size? Third, should eligibility be redrawn over time?"

**Close**  
"Thank you. We worked with the AI assistant Claude (Anthropic), used for literature search, fact-checking, coding, model runs and drafting, in line with the course AI policy."
