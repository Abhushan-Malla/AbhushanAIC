from owlready2 import get_ontology
from tkinter import (
    Tk, Label, Button, Listbox, Scrollbar, VERTICAL, RIGHT, Y, Frame, BOTH, X, LEFT, TOP, Entry, StringVar
)
from tkinter import ttk
from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename

# Load the ontology (default file path)
ontology_file = "MathOntology.owl"
try:
    ontology = get_ontology(ontology_file).load()
except Exception as e:
    ontology = None
    print(f"Error loading ontology: {e}")

# Function to fetch classes
def fetch_classes():
    listbox.delete(0, "end")
    if ontology:
        for cls in ontology.classes():
            listbox.insert("end", f"Class: {cls.name}")
        listbox.insert("end", f"\nTotal Classes: {len(list(ontology.classes()))}")
    else:
        listbox.insert("end", "Ontology not loaded!")

# Function to fetch individuals
def fetch_individuals():
    listbox.delete(0, "end")
    if ontology:
        for individual in ontology.individuals():
            listbox.insert("end", f"Individual: {individual.name}")
        listbox.insert("end", f"\nTotal Individuals: {len(list(ontology.individuals()))}")
    else:
        listbox.insert("end", "Ontology not loaded!")

# Function to fetch object properties
def fetch_object_properties():
    listbox.delete(0, "end")
    if ontology:
        for prop in ontology.object_properties():
            listbox.insert("end", f"Object Property: {prop.name}")
        listbox.insert("end", f"\nTotal Object Properties: {len(list(ontology.object_properties()))}")
    else:
        listbox.insert("end", "Ontology not loaded!")

# Function to fetch data properties
def fetch_data_properties():
    listbox.delete(0, "end")
    if ontology:
        for prop in ontology.data_properties():
            listbox.insert("end", f"Data Property: {prop.name}")
        listbox.insert("end", f"\nTotal Data Properties: {len(list(ontology.data_properties()))}")
    else:
        listbox.insert("end", "Ontology not loaded!")

# Function to search for a class or individual
def search_item():
    query = search_var.get().strip().lower()
    listbox.delete(0, "end")
    if ontology and query:
        found = False
        for entity in ontology.classes():
            if query in entity.name.lower():
                listbox.insert("end", f"Class: {entity.name}")
                found = True
        for entity in ontology.individuals():
            if query in entity.name.lower():
                listbox.insert("end", f"Individual: {entity.name}")
                found = True
        if not found:
            listbox.insert("end", f"No matches found for '{query}'.")
    elif not query:
        listbox.insert("end", "Enter a search query.")
    else:
        listbox.insert("end", "Ontology not loaded!")

# Function to load ontology dynamically
def load_ontology():
    global ontology
    ontology_path = askopenfilename(filetypes=[("OWL Files", "*.owl"), ("RDF Files", "*.rdf")])
    if ontology_path:
        try:
            ontology = get_ontology(ontology_path).load()
            listbox.delete(0, "end")
            listbox.insert("end", f"Ontology loaded successfully from {ontology_path}")
        except Exception as e:
            showerror("Error", f"Failed to load ontology: {e}")

# Build the enhanced UI
root = Tk()
root.title("Math Ontology Viewer")
root.geometry("700x600")
root.configure(bg="#fefbd8")  # Pale yellow background

# Header Label
header = Label(
    root,
    text="Math Ontology Viewer",
    font=("Helvetica", 20, "bold"),
    fg="#fff",
    bg="#ff7f50",  # Coral
    pady=10
)
header.pack(fill=X)

# Frame for buttons
button_frame = Frame(root, bg="#fefbd8", pady=10)
button_frame.pack(fill=X)

# Styled Buttons
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=5)

class_button = ttk.Button(button_frame, text="Show Classes", style="TButton", command=fetch_classes)
class_button.pack(side=LEFT, padx=10)

individual_button = ttk.Button(button_frame, text="Show Individuals", style="TButton", command=fetch_individuals)
individual_button.pack(side=LEFT, padx=10)

object_prop_button = ttk.Button(button_frame, text="Object Properties", style="TButton", command=fetch_object_properties)
object_prop_button.pack(side=LEFT, padx=10)

data_prop_button = ttk.Button(button_frame, text="Data Properties", style="TButton", command=fetch_data_properties)
data_prop_button.pack(side=LEFT, padx=10)

# Search Bar
search_frame = Frame(root, bg="#fefbd8", pady=5)
search_frame.pack(fill=X)

search_var = StringVar()
search_entry = Entry(search_frame, textvariable=search_var, font=("Arial", 14), width=30)
search_entry.pack(side=LEFT, padx=10)

search_button = ttk.Button(search_frame, text="Search", style="TButton", command=search_item)
search_button.pack(side=LEFT, padx=10)

load_button = ttk.Button(search_frame, text="Load Ontology", style="TButton", command=load_ontology)
load_button.pack(side=LEFT, padx=10)

# Frame for listbox
listbox_frame = Frame(root, bg="#fefbd8")
listbox_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Scrollbar and Listbox
scrollbar = Scrollbar(listbox_frame, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(
    listbox_frame,
    yscrollcommand=scrollbar.set,
    font=("Courier", 12),
    bg="#fffaf0",  # Floral white
    fg="black",
    height=20,
    selectbackground="#4682b4",  # Steel blue
    selectforeground="white"
)
listbox.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.config(command=listbox.yview)

# Footer Label
footer = Label(
    root,
    text="Ontology Viewer - Developed in Python",
    font=("Arial", 10),
    bg="#ff7f50",  # Coral
    fg="white",
    pady=5
)
footer.pack(fill=X)

# Run the application
root.mainloop()
