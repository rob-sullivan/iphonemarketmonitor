# iPhone Market Monitor
A tool to get the price distribution of iphones for sale on secondhand websites

## List of Websites
- DoneDeal.ie
- Adverts.ie
- Gumtree.ie
- Facebook Marketplace
- Gumtree.com
- Shpock
- eBay.co.uk
- Facebook Marketplace
- Preloved.co.uk

## The Guess / Question to answer
* There is a statistical difference between iphone ad prices from their average across all sites and an opportunity exists to buy below on one and sell at average on another.

## Method / Plan
1. Get total number of iphone ads (not price)
2. Randomly sample iPhone ads 
3. For every ad in sample 
    1. Get text model (e.g iPhone 14), 
    2. Get text description
    3. Get float Price
    4. Get datetime when ad was posted

4. Perform a Levene's test on each website sample to check homogeneity of variance (that the distance between the max and min from the average is the same).

5. If the same (accept Levene's test) then perform a One-Way Anova test and a post hoc test called Tukey.


Results should confirm either
1. Null Hypothesis (H₀): There is no significant difference in the mean ad prices between the different websites. In other words, the average ad price is the same across all websites.

2. Alternative Hypothesis (H₁): There is a significant difference in the mean ad prices between at least some of the websites. ad prices on some websites are either higher or lower compared to others.

* Post hoc test should tell us which ads on which sites.