# ⭐ 2026 Statistics Bootcamp for Systems Engineering

![Banner Image](docs/image_banner.png)


Welcome to our Github Repository for the **Statistics Bootcamp** for Cornell University Systems Engineering Program!

- Last Updated: Winter 2026
- Maintainer: Tim Fraser <tmf77@cornell.edu>

---

## Table of Contents

- [Read: Syllabus](docs/syllabus.md)
- [Read: Earn Your Certificate](docs/certificate.md)
- [Read: List of Modules](#modules)
- [Use: CANVAS course site](https://canvas.cornell.edu/courses/75015)

---

## Program Highlights

- 🎥 **Learn statistics and probability through short online modules**, complete with videos and instructor office hours.

- 🎛️ **Customize your bootcamp path**: choose from >15 modules to refresh skills or learn brand-new ones.
Most students complete >5, but you can tackle all modules if you want.

- 📚 **Module options include**: Intro to Statistical Coding, Descriptive Statistics & Distributions, Difference of Means (t-tests), Probability, Simulation, Optimization, Calculus for Probability & Statistics, and more.

- 🐍📊 **Choose your coding environment**: every module includes R and Python scripts, walkthrough videos, and repeatable practice quizzes.

- 🔁 **No grades**: instead, use optional, unlimited-attempt quizzes to check your understanding as you go.

- 🏅 **Earn a Statistics Bootcamp Certificate** by completing quizzes across the modules you select.
Use the certificate to show employers or instructors that you’re trained in core statistical methods.

- Read the [**Syllabus**](docs/syllabus.md) for more details!

---

## Modules

This Stats Bootcamp is made up of several modules, which you may progress through at your own pace, and in your preferred order. Some may be less necessary for you, and you can skip these.

### ⬜ START HERE

- 🧮 Getting Started
- 💻 [A. Statistical Coding](A/)

### 🟦 Path 1: Descriptive Statistics

- 📊 [B. Descriptive Statistics](B/)
- 📈 [C. Visualizing Distributions](C/)
- 💻 [D. Data Wrangling](D/)

### 🟨 Path 2: Inferential Statistics

- 🎲 [E. Sampling & Confidence Intervals](E/)
- 📏 F. Hypothesis Testing & Significance
- 📊 [G. Difference of Means (t-tests)](G/)
- 📊 [H. Analysis of Variance (ANOVA)](H/)
- 📊 [I. Crosstabulation (Chi-squared)](I/)
- 📊 [J. Correlation (Pearson's r)](J/)
- 📊 [K. Regression](K/)
- 📤 [L. Prediction & Simulation](L/)

### 🟥 Path 3: Math for Statistics

- ➗ [M. Calculus](M/)
- 🎲 [N. Probability Rules](N/)
- 🔢 [O. Probability Distributions](O/)
- ↕️ [P. Optimization](P/)

### 🟧 Part 4: Data Science for Statistics

- 🔄 [Q. Functions, Iteration, Loops, and Callbacks](Q/)
- 📦 [R. Using GitHub for Version Control](R/)
- 🔢 [S. TBD](S/)

---

Here are several **recommended** routes through our modules:

```mermaid
flowchart TD


subgraph p0["START HERE"]
    Z["Getting<br>Started"]
    A["<b>A</b><br>Statistical Coding"]
end

subgraph p4["Path 4: Data Science for Statistics"]
    Q["<b>Q</b><br>Functions, Iteration,<br>Loops, & Callbacks"]
    R["<b>R</b><br>Github for<br>Data Science"]
    S["<b>S</b><br>Calculus with Statistical Coding!"]
end

subgraph p3["Path 3: Math for Statistics"]
    M["<b>M</b><br>Calculus"]
    N["<b>N</b><br>Probability Rules"]
    O["<b>O</b><br>Probability Distributions"]
    P["<b>P</b><br>Optimization"]
end

subgraph p2["Path 2: Inferential Stats"]
    E["<b>E</b><br>Sampling &<br>Confidence Intervals"]
    F["<b>F</b><br>Hypothesis Testing &<br>Significance"]
    G["<b>G</b><br>Difference of Means (t-tests)"]
    H["<b>H</b><br>Analysis of Variance (ANOVA)"]
    I["<b>I</b><br>Crosstabulation<br>(Chi-squared)"]
    J["<b>J</b><br>Correlation<br>(Pearson's r)"]
    K["<b>K</b><br>Regression"]
    L["<b>L</b><br>Simulation"]
end

subgraph p1["Path 1: Descriptive Stats"]
    B["<b>B</b><br>Descriptive Statistics"]
    C["<b>C</b><br>Visualizing Distributions"]
    D["<b>D</b><br>Data Wrangling"]
end



Z --> A
A --> B --> C --> D
A --> E --> F --> G --> H --> I
F --> J --> K --> L
A --> M --> N --> O --> P
A --> Q --> R --> S


%%class Z,A path0;
%%class B,C,D path1;
%%class E,F,G,H,I,J,K,L path2;
%%class M,N,O,P,Q,R path3;

class p0 path0;
class p1 path1;
class p2 path2;
class p3 path3;
class p4 path4;

classDef path0 fill:#D3DEFB,stroke:#FFFFFF;
classDef path1 fill:#648FFF,stroke:#FFFFFF;
classDef path2 fill:#FFB000,stroke:#FFFFFF;
classDef path3 fill:#FE6100,stroke:#FFFFFF;
classDef path4 fill:#fba835,stroke:#FFFFFF;


```

---

![](image_icons.png)

---

← 🏠 [Back to Top](#Table-of-Contents)
