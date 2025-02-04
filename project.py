import PySimpleGUI as sg # type: ignore
from Recipe_Class import Recipe
import os
import re

def file_search(searchterm):
#search through recipe folder, find filenames with search term in them
    results = []
    path = "recipes"
    recipelist = os.listdir(path)
    for x in recipelist:
        if searchterm.lower() in x.lower():
            results.append(x.removesuffix(".txt").title())
        else:
            pass
    if results == []:
        return "No Results Found"
    else:
        return (results)

def file_fetch(recipename):
    #put user selection into file path, return filename
    path = f"recipes//{recipename}.txt"
    with open(path) as file:
        return file.read()

def file_write(recipename, recipetext):
    #create file for new recipe input by user
    with open(recipename, "w+") as file:
        file.write(recipetext)
def file_name_fix(filename):
    return re.sub(r'[\\/*?:"<>|]',"",filename)


def main():

    sg.theme("DarkGrey11")

    recipe_list = []

    buttonlist = ["EditButton", "SaveButton", "CancelButton", "DeleteButton", "CloseButton"]

    def submit_recipe():
        filepath = f"recipes\{values['recipe_filename']}.txt"
        file_write(filepath, values["recipe_submit_text"])
        column_switch("-COL2-", "-COL4-")
        window["recipe_filename"].update("Recipe Name")
        window["recipe_submit_text"].update("Recipe Ingredients and Instructions")
        move_to_center()

    def external_update(image, name, description, ingredients, instructions):
        window["-COL3-"].update(visible=False)
        window["-COL6-"].update(visible=True)
        window["recipename"].update(name)
        window["recipedescription"].update(description)
        window["recipeingredients"].update(ingredients)
        window["filename"].update(image)
        window["recipeinstructions"].update(instructions)
        window.refresh()
        window.move_to_center()

    def button_flip():    
        for x in buttonlist:
            window[x].update(visible=not window[x].visible)

    def column_switch(column1, column2):
        window[column1].update(visible = not window[column1].visible)
        window[column2].update(visible = not window[column2].visible)

    def recipe_update():
        window["RecipeName"].update(recipe_name)
        window["RecipeText"].update(recipe_text)
    
    def recipe_disable():
        window["RecipeName"].update(disabled = True)
        window["RecipeText"].update(disabled = True)

    def move_to_center():
        window.refresh()
        window.move_to_center()

    layout_home = [
        [sg.Image("assets//home_screen_text.png", size=(500,None))],
        [sg.Button("Saved Recipes"), sg.Button("Search Online Recipes")],
    ]
    layout_stock = [
        [sg.Input("Search your recipe here",key = "Input1", expand_x = True) ],
        [sg.Combo(recipe_list, size=(30,1), key="Input2", readonly="True", enable_events=True, auto_size_text=False, expand_x = True)],
        [sg.Button("Home"), sg.Button("Input New Recipe"), sg.Button("Recipe List")]
    ]

    layout_external = [ 
        [sg.Text("Choose Website")],
        [sg.Radio("Bon Appetit", group_id=1, default=True, key="BA"), sg.Radio("Food52", group_id=1, key="52"), sg.Radio("Sally's Baking Addiction", group_id=1, key = "Sally")],
        [sg.Input("Search your recipe here",key = "ExtSearch", expand_x=True) ],
        [sg.Combo(recipe_list, size=(30,1), key="ExtSelect", readonly="True", enable_events=True, auto_size_text=False, expand_x=True)],
        [sg.Button("Home")]
    ]

    layout_recipe_input = [
        [sg.Input("Recipe Name", size=(100,1),key = "recipe_filename")],
        [sg.Multiline(default_text="Recipe Ingredients and Instructions", size=(100,35),key="recipe_submit_text", expand_x = True, expand_y=True)],
        [sg.Button("Submit"), sg.Button("Cancel")]
    ]

    layout_recipe_edit = [
        [sg.Input(disabled = True, key = "RecipeName", disabled_readonly_background_color = "#313641", disabled_readonly_text_color = "#cccdcf")],
        [sg.Multiline(disabled = True, size = (200,39), key = "RecipeText")],
        [sg.Button("Edit", visible=True, key = "EditButton", enable_events = True), sg.Button("Close", visible=True, key = "CloseButton", enable_events = True), 
        sg.Button("Save", visible = False, key = "SaveButton", enable_events = True), sg.Button("Cancel", visible = False, key = "CancelButton", enable_events = True), 
        sg.Button("Delete", visible = False, key = "DeleteButton", enable_events = True)]
    ]

    layout_external_recipe = [
        [sg.Text(key = "recipename", font="bold")],
        [sg.Text(key="recipedescription")],
        [sg.Text("Ingredients:", font="bold")],
        [sg.Text(key = "recipeingredients", size = (75, 14)), sg.Image(key = "filename")],
        #[sg.Multiline(key = "recipeingredients", size = (75, 14), expand_x=True, disabled=True), sg.Image(key = "filename")],#color 
        [sg.Text("Instructions:", font="bold")],
        [sg.Text(key = "recipeinstructions", auto_size_text = True)],
        #[sg.Multiline(key = "recipeinstructions", expand_x = False, size = (200, 20), disabled=True)],#color 
        [sg.Button("Save Recipe", key="SaveRecipe", enable_events=True), sg.Button("Close", key="CloseExt", enable_events=True)]
    ]

    layout = [[sg.Column(layout_home, key="-COL1-", element_justification="center"), sg.Column(layout_stock, visible=False, key="-COL2-"), sg.Column(layout_external, visible=False, key="-COL3-"), sg.Column(layout_recipe_input, visible=False, key="-COL4-"), sg.Column(layout_recipe_edit, visible=False, key="-COL5-"), sg.Column(layout_external_recipe, visible=False, key="-COL6-", scrollable = True, vertical_scroll_only = True, size = (1200,700))]]

    window = sg.Window("Hannah's Recipe Finder", layout, finalize=True)
    window["Input1"].bind("<Return>", "_Enter")
    window["ExtSearch"].bind("<Return>", "_Enter")

    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        #opens Saved Recipes window
        elif event == "Saved Recipes":
            column_switch("-COL1-", "-COL2-")
        
        #opens input new recipe window
        elif event == "Input New Recipe":
            column_switch("-COL2-", "-COL4-")
            move_to_center()
        #displays list of files in recipes folder
        elif event == "Recipe List":
            files = os.listdir("recipes")
            list = []
            for file in files:
                file = file.removesuffix(".txt")
                list.append(file)
            list = "\n".join(list)
            sg.popup_scrolled(list, title = "Recipe List", size = (100,40))
        #return to stock recipe window if cancel pressed
        elif event == "Cancel":
            column_switch("-COL2-", "-COL4-")
            window["recipe_filename"].update("Recipe Name")
            window["recipe_submit_text"].update("Recipe Ingredients and Instructions")
            move_to_center()
        #submits new recipe
        elif event == "Submit":
            submityn = sg.popup_yes_no(f"Are you sure you want to submit?", title = "Submit?", auto_close = False)
            if submityn == "Yes":
                filenamecheck = os.listdir("recipes")
                savefilename = f"{values['recipe_filename']}.txt"
                if savefilename.lower() in (name.lower() for name in filenamecheck):
                    duplicatefile = sg.popup_yes_no(f"{values['recipe_filename']} already exists, would you like overwrite {values['recipe_filename']}?")
                    if duplicatefile == "Yes":
                        submit_recipe()
                    if duplicatefile == "No":
                        pass
                else:
                    try:
                        submit_recipe()
                    except FileNotFoundError:
                        sg.popup_error("Invalid Filename")
                        pass
            if submityn == "No":
                pass
        #returns home when home button pressed
        elif event == "Home":
            column_switch("-COL1-", "-COL2-")
        elif event == "Home0":
            column_switch("-COL1-", "-COL3-")
        #opens Search Online Recipes window WIP
        elif event == "Search Online Recipes":
            column_switch("-COL1-", "-COL3-")
        #searches Saved Recipes, populates drop down with results
        elif event == "Input1" + "_Enter":
            searchterm = values["Input1"]
            recipe_list = file_search(searchterm)
            if recipe_list == "No Results Found":
                window["Input2"].update(values= ["No Results Found"], value = "No Results Found")#, value="No Results Found")
            else:
                window["Input2"].update(values = recipe_list, value = recipe_list[0])    
        #initiates external search function, website and scraper function determined by radio button
        elif event == "ExtSearch" + "_Enter":
            searchterm = values["ExtSearch"]
            if values["BA"] == True:
                recipelist, recipenamelist = Recipe.BASearch(searchterm)
            elif values["52"] == True:
                recipelist, recipenamelist = Recipe.food52search(searchterm)
            elif values["Sally"] == True:
                recipelist, recipenamelist = Recipe.sallysearch(searchterm)
            window["ExtSelect"].update(values = recipenamelist, value = "Click arrow for results")
        #allows user to select recipe from dropdown list of search results, displays recipe
        elif event == "ExtSelect":
            if values["BA"] == True:
                barecipechoice = values["ExtSelect"]
                results = Recipe.BASelect(recipelist, barecipechoice)
                external_update(results.imagefile, results.name, results.description, results.ingredients, results.instructions)
            elif values["52"] == True:
                food52recipechoice = values["ExtSelect"]
                results = Recipe.food52_recipe_select(recipelist, food52recipechoice)
                external_update(results.imagefile, results.name, results.description, results.ingredients, results.instructions)
            elif values["Sally"] == True:
                sallyrecipechoice = values["ExtSelect"]
                results = Recipe.sallyselect(recipelist, sallyrecipechoice)
                external_update(results.imagefile, results.name, results.description, results.ingredients, results.instructions)
        #saves recipe in recipes folder, uses name as filename
        elif event == "SaveRecipe":

            saveyn = sg.popup_yes_no(f"Are you sure you want to save {results.name}?", title = "Save?", auto_close = False)

            if saveyn == "Yes":
                name = results.name
                name = file_name_fix(name)
                filenamecheck = os.listdir("recipes")
                if f"{name.lower()}.txt" in (extfilename.lower() for extfilename in filenamecheck):
                    extduplicatefile = sg.popup_yes_no(f"{name} already exists, would you like overwrite {name}?")
                    if extduplicatefile == "Yes":
                        with open(f"recipes//{str(name)}.txt", "w+", encoding="utf-8") as file:
                            file.write(f"{name}\n\n{results.description}\n\n{results.ingredients}\n\n{results.instructions}")
                            file.close()
                    if extduplicatefile == "No":
                        pass
                else:
                    with open(f"recipes//{str(name)}.txt", "w+", encoding="utf-8") as file:
                        file.write(f"{name}\n\n{results.description}\n\n{results.ingredients}\n\n{results.instructions}")
                        file.close()
            if saveyn == "No":
                pass
        #closes external recipe, returns to search page
        elif event == "CloseExt":
            column_switch("-COL3-", "-COL6-")
            move_to_center()
        #displays selected internal recipe
        elif event == "Input2":
            column_switch("-COL2-", "-COL5-")   
            recipe_name = values["Input2"]
            recipe_text = file_fetch(recipe_name)
            recipe_update()
            move_to_center()
        #opens edit window
        elif event == "EditButton":
            button_flip()
            window["RecipeName"].update(disabled = False)
            window["RecipeText"].update(disabled = False)
        #saves edits to recipe   
        elif event == "SaveButton":
            saveyn = sg.popup_yes_no(f"Are you sure you want to save {recipe_name}?", title = "Save?", auto_close = False)
            if saveyn == "Yes":
                try:
                    with open(f"recipes//{recipe_name}.txt", "w") as file:
                        file.write(values["RecipeText"])
                        file.close()
                        os.rename(f"recipes//{recipe_name}.txt", f"recipes//{values['RecipeName']}.txt")
                except FileNotFoundError:
                    sg.popup_error("Invalid Filename")
                    pass
                button_flip()
                recipe_disable()
                window["RecipeName"].update(f"{values['RecipeName']}")
                window["RecipeText"].update(f"{values['RecipeText']}")
                recipe_name = values["RecipeName"]
                recipe_text = values["RecipeText"]
                window["Input1"].update("Search your recipe here")
                recipe_list = []
                window["Input2"].update(values = recipe_list)
            if saveyn == "No":
                pass
        #cancels and discards edits, reverts to original recipe
        elif event == "CancelButton":
            button_flip()
            recipe_disable()
            recipe_update()
        #closes recipe edit window
        elif event == "CloseButton":
            column_switch("-COL2-", "-COL5-")
            move_to_center()
        #deletes recipe from recipes folder
        elif event == "DeleteButton":
            deleteyn = sg.popup_yes_no(f"Are you sure you want to delete {recipe_name}?", title = "Delete?", auto_close = False)

            if deleteyn == "Yes":
                os.remove(f"recipes//{recipe_name}.txt")
                column_switch("-COL2-", "-COL5-")
                recipe_list = []
                window["Input2"].update(values = recipe_list)
                window["Input1"].update("Search your recipe here")
                recipe_disable()
                button_flip()
                move_to_center()
            elif deleteyn == "No":
                pass
         
        #print(event, values)

    window.close()

if __name__ == "__main__":
    main()