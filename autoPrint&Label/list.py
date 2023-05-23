import tkinter as tk
from tkinter import ttk


def reprint(item):
    print(f"Reprinting {item}")


def delete(item):
    print(f"Deleting {item}")
    for i in tree.get_children():
        if tree.item(i)['values'][0] == item:
            tree.delete(i)
            printouts.remove(item)
            break


root = tk.Tk()

tree = ttk.Treeview(root, columns=('Reprint', 'Delete'))
tree.heading('#0', text='Item')
tree.heading('#1', text='Reprint')
tree.heading('#2', text='Delete')

printouts = ['Printout 1', 'Printout 2', 'Printout 3']
for item in printouts:
    iid = tree.insert('', 'end', text=item)
    tree.set(iid, '#1', 'Reprint')
    tree.set(iid, '#2', 'Delete')

tree.bind('<Double-1>', lambda e: reprint(tree.item(tree.selection())['text']) if tree.identify_column(
    e.x) == '#1' else delete(tree.item(tree.selection())['text']) if tree.identify_column(e.x) == '#2' else None)

tree.pack()

root.mainloop()
