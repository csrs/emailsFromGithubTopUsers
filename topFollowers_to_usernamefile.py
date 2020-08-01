### This is quite janky, because I couldn't get BeautifulSoup to consistently return the usernames, so I went 5 at a time and then compiled them all into a Python list.

### Input: List of Top Github users by number of followers (https://github.com/search?o=desc&p=1&q=followers%3A%3E%3D312&s=followers&type=Users) and then change the number in 'p=1' to go through all 100 "subpages".

### Output: usernames in a text file 'usernames.txt. I outputted to a text file so that I could see what had worked and what hadn't. Then, I removed everything but the usernames and copied that in usernames_output.txt.
import requests
from bs4 import BeautifulSoup

with open('usernames.txt', 'w') as file:        # empty file in the beginning
    count = 0
    for i in range(95,101):                 # start from range 1,5, then range 5,11, and increase until you get to all the "subpages"
        url = 'https://github.com/search?o=desc&p=' + str(i) + '&q=followers%3A%3E%3D312&s=followers&type=Users'
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        file.write(url)
        file.write('\n')
        for user in soup.select(".f4.text-normal a.text-gray"):            # get usernames -- THIS WORKS
        # for user in soup.select(".mr-3 .muted-link"):                    # get emails -- THIS DOESN'T WORK
            count += 1
            file.write(user.get_text())
            file.write(',')


        print(i, count)     # verify that this code is getting the users for each "subpage"
print('done')



### Other things I tried that didn't work

# req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
# webpage = urlopen(req).read()

# soup = BeautifulSoup(webpage, "lxml")
# cont_res = ' '.join([item.find(class_="text-normal").text for item in soup.find_all(class_="text-normal") if '' in item.text])




# r  = requests.get("https://github.com/search?o=desc&p=1&q=followers%3A%3E%3D312&s=followers&type=Users")
# soup = BeautifulSoup(r.text, 'html.parser')
# results = [a.attrs.get('href') for a in soup.select('a[href^="mailto:"]')]


# print(results)