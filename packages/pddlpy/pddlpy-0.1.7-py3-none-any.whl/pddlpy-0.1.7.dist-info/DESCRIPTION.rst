
A PDDL library that, by using an ANTLR 4 grammar to parse PDDL files, provides a very simple interface to interact with domain-problems.
This library publishes one object class whose API exposes methods for obtaining:

* The initial state.
* The goals.
* The list of operators.
* The positive and negative preconditions and the positive and negative effects.
* The _grounded_ states of a given operator (grounded variables, preconditions and effects).

This is enough for the user to focus on the implementation of state-space or plan-space search algorithms.

The development of this tool was inspired from Univerty of Edimburgh's Artificial Intelligence Planning course by Dr. Gerhard Wickler and Prof. Austin Tate. The terms used in this API (and the API itself) closely resembles the ones proposed by the lecturers.

As of today it supports Python 3 and .NET. While project name is `pddl-lib` to emphasize its language agnosticy each target library has its own name. For Python is `pddlpy`. For .NET the library is `pddlnet.dll`.

The orginal grammar file was authored by Zeyn Saigol from University of Birmingham. I cleaned up it, made it language agnostic and upgraded to ANTLR 4.





