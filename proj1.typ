#import "@preview/ilm:1.2.1": *
#set text(font: "New Computer Modern", lang: "en", size: 9pt)

// #show: ilm.with(
//   title: [MTH800 Project 1],
//   author: "Mustafif Khan | 501095413",
//   date: datetime.today(),
//   abstract: [],
//   bibliography: [],
//   figure-index: (enabled: false),
//   table-index: (enabled: false),
//   listing-index: (enabled: false),
//   table-of-contents: none
// )
#set math.equation(numbering: "(1)")
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
to show where each part is completed. The following content is `q1.py`.

#raw(read("q1.py"), lang: "Python")

When we run the program (`$ python3 q1.py`), we get the following results which were reorganized
in a table for a better reading experience.

#figure(
table(
  rows: 4,
  columns: 8,
  ..csv("q1_var.csv").flatten()
),
caption: [$"VaR"_99$ Results for all sample sizes]
)

#figure(
  table(
    rows: 4,
    columns: 8,
    ..csv("q1_es.csv").flatten()
  ),
  caption: [$"ES"_99$ Results for all sample sizes]
)

From the results from both tables of VaR and ES respectively, we can notice that generally (apart for $"ES"_99$ errors from second sample size to third for parametic) as the sample sizes increases the error decreases,
thus showing better accuracy. As shown in the code we used both the Shapiro Wilk test and the kstest (which is better for large sample sizes like ours) both are used to determine if the distribution is normal
from our hypothesis test, checking if the p-value for both test is greater than 0.05 for which both did.

We can also notice this in the following histograms:

#align(center)[
  #image("normality_check_1000000.png", width: 80%)
  #image("normality_check_10000000.png", width: 80%)
  #image("normality_check_100000000.png", width: 80%)
]

= Question 2
For question 2 we consider the distribution where $L ~ "Exp"(4)$.

== 1)
To compute the theoretical values for value at risk and expected shortfall for an exponential distrubution with $alpha$ and $lambda$, we have the following
formulas:

$
  "VaR"_(alpha)(L) = - ln(1-alpha)/lambda
$<var_exp>

$
  "ES"_(alpha)(L) = (1-ln(1-alpha))/lambda
$<es_exp>

From the question we are given $alpha=0.99$ and $lambda=4$ which will be plugged into @var_exp and @es_exp for value at risk and expected shortfall respectively:

$
  "VaR"_(0.99)(L) &= - ln(1-0.99)/4\
  &= 1.15
$

$
  "ES"_(alpha)(L) &= (1-ln(1-0.99))/4\
  &= 1.40
$

== 2-3) (a-c)

All of these parts are done in the program `q2.py` where each part is commented. Compared to
the first question the code has been much more organized.

#raw(read("q2.py"), lang: "Python")


When we run the program (`$ python3 q2.py`), we get the following results which were reorganized
in a table for a better reading experience.

#figure(
table(
  rows: 4,
  columns: 8,
  ..csv("q2_var.csv").flatten()
),
caption: [$"VaR"_99$ Results for all sample sizes]
)

#figure(
  table(
    rows: 4,
    columns: 8,
    ..csv("q2_es.csv").flatten()
  ),
  caption: [$"ES"_99$ Results for all sample sizes]
)

From our result we are able to see in this case the empirical results do much better compared to the parametric,
the opposite from question 1. From there we are able to see that the empirical results' errors go down as each sample size
increases thus increasing the accuracy while the parametrics' errors doesn't move much as sample size increases. The same
can also be said for Expected Shortfall as well.

To be able to view how the distribution looks like, consider the following histograms, which show that the distributions are exponential.

#align(center)[
  #image("var_es_plots_N_1000000.png", width: 80%)
  #image("var_es_plots_N_10000000.png", width: 80%)
  #image("var_es_plots_N_100000000.png", width: 80%)
]
