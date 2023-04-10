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

## Taxonomy

This part will look at the genome of each organism and label it according to
the details in [characteristics.ods]("./characteristics.ods").

## Distribution

This part of the program will handle the distribution of food and other things
in the environment, It will also handle the movement of the organisms.

## Rendering

This part will render the simulation according to the state of the system.
This will be done using [pygame](https://pygame.org/), which is a library that
provides SDL bindings for python.
