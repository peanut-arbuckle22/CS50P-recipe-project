# Hannah's Recipe Finder
#### Video demo: https://youtu.be/OJZmPSuXpWM
#### Description:
Hannah's recipe machine is an application that helps you manage and access saved recipes. It allows you to add, edit, and delete recipes manually via user input. It also incorporates a web scraper for Bon Appetit, Food52, and Sally's Baking addiction that allows users to search, view, and save selected recipes to the user's computer. 

I chose to use PYsimpleGUI to create the GUI for this project. I considered using a command line format, but I though creating a GUI would make it much more user friendly, and would be a fun challenge. I used BeautifulSoup to create the scraper for the online recipe search tool. I used a few other libraries for misc functions, but these were the two main libraries I used. 

Regarding the GUI, I opted to use columns to simulate window changes. I could have either used this method, or used multiple windows, but this seemed much simpler. I didn't have to sacrifice any real functionality to do so, so I am ultimately happy with the dicision. I also opted to show and hide buttons on the recipe edit screen. It may have been better to just have another column for the edit screen, but regardless, I'm happy with the result. 

Choosing a layout for the online recipe screen was a challenge. I chose to have text elements display in a scrollable window. I started out using scrollable multiline elements for ingredients and instructions, but the scrollable window looks significantly cleaner. 

The project started out as a way to navigate my wife's family recipes. She had them saved in a large word doc, and I created a program to format them and save them into individual text files in a folder. Then I created the functions to search and read those files. My wife (Hannah) is a pastry chef, and isn't particularly tech savvy, so I wanted her to be able to use it if she felt so inclined, so I created a GUI. Then I had the idea to incorporate a way to search external websites and easily add them to her collection, as it seems more elegeant than just having a bunch of saved bookmarks in a web browser. 

After making the first 2 scrapers, I noticed that most websites with recipes have common elements that allow them to be scraped in similar ways. Notably, most recipe websites have a JSON element to allow for rich search engine results. These JSON files are generally formatted in very simlar ways, and even have the same keys for the dict entries. This allowed for some modularity of the scraper, and it would be relatively easy to add new sites if I wanted to do so (I don't).

One feature I considered implementing was the ability to input ingredients and output recipes that a person could make using those ingredients. I decided against this because I believe the controls over the data that would allow this would be too cumbersome. I would need to standardize each ingredient for inputting recipes, which would probably look like a list of ingredients that the user could select a quantity of. I think this would be detrimental to user experience, and would discourage use of the program. 

This is the first thing I've ever programmed, so I would love to get some feedback on it. I'm sure there are a multitute of ways I could improve it. 