# Lalalander - lab 3 - variant 6

This is an project which demonstrates the process of lambda-calculus and
related tests. Although it is not the best structure for real-world lambda
calculus, it shows basic lambda calculus, the process of parse and definition
of some expressions.

## Project structure

- `lambcal.py` -- Defines elements related to lambda calculus, such as
  variables, constants, and parameters. Defines some expression bodies
  and conversion rules between them, and realizes the function of
  transforming defined expressions into lambda expressions.

- `lambcal_test.py` -- Some tests for `lambcal` and log output.

- `visu_factorial.py` -- Visualize the factorial computational process
  models.

- `visu_factorial_test.py` -- A test of the visual factorial
  computational process function.

## Features

- Defines expressions body.
- Defines conversion rules for expressions.
- Implements the visualization of computational process.

## Contribution

- Wu Chenyun (1329846782@qq.com) -- Implementation and Modification.
- Huang Yuting (hyut@hdu.edu.cn) -- Modification.

## Changelog

- 20.06.2022 - 2
  - Modification program and update README file.
- 19.06.2022 - 1
  - Update.
- 16.06.2022 - 0
  - Initial.

## Design notes

- Token list and some regular expressions are used, and some expression
  bodies and the quasi conversion rules between these expression bodies
  are defined to realize the parsing of tags and expressions.

- We visualized the factorial calculation and wrote it to the fsm file.

## Evaluation strategies

- Normal-order reduction: Continuing to apply the rule for β-reduction
  in head position until no more such reductions are possible. At that
  point, the resulting term is in head normal form. One then continues
  applying a reduction in the sub-terms from left to the right.

- Applicative order reduction: Firstly, applying the internal reductions
  and then only applying the head reduction when no more internal
  reductions are possible.

- Conversion: β-conversion represents the evaluation of a function on an
  argument. α-conversion is a technical device to change the names of
  bound variables.
