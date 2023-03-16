import tkinter as tk
import HexMapHelper


# Define the function to display the generated biome
def display_biome():
    selected_biome = dropdown.get()  # get the selected biome from the dropdown
    printlist = HexMapHelper.ProcessWrapper(selected_biome)  # generate the biome list for the selected biome
    output.delete('1.0', tk.END)  # clear the previous output
    for b in printlist:
        output.insert(tk.END, str(b) + '\n')  # display the generated biomes in the output box


# Create the GUI
root = tk.Tk()
root.title('HexMapHelper Tile Generator')
root.geometry('400x300')

# Create the dropdown menu
biomes = ['water', 'swamp', 'desert', 'plains', 'forest', 'hills', 'mountain']
dropdown = tk.StringVar(root)
dropdown.set(biomes[0])  # set the default selected biome
dropdown_menu = tk.OptionMenu(root, dropdown, *biomes)
dropdown_menu.pack()

# Create the generate button
generate_button = tk.Button(root, text='Generate', command=display_biome)
generate_button.pack()

# Create the output box
output = tk.Text(root)
output.pack()

# Start the GUI
root.mainloop()
