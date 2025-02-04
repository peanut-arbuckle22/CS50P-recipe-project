from bs4 import BeautifulSoup # type: ignore
from urllib.request import Request, urlopen, urlretrieve, build_opener, install_opener
import re
import json
from PIL import Image # type: ignore
import textwrap
import html


class Recipe:


    def unescape(name, description, ingredients, instructions):
        name = html.unescape(name)
        description = html.unescape(description)
        ingredients = html.unescape(ingredients)
        instructions = html.unescape(instructions)
        return name, description, ingredients, instructions

    def __init__(self, name, ingredients, instructions, description, imagefile):
        self.name = name 
        self.ingredients = ingredients
        self.instructions = instructions
        self.description = description
        self.imagefile = imagefile
    
    def __str__(self):
        return f"{self.name}\n{self.ingredients}\n{self.instruction}\n{self.description}"
    
    def name_link_compile(a, link, dict, list):

        link = str(link)
        recipename = a.text
        dict[recipename] = link
        list.append(recipename)

    def searcher(searchterm, urlbeg, urlend=""):
        searchterm = searchterm.replace(" ", "%20")
        url=f"{urlbeg}{searchterm}{urlend}"
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        webpage = urlopen(req).read()
        print(url)
        return BeautifulSoup(webpage, "html.parser")
    
    def json_compile(jsn, list, stepnumber):
        for k in jsn:
            k = f"{stepnumber}. {k['text']}"
            lines = textwrap.fill(k, 200)
            list.append(f"{lines}")
            stepnumber += 1


    def json_finder(recipe_links_names, choice):
        recipeurl = recipe_links_names[choice]
        req = Request(url=recipeurl, headers={"User-Agent": "Mozilla/5.0"})
        webpage = urlopen(req).read()
        recipe_soup = BeautifulSoup(webpage, "html.parser")
        recipe_soup = recipe_soup.find("script", type="application/ld+json").text
        jsn = json.loads(recipe_soup, strict=False)
        return jsn
    

    def recipe_properties_builder(jsn, img_size):

        ingredients = "\n".join(jsn["recipeIngredient"])

        opener = build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        install_opener(opener)
        
        picture = jsn["image"]
        picture = picture[0]
        urlretrieve(picture, "assets//image.gif")
        picture = Image.open("assets//image.gif")
        picture.thumbnail((img_size,img_size))
        picture.save("assets//image.gif")

        imagefile = "assets//image.gif"
        description = jsn["description"]
        description = textwrap.fill(description, 200)
        name = jsn["name"]

        return name, ingredients, description, imagefile

    def food52search(searchterm):

        soup = Recipe.searcher(searchterm, "https://food52.com/recipes/search?q=")

        def no_class(tag):
            return not tag.has_attr("class") and not tag.has_attr("rel") and not tag.span

        soup = soup.find_all(no_class, href=re.compile(r"^/recipe"))

        recipe_links_names = {}
        recipe_name_list = []
        for a in soup:
            try:
                link = f"https://food52.com{a['href']}"
                Recipe.name_link_compile(a, link, recipe_links_names, recipe_name_list)
                
            except AttributeError:
                pass

        return recipe_links_names, recipe_name_list

    def food52_recipe_select(recipe_links_names, choice):

        jsn = Recipe.json_finder(recipe_links_names, choice)
#sometimes the JSON file is structured weird and puts the instructions inside 2 different dictionary lists, this checks for KeyError and uses different function if needed
        stepnumber = 1
        instructions = []
        try:
            Recipe.json_compile(jsn["recipeInstructions"], instructions, stepnumber)
        except KeyError:
            instructiontag = jsn["recipeInstructions"]
            instructiontag = instructiontag[0]    
            try:
                Recipe.json_compile(instructiontag["itemListElement"], instructions, stepnumber) 
            except KeyError:
                print("FUCK!")
    
        instructions = "\n\n".join(instructions)

        name, ingredients, description, imagefile = Recipe.recipe_properties_builder(jsn, 225)
        name, description, ingredients, instructions = Recipe.unescape(name, description, ingredients, instructions)
        return Recipe(name, ingredients, instructions, description, imagefile)

    def BASearch(searchterm):

        def nodatatestid(tag):
            return not tag.has_attr("data-testid")

        soup = Recipe.searcher(searchterm, "https://www.bonappetit.com/search?q=", "&page=1&content=recipe")
        soup = soup.find_all(nodatatestid, href=re.compile(r"^/recipe"), attrs={ "class" : re.compile("BaseWrap")})
        
        recipe_links_names = {}
        recipe_name_list = []

        for a in soup:
            try:
                link = f"https://www.bonappetit.com{a['href']}"
                Recipe.name_link_compile(a, link, recipe_links_names, recipe_name_list)
            except AttributeError:
                pass

        return recipe_links_names, recipe_name_list

    def BASelect(recipe_links_names, choice):

        jsn = Recipe.json_finder(recipe_links_names, choice)

        stepnumber = 1
        instructions = []
        Recipe.json_compile(jsn["recipeInstructions"], instructions, stepnumber)
        instructions = "\n\n".join(instructions)

        name, ingredients, description, imagefile = Recipe.recipe_properties_builder(jsn, 400)
        name, description, ingredients, instructions = Recipe.unescape(name, description, ingredients, instructions)
        return Recipe(name, ingredients, instructions, description, imagefile)

    def sallysearch(searchterm):
        
        soup = Recipe.searcher(searchterm, "https://sallysbakingaddiction.com/?s=")
        soup = soup.find_all("a")

        recipe_links_names = {}
        recipe_name_list = []

        for a in soup:
            if a.get("class") == None and "title" in str(a.get("rel")) and not "Video" in a.text and not "video" in a.text:
                link = f"{a['href']}"
                Recipe.name_link_compile(a, link, recipe_links_names, recipe_name_list)
            else:
                pass 

        return recipe_links_names, recipe_name_list

    def sallyselect(recipe_links_names, choice):
        
        jsn = Recipe.json_finder(recipe_links_names, choice)
        jsn = jsn["@graph"]

        for k in jsn:
            if "@context" in k.keys():
                jsn = k
            else:
                pass

        stepnumber = 1
        instructions = []
        Recipe.json_compile(jsn["recipeInstructions"], instructions, stepnumber)
        instructions = "\n\n".join(instructions)

        name, ingredients, description, imagefile = Recipe.recipe_properties_builder(jsn, 400)
        name, description, ingredients, instructions = Recipe.unescape(name, description, ingredients, instructions)
        return Recipe(name, ingredients, instructions, description, imagefile)

       




