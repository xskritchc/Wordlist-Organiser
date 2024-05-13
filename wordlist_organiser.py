import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar

def read_words_from_file(file_path):
    with open(file_path, 'r') as file:
        words = file.read().split()
    return words

def merge_and_sort_lists(*lists):
    merged_list = []
    for lst in lists:
        merged_list.extend(lst)
    merged_list = list(set(merged_list))  # Remove duplicates
    merged_list.sort()  # Sort alphabetically
    return merged_list

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        input_files_listbox.insert(tk.END, file_path)

def browse_output_file():
    output_file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if output_file_path:
        output_file_entry.delete(0, tk.END)
        output_file_entry.insert(0, output_file_path)

def clear_inputs():
    input_files_listbox.delete(0, tk.END)
    output_file_entry.delete(0, tk.END)

def process_files():
    input_files = input_files_listbox.get(0, tk.END)
    if not input_files:
        messagebox.showerror("Error", "No input files provided.")
        return

    try:
        words_lists = [read_words_from_file(file) for file in input_files]
    except FileNotFoundError as e:
        messagebox.showerror("Error", f"Error reading file: {e.filename}")
        return

    merged_and_sorted = merge_and_sort_lists(*words_lists)

    output_file_path = output_file_entry.get()
    if not output_file_path:
        messagebox.showerror("Error", "No output file specified.")
        return

    total_words = len(merged_and_sorted)
    progress_bar["maximum"] = total_words
    progress_bar.start()

    with open(output_file_path, 'w') as output_file:
        for i, word in enumerate(merged_and_sorted, 1):
            output_file.write(word + "\n")
            progress_bar["value"] = i
            root.update_idletasks()

    progress_bar.stop()
    messagebox.showinfo("Success", f"Combined and alphabetically sorted list of words saved to '{output_file_path}'.")
    
    # Clear input files listbox and output file entry
    clear_inputs()

root = tk.Tk()
root.title("Wordlist Organizer")
root.geometry("500x400") # Set window size

# Input Frame
input_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
input_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

input_files_label = tk.Label(input_frame, text="Input Files:")
input_files_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

input_files_listbox = tk.Listbox(input_frame, selectmode=tk.MULTIPLE, height=8, width=50) 
input_files_listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

browse_button = tk.Button(input_frame, text="Browse", command=browse_file)
browse_button.grid(row=1, column=2, padx=5, pady=5)

# Output Frame
output_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
output_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

output_file_label = tk.Label(output_frame, text="Output File:")
output_file_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

output_file_entry = tk.Entry(output_frame, width=50)
output_file_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

browse_output_button = tk.Button(output_frame, text="Browse", command=browse_output_file)
browse_output_button.grid(row=1, column=2, padx=5, pady=5)

# Button Frame
button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, padx=5, pady=5)

process_button = tk.Button(button_frame, text="Process", command=process_files, width=10)
process_button.grid(row=0, column=0, padx=5, pady=5)

clear_button = tk.Button(button_frame, text="Clear", command=clear_inputs)
clear_button.grid(row=0, column=1, padx=5, pady=5)

# Progress Frame
progress_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
progress_frame.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

progress_label = tk.Label(progress_frame, text="Progress:")
progress_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

progress_bar = Progressbar(progress_frame, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=1, column=0, padx=5, pady=5)

root.mainloop()
