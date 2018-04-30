import urllib
import csv
from bs4 import BeautifulSoup
from requests import get
import pandas as pd

url = 'http://www.saic.edu/coursesearch/?name=By+Instructor%27s+Name&dept-program=Sound&area-study=&level=&semester=&session=&submit=Search'
response = get(url)

html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)
class_containers = html_soup.find_all(class_ = 'course-desc')

f = csv.writer(open('classNames.csv', 'w'))
f.writerow(['Name'])

for course in class_containers:
    names = course.content

    f.writerow([names])


test_df = pd.DataFrame({'className': class_containers})
print(test_df.info())
test_df
