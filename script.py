#import codecademylib3_seaborn
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

webpage = requests.get("https://content.codecademy.com/courses/beautifulsoup/cacao/index.html")

soup = BeautifulSoup(webpage.content, "html.parser")

#print(soup)

#view ratings of chocolates as histogram
ratings = []
for rating_tag in soup.find_all(attrs={"class": "Rating"})[1:]:
  ratings.append(float(rating_tag.get_text()))
plt.figure()
plt.hist(ratings)
plt.title("Choclate Ratings")
plt.xlabel("Different Ratings")
plt.ylabel("Frequency of Rating")

#get company names
company_names = []
for company_tag in soup.select(".Company")[1:]:
  company_names.append(company_tag.get_text())

#get cocoa percentages
cocoa_percentages = []
for cocoa_perc_tag in soup.select(".CocoaPercent")[1:]:
  cocoa_percentages.append(float(cocoa_perc_tag.get_text()[:-1]))

#print top 10 chocolates
data_dict = {"Company": company_names, "Rating": ratings, "CocoaPercentage": cocoa_percentages}
cacao_df = pd.DataFrame.from_dict(data_dict)
mean_ratings = cacao_df.groupby("Company").Rating.mean()
ten_best = mean_ratings.nlargest(10)
print(ten_best)

#display scatterplot with trendling to see if there's
# a correlation between cocoa percentage and rating
plt.figure()
plt.scatter(cacao_df.CocoaPercentage, cacao_df.Rating)
z = np.polyfit(cacao_df.CocoaPercentage, cacao_df.Rating, 1)
line_function = np.poly1d(z)
plt.plot(cacao_df.CocoaPercentage, line_function(cacao_df.CocoaPercentage), "r--")
plt.title("Percent Cocoa vs Choclate Ratings")
plt.xlabel("Cocoa Percentage")
plt.ylabel("Rating")

plt.show()

#It seems from the final plot that the chocolate rating decreases
# as cocoa percentage increases. Maybe since more cocoa menas more
# bitterness. The scatterplot is widely spread across the y axis.