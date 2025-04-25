library(arules)
library(arulesViz)

library(conflicted)

articles <- read.transactions("text-mining-project-data/clean/arm-data-clean.csv",
                              rm.duplicates = F,
                              format="basket",
                              sep=",")


rules = apriori(articles,
                parameter = list(support=0.15,
                                 confidence=0.6,
                                 minlen=2,
                                 maxlen=2),
                appearance = list(default="lhs", rhs="police"))

sorted_rules <- sort(rules, by="confidence", decreasing = T)
arules::inspect(sorted_rules)

plot(rules, method="graph")
