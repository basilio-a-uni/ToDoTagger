# ToDoTagger
A small python utility that tags matching lines with unique IDs across selected file types. Thought to be used with markdown.

To use it just `cd` to your directory and type the command

```py
python ToDoTagger.py TODO md/txt/py
```
It will recursively search all files with .md, .txt or .py extensions filename and search the string "TODO" in all of those files, then will add a unique id with an exponentiation symbol before at the end of the line, this is how you can make custom links in some markdown apps (at least in Obsidian, https://obsidian.md)

Then it will create a file named TODO.md (if you change the string to search this name will change too) and create a list of links separated by file and sorted alphabetically with all the matched lines.
If you already have a TODO.md in this folder you'll have to delete or move it (or just run with `--overwrite` flag).

