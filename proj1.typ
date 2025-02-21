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
#set math.equation(numbering: "1.")
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
to show where each part is completed. The following content is `q1.py`

#raw(read("q1.py"), lang: "Python")
#let terminal(
  title: none,                // Title for the terminal
  content,                    // The body content
  fill: black,                // Background color of the terminal
  text_color: white,          // Text color for the terminal content
  title_color: luma(240),     // Title bar text color
  title_bg_color: black,       // Title bar background color
  radius: 6pt                 // Corner radius
) = {
  let stroke = black + 1pt     // Border color and width

  // Outer box for the terminal
  box(stroke: stroke, radius: radius)[
    // Title bar (if title is provided)
    #if title != none {
      box(
        fill: title_bg_color,
        inset: 0.5em,
        radius: (top-left: radius, top-right: radius),
        width: 100%,
        align(center)[#text(fill: title_color)[*#title*]]
      )
    }
    // Terminal content area
    #box(
      fill: fill,
      inset: (x: 1em, y: 0.7em),
      radius: (bottom-left: radius, bottom-right: radius),
      width: 100%,
      text(fill: text_color)[#content]
    )
  ]
}

To get the results, we can run the program on the terminal:
\
#terminal(title: "Terminal", [
  ```bash
  $ python3 q1.py
  N = 1000000
    Normality confirmed: True
    VaR_99 Parametric: 8.975556669822536, Abs Error: 0.003486952299985191
    ES_99 Parametric: 9.992346866772403, Abs Error: 0.0032957942650142513
    VaR_99 Empirical: 8.972412832156806, Abs Error: 0.006630789965715422
    ES_99 Empirical: 9.982018640953951, Abs Error: 0.013624020083465638
  -
  N = 10000000
    Normality confirmed: True
    VaR_99 Parametric: 8.978946535236147, Abs Error: 9.708688637388718e-05
    ES_99 Parametric: 9.995559381058833, Abs Error: 8.327997858437186e-05
    VaR_99 Empirical: 8.977836858606143, Abs Error: 0.0012067635163788282
    ES_99 Empirical: 9.99396136390425, Abs Error: 0.0016812971331674476
  -
  N = 100000000
    Normality confirmed: True
    VaR_99 Parametric: 8.979114004714269, Abs Error: 7.038259174763084e-05
    ES_99 Parametric: 9.995786749743548, Abs Error: 0.0001440887061310292
    VaR_99 Empirical: 8.978653808056245, Abs Error: 0.0003898140662759175
    ES_99 Empirical: 9.995781538215402, Abs Error: 0.00013887717798510835
  -
  Plot saved as: var_es_comparison.png
  ```
])

To better visualize the results, and how the error changes across sample sizes increasing, consider the following diagram:

#figure(
  image("var_es_comparison.png"),
  caption: "VaR and ES Error Comparison across Sample Sizes"
)

We are able to see in bottom diagram that as the sample sizes increases all errors
are decreasing, thus becoming more accurate. We can also notice that for all sizes, the
least accurate measurement is the empirical calculation.
