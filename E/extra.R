# Sampling distribution example

library(dplyr)

length(mtcars$mpg)

data = tibble(reps = 1:1000) %>%
  group_by(reps) %>%
  reframe(
    mu = mtcars %>% sample_n(size = 10) %>% with(mpg) %>% sd()
  )

data$mu %>% hist()
# as number of samples increases

