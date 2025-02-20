#import "@preview/ilm:1.2.1": *

#show: ilm.with(
  title: [MTH800 Project 1],
  author: "Mustafif Khan | 501095413",
  date: datetime.today(),
  abstract: [],
  bibliography: [],
  figure-index: (enabled: false),
  table-index: (enabled: false),
  listing-index: (enabled: false),
  table-of-contents: none
)

#set heading(outlined: false, numbering: none)
// #let h(title) = { heading(outlined: false, level: 1, numbering: none, title)}

= Question 1

The problem provides us to consider $L ~ N(2, 9)$, to compute the theoretical value at risk
and expected shortfall for  a given $alpha$ of $L$, we use the following formulas:

$
  "VaR"_(alpha)(L) = mu + sigma Phi^(-1)(alpha)
$<theo_var>

$
  "ES"_(alpha)(L) = mu + sigma Phi(Phi^(-1)(alpha))/(1-alpha)
$<es_var>

== 1)
The theoretical value of $"VaR"_0.99(L)$ using @theo_var where we are given $mu=2$, $sigma=3$
and $alpha=0.99$:

$
  "VaR"_(0.99)(L) &= 2 + 3 Phi^(-1)(0.99)\
  &= 8.98
$

The theorical value of $"ES"_0.99(L)$ using @es_var with the mentioned given values is:


$
  "ES"_(0.99)(L) &= 2 + 3 Phi(Phi^(-1)(0.99))/(1-0.99) \
              &= 10.00
$

== 2-3) (a-c)

All of these parts are done at the same time in our Python program, which will have comments
to disect where each part is completed.
