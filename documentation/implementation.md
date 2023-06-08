# Implementation

The program will have several parts.

## Genome encoding

This part of the program, will encode and decode the various features of the
organism such as the optimal temperature, whether its sexual or asexual, its
energy requirements, etc. The full details can be found in
[characteristics.ods]("./characteristics.ods").

The genome will also contain some code which will determine how it will react to
certain stimuli such as presence of food, other organisms, potential mating
partners, etc. This part will essentially determine the neural structure of the
organism.

The genome will be encoded as a hexadecimal number. And the offspring's genome
will be derived from the parent's genome by randomly selecting each digit randomly
for each digit and mutation are also applied.

Each digit of the genome represents a feature, as a hexadecimal number this means
each digit has 16 states.

```python
[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
```

## Neural network

This part of the program essentially determines the brain the of the organism.
It defines a class called `NeuralNetwork` which has methods for generating
neural networks from the genome of the organism and running it.

The network extracts the weights from the genome by first calculating the
number of connections required and then dividing and taking average of the
divided parts for each weight.

## Taxonomy

This part will look at the genome of each organism and label it according to
the details in [characteristics.ods]("./characteristics.ods").

## Distribution

This part of the program will handle the distribution of food and other things
in the environment, It will also handle the movement of the organisms.

Current it has a class called `World` which has various NumPy Arrays and
python Lists which represent the food distribution, Organsims distribution, etc.

## Rendering

This part will render the simulation according to the state of the system.
This will be done using [pygame](https://pygame.org/), which is a library that
provides SDL bindings for python.
