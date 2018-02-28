# Load the libraries
library(arules)
library(arulesViz) 
library(lubridate)

master_tran<-read.csv('C:\\Projects\\Hasbro\\sample1.csv')
master_tran['bill_date_new']<- as.Date(master_tran$bill_date)
#master_tran['Year'] <- year(master_tran$bill_date_new)

cols <- c("customer_id","bill_date_new","Productname")

trans_2016 <- subset(master_tran,master_tran$bill_date_new<"2017-01-01",cols)
srt_trans_2016<-trans_2016[order(trans_2016$customer_id,trans_2016$bill_date_new),]

str(trans_2016)
trans_2017 <- subset(master_tran,master_tran$bill_date_new > "2016-12-31",cols)
srt_trans_2017 <- trans_2017[order(trans_2017$customer_id,trans_2017$bill_date_new),]

split_2016 <- split(trans_2016$Productname,trans_2016$customer_id,drop=TRUE)

split_2017 <- split(trans_2017$Productname,trans_2017$customer_id,drop=TRUE)

#test<-read.csv('C:\\Projects\\Hasbro\\flat_2016.csv')
#t_matrix<-as.matrix(test)

order_trans_2016<-as(split_2016,"transactions")

summary(order_trans_2016)

itemFrequencyPlot(order_trans_2016,topN=10,type="absolute") 

# for 2017 data 

order_trans_2017<-as(split_2017,"transactions")

summary(order_trans_2017)

itemFrequencyPlot(order_trans_2017,topN=10,type="absolute") 


# Get the rules
rules <- apriori(order_trans_2016, parameter = list(supp = 0.001, conf = 0.8))

summary(rules)

# Remove redudant rules for rules 2016
#subset.matrix <- is.subset(rules, rules)

#subset.matrix[lower.tri(subset.matrix, diag=T)] <- NA
#redundant <- colSums(subset.matrix, na.rm=T) >= 1
#rules.pruned <- rules[!redundant]
#rules<-rules.pruned

rules_2017 <- apriori(order_trans_2017, parameter = list(supp = 0.001, conf = 0.8))

summary(rules_2017)


# Show the top 5 rules, but only 2 digits
options(digits=2)
inspect(rules[1:30])
inspect(rules_2017[1:30])

rules<-sort(rules, by="confidence", decreasing=TRUE)

rules_n_2017<-sort(rules_2017, by="confidence", decreasing=TRUE)

toprules_2016 <-rules[1:15]
toprules_2017 <-rules_n_2017[1:15]

#plotting rules 
plot(toprules_2016)

plot(toprules_2016,method="graph",engine='interactive',shading=NA)

plot(toprules_2016,method="grouped")

plot(toprules_2017)

plot(toprules_2017,method="graph",engine="interactive",shading=NA)
plot(toprules_2017,method="grouped")


# check for T-shirts

 tshirt_rules_2017 <- apriori(order_trans_2017, parameter = list(supp = 0.001, conf = 0.8),
                             appearance = list(default="lhs",rhs="SHIRTS"),
                             control = list(verbose=F))

t_rules<-sort(tshirt_rules_2017, decreasing=TRUE,by="confidence")
inspect(t_rules[1:10])