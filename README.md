# stats_bootcamp

Welcome to our Github Repository for the **Statistics Bootcamp** for Cornell University Systems Engineering Program!

- Last Updated: Winter 2025
- Maintainer: Tim Fraser <tmf77@cornell.edu>

This Stats Bootcamp is made up of several modules, which you may progress through at your own pace, and in your preferred order. Some may be less necessary for you, and you can skip these.

# Bootcamp Pathways
Here are several **recommended** routes through our modules:

```mermaid
flowchart TD


subgraph p0["START HERE"]
    Z["Getting<br>Started"]
    A["<b>A</b><br>Statistical Coding"]
end

subgraph p3["Path 3: Math for Statistics"]
    M["<b>M</b><br>Calculus"]
    N["<b>N</b><br>Probability Rules"]
    O["<b>O</b><br>Probability Distributions"]
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
A --> M --> N --> O 


%%class Z,A path0;
%%class B,C,D path1;
%%class E,F,G,H,I,J,K,L path2;
%%class M,N,O,P,Q,R path3;

class p0 path0;
class p1 path1;
class p2 path2;
class p3 path3;

classDef path0 fill:#D3DEFB,stroke:#FFFFFF;
classDef path1 fill:#648FFF,stroke:#FFFFFF;
classDef path2 fill:#FFB000,stroke:#FFFFFF;
classDef path3 fill:#FE6100,stroke:#FFFFFF;



```

