
This is based off of https://github.com/s0md3v/Zen. 

1. I got all the usernames from this GitHub page (and the rest, see the table of contents on the bottom): https://github.com/search?o=desc&p=1&q=followers%3A%3E%3D312&s=followers&type=Users. There were all sorts of issues because BeautifulSoup couldn't consistently return all of the usernames. 

2. I put all the usernames into a file (usernames_output.txt). This has 1000 usernames. 

Now the important part:
3. I tried to feed each username into the Zen code, which uses the GitHub API to fetch an email address for a user. Here, there were issues with tabs/spaces in my IDE so the code wouldn't run or ran spoadicly.  `IndentationError: unindent does not match any outer indentation level
`
