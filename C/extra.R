# Let's visualize some distributions for use in our slides.
# This content is optional, but might be interesting.

library(ggplot2)
library(readr)
library(dplyr)

gapminder = read_csv("C/gapminder.csv")

# Way too many observations for a useful dotplot
ggplot() +
  geom_dotplot(data = gapminder, mapping = aes(x = gdpPercap))

# Try grouping by stems of $10 dollars of gdp per capita
gapminder = gapminder %>%
  mutate(stem = round(gdpPercap/10, 0)*10)

gapminder %>%
  arrange(stem, gdpPercap) %>%
  select(stem, gdpPercap) %>%
  group_by(stem) %>%
  summarize(leafs = paste0(round(gdpPercap, 1), collapse = ", "))


ggplot() +
  geom_histogram(data = gapminder, mapping = aes(x = gdpPercap), 
                 binwidth = 5000, color = "white")

ggplot() +
  geom_histogram(data = gapminder, mapping = aes(x = gdpPercap), 
                 binwidth = 10000, color = "white")

ggplot() +
  geom_histogram(data = gapminder, mapping = aes(x = gdpPercap), 
                 binwidth = 20000, color = "white")


ggplot() +
  geom_density(data = gapminder, mapping = aes(x = gdpPercap), 
               color = "white", fill = "steelblue") +
  scale_x_continuous(limits = c(0, 45000))

MASS::fitdistr(x = gapminder$gdpPercap, densfun = "normal")

probs = tibble(
  x = seq(from = 0, to = 45000, by = 1000),
  y = dnorm(x, mean= 7215, sd = 9854 )
) 

ggplot() +
  geom_density(data = gapminder, mapping = aes(x = gdpPercap), fill = "steelblue", color = "white") +
  geom_area(data = probs, mapping = aes(x = x, y = y), color = "azure", fill = "azure", alpha = 0.5) +
  scale_x_continuous(limits = c(0, 45000))


ggplot() +
  geom_boxplot(data = gapminder, mapping = aes(x = gdpPercap)) +
  scale_x_continuous(limits = c(0, 45000))



ggplot() +
  geom_boxplot(data = gapminder, mapping = aes(x = gdpPercap, group = continent, y = continent)) +
  scale_x_continuous(limits = c(0, 45000))

