import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
from class_predefine import *

# Function to load metadata from JSON
def load_metadata(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        metadata = json.load(file)
    return metadata

# Recursive function to retrieve all subthemes of selected themes
def get_all_selected_themes(selected_themes, structure):
    all_themes = []
    for theme, sub_structure in structure.items():
        if selected_themes.get(theme, False):
            all_themes.append(theme)
            all_themes.extend(get_all_selected_themes(selected_themes, sub_structure))
    return all_themes

# Filtering function based on user selection
def filter_datasets(metadata, selected_themes, selected_spatial_granularity=None,
                    selected_temporal_granularity=None, selected_spatial_scope=None, selected_temporal_scope=None):
    # Filtering logic remains the same as before
    filtered_datasets = []
    for dataset in metadata:
        theme_match = False
        if selected_themes:
            theme_match = any(
                dataset['themeDataset'] == theme or any(theme in measure.values() or theme in info.values()
                for measure in dataset.get('measures', []) for info in dataset.get('complementaryInfo', []))
                for theme in selected_themes
            )
            if not theme_match:
                continue

        if selected_spatial_granularity and dataset.get('spatioGranularityMin') > selected_spatial_granularity:
            continue
        if selected_temporal_granularity and dataset.get('temporalGranularityMin') > selected_temporal_granularity:
            continue
        if selected_spatial_scope and not any(selected_spatial_scope == scope.get('Level') for scope in dataset.get('spatioScope', [])):
            continue
        if selected_temporal_scope:
            dataset_temporal_scope = dataset.get('temporalScope')
            if dataset_temporal_scope:
                dataset_start = datetime.strptime(dataset_temporal_scope['min_date'], "%Y-%m-%d %H:%M:%S")
                dataset_end = datetime.strptime(dataset_temporal_scope['max_date'], "%Y-%m-%d %H:%M:%S")
                user_start, user_end = selected_temporal_scope
                if not (dataset_start <= user_end and dataset_end >= user_start):
                    continue

        filtered_datasets.append(dataset)
    return filtered_datasets

class DataSelectionApp:
    def __init__(self, root, metadata):
        self.root = root
        self.metadata = metadata
        self.root.title("Identify Your Requirement")
        self.root.geometry("600x600")

        # Frame for theme checkboxes with scrollable area
        tk.Label(root, text="Select Theme(s):").pack()
        theme_frame = tk.Frame(root)
        theme_frame.pack(expand=True, fill="both", padx=10, pady=5)
        canvas = tk.Canvas(theme_frame)
        scrollbar = tk.Scrollbar(theme_frame, orient="vertical", command=canvas.yview)
        scrollable_theme_frame = tk.Frame(canvas)
        scrollable_theme_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_theme_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Checkbox variables for themes
        self.theme_vars = {}
        self.create_checkboxes(scrollable_theme_frame, theme_folder_structure)

        # Spatial and temporal granularity selections
        self.spatial_granularity = tk.StringVar()
        self.temporal_granularity = tk.StringVar()
        tk.Label(root, text="Select Spatial Granularity:").pack()
        spatial_options = [level[1] for hierarchy in hS_F for level in hierarchy]
        ttk.Combobox(root, textvariable=self.spatial_granularity, values=spatial_options).pack()

        tk.Label(root, text="Select Temporal Granularity:").pack()
        temporal_options = [level[1] for hierarchy in hT_F for level in hierarchy]
        ttk.Combobox(root, textvariable=self.temporal_granularity, values=temporal_options).pack()

        # Spatial and temporal scope inputs
        tk.Label(root, text="Enter Spatial Scope (e.g., specific region, commune):").pack()
        self.spatial_scope_entry = tk.Entry(root)
        self.spatial_scope_entry.pack()
        tk.Label(root, text="Enter Temporal Scope (e.g., specific year):").pack()
        self.temporal_scope_entry = tk.Entry(root)
        self.temporal_scope_entry.pack()

        # Submit button
        tk.Button(root, text="Submit Selection", command=self.submit_selection).pack(pady=10)

    def create_checkboxes(self, parent_frame, structure, level=0):
        for theme, sub_structure in structure.items():
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(
                parent_frame,
                text=theme,
                variable=var,
                command=lambda v=var, ss=sub_structure: self.on_theme_check(v, ss)
            )
            checkbox.grid(sticky="w", padx=level * 20)
            self.theme_vars[theme] = var
            if sub_structure:
                self.create_checkboxes(parent_frame, sub_structure, level + 1)

    def on_theme_check(self, parent_var, sub_structure):
        if sub_structure:
            for sub_theme, sub_sub_structure in sub_structure.items():
                var = self.theme_vars.get(sub_theme)
                if var:
                    var.set(parent_var.get())
                if sub_sub_structure:
                    self.on_theme_check(var, sub_sub_structure)

    def submit_selection(self):
        # Retrieve all selected themes and their sub-themes
        selected_themes = get_all_selected_themes(self.theme_vars, theme_folder_structure)
        selected_spatial_granularity = self.spatial_granularity.get() or None
        selected_temporal_granularity = self.temporal_granularity.get() or None
        spatial_scope = self.spatial_scope_entry.get() or None
        temporal_scope_text = self.temporal_scope_entry.get()

        selected_temporal_scope = None
        if temporal_scope_text:
            try:
                selected_temporal_scope = (datetime.strptime(temporal_scope_text, "%Y"), datetime.strptime(temporal_scope_text, "%Y"))
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid year for temporal scope.")
                return

        filtered_datasets = filter_datasets(
            self.metadata,
            selected_themes,
            selected_spatial_granularity=selected_spatial_granularity,
            selected_temporal_granularity=selected_temporal_granularity,
            selected_spatial_scope=spatial_scope,
            selected_temporal_scope=selected_temporal_scope
        )

        messagebox.showinfo("Filtered Datasets", f"Number of datasets matching criteria: {len(filtered_datasets)}")

# Load metadata and start GUI
file_path = r'C:\Users\ADMrechbay20\Documents\Metadata\raw_data_metadata.json'
metadata = load_metadata(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = DataSelectionApp(root, metadata)
    root.mainloop()

