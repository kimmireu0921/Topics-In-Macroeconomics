---
title: "EPS project: points to discuss"
subtitle: "Sara Ambre Chekroune, Yitang Donny Chen, Mireu Kim, Julian Henry Raymundo, Zachary Benjamin Yoo · November 24, 2026"
---

**Questions that could still change the model** (we plan to freeze it after this discussion)

1. **Korean labour market.** Now there is one pool of Korean workers, *N*. Each plant splits its Koreans between core work *h* and manual work *k*, and the wage clears Σ(*h* + *k*) = *N*. Manual Koreans cost more at small plants only through the premium. *Should Korean manual workers instead be a separate, fixed pool with its own wage?* If so, the Ministry's 직종별사업체노동력조사 reports current workers and unfilled positions by occupation and plant size, with Korean and foreign workers separated.
2. **Low tail of cap use.** Among plants with at least one EPS worker, the survey has 21% below 30% of their cap; the model has none. *Add a taste shock to EPS hiring, or report this as a limitation?*
3. **Eligibility over time.** Eligibility is now a permanent random draw at entry; actual permits last about three years. *Keep it permanent, or redraw it over time?*

**Our plans for today's comments**

4. **Disciplining the premium.** The premium is not a wage: it is the cost of manual jobs that small plants cannot fill with Koreans. Evidence:
    - EPS survey (2019): the smallest firms leave 56% of planned Korean manual hires unfilled, against 11% at the largest, while Korean wages are flat across sizes (about 1.12 times EPS wages).
    - Ministry establishment survey (2026 H1), all manufacturing plants: the labour shortage rate is 4.0% at plants with fewer than 5 regular workers, 3.0% at 10–29, and 2.0% at 100–299.

    *Plan:* fit the premium's decline with size (ξ) to these patterns. *Is this a reasonable discipline, or is there a standard approach in the literature?*
5. **Parameters equal to targets.** Today: 13 parameters, 8 targets. *Plan:* set about five externally (returns to scale, persistence, discount factor, exogenous exit, entry cost) and add targets such as the premium's decline with size. *Which would you set externally?*
6. **Equal limit and cap tilt.**
    - The equal limit is small but not zero: −0.0021% under the 2024 caps (limit of 45) and −0.0013% under the 2019 caps (limit of 14). Only 1.6% of EPS users are at their 2024 cap.
    - *Plan:* run your tilt experiment (larger caps for small plants, smaller for large ones) and report output along the tilt, together with the variable that clears the quota (*e*, *p* or *L*) in each case.
    - The permit price is the same under both cap schedules (*p* = 0.17, about 18% of the wage), because the price economy has no caps. The +0.33% vs +0.39% gap comes from the two baselines.
7. **Framing.** The caps rarely bind, and a price (open access) raises net output by 0.39%. *Should the paper ask about access to permits rather than size, or keep size as the question with the tilt experiment as the test?*
