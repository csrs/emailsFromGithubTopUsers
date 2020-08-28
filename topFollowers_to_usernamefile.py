### Input: List of Top Github users by number of followers (https://github.com/search?o=desc&p=1&q=followers%3A%3E%3D312&s=followers&type=Users) and then change the number in 'p=1' to go through all 100 "subpages".

### Output: usernames in a text file 'usernames.txt.
import requests
from bs4 import BeautifulSoup

with open('usernames.txt', 'w') as file:        # empty file in the beginning
    count = 0
    for i in range(1,5):                 # start from range 1,5, then range 5,11, and increase until you get to all the "subpages"
        url = 'https://github.com/search?o=desc&p=' + str(i) + '&q=followers%3A%3E%3D312&s=followers&type=Users'
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        file.write(url)
        file.write('\n')
        for user in soup.select(".f4.text-normal a.text-gray"):            
            count += 1
            file.write(user.get_text())
            file.write(',')


        print(i, count)     # verify that this code is getting the users for each "subpage"
print('done')
