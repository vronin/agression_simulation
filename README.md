# Premise

My friend and I had a discussion about whether it is appropriate to attach the labels "good" and "bad" to people based on limited information. The idea was that a good person doesn't offend or attack anyone first, while a bad person does. To prove that it's impossible to attach a label in this way, we used the example of a scenario in which two people are attacking each other. In such a case, the labels "good" and "bad" could be assigned arbitrarily, as there is no information about who started the aggression.

During the discussion, I mentioned two points:

- "Good" and "bad" are very binary definitions. It would be more appropriate to have a scale (which is still simplistic, but better than a binary definition).
- Even with limited information, you can still determine how well-behaved someone is. To do this, you can build a graph of attacks based on existing information, and more aggressive or malevolent people will end up in a more tightly coupled part of the graph, while less aggressive people will be on a loosely coupled part of the graph.

# Simulation

As a result, I decided to build the following simulation. On the one hand, it is complex enough to generate reasonably complex and realistic graphs. On the other hand, it is obviously extremely simple compared to real life.

BTW, a disclaimer: I haven't done any research on what is appropriate for a simulation. I am pretty sure there is a ton of literature on the subject. This one was just built in a couple of hours of spare time.

## Simulation initialization

Each person has coordinates, an age, and a malevolence factor. The initial population has random coordinates, age, and a random malevolence factor.

## Simulation turn

Each turn the following things happen:

New people are born at random coordinates.
People die.
People move around.
People come of age (at the age of 15, a malevolence factor is calculated). Malevolence is set to be a random number based on a Gaussian distribution with a mean equal to the average malevolence of the people around you.
People age.
Cop promotion and retirement happens
People attack each other.

## Cop promotion and retirement

There is a probability that people may become police officers at age 21 and they retire at age 50.

## Attack simulation

- Each person, based on their malevolence, decides whether or not to attack somebody. If they decide to attack, they randomly pick a person around them.
- The victim, based on their malevolence, may decide to counter-attack.
- If there is a cop in the vicinity, then the cop records this (who attacked whom) and may decide to counter-attack.
- With a small probability, a victim may die because of the attack.
- The records are the critical part of the simulation. I want to use them to try to reconstruct a hidden variable (malevolence).
