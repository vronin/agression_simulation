# Premise
My friend and I had an interesting discussion about whether the labels "good" and "bad" are appropriate, specifically whether we can externally attach them to people based on limited information. The case in point was a scenario in which there are only two people who have attacked each other. In such a case, the labels "good" and "bad" could be assigned arbitrarily in the absence of information (for example) about who started the aggression.

As we discussed this, I pointed out two aspects:

- That "good"/"bad" are very binary definitions. It's more appropriate to have a scale (BTW, which is still too simplistic, but a bit better than a binary definition)
- I thought that even with limited information, you can figure out how well-behaved people are. The main idea for that was to build (based on existing information) a graph of attacks, with more aggressive/malevolent people being part of a more tightly coupled part of the graph, while less aggressive people being on a loosely coupled part of the graph.
# Simulation

As a result, I decided to build the following simulation. On one hand, it's complex enough to generate reasonably complex and realistic graphs. On the other hand, it's obviously extremely simple compared to real life.

## Simulation initialization:

Each person has coordinates, an age, and a malevolence factor.
The initial population has random coordinates, age, and if they are over 15, a random malevolence factor.

## Simulation turn

Each turn the following things happen:

- New people are born at random coordinates.
- People die.
- People move around.
- People come of age (at the age of 15, a malevolence factor is calculated). Malevolence is set to be a random number based on a Gaussian distribution with a mean equal to the average malevolence of the people around you.
- People age.
