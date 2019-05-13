# trashf
CLI tool to safely remove any file and directory by putting them in the trash  

Move any file or directory in the trash in a clever and safe way when wanting to remove them. If a file or folder with the same name already exist in the trash, the file or folder to be removed will be renamed with the date before to be moved to the trash (fname + "_%Y_%m_%d-%H_%M_%S").


# installation
```sh
with pip:
sudo pip3 install trashf

with yay:
yay -a trashf

with yaourt:
yaourt -a trashf
```

# compatibility
python >= 3


# usage
<pre>
<b>trashf / rt</b> [<b>F_PATH_01 F_PATH_02 ...</b>]
<b>options:</b>
<!-- -->         <b>-h, --help</b>        show this help message and exit
</pre>


# examples
for **help**:<br/>
```sh
trashf -h
or
rt --help
```

move in the trash ($HOME/.local/share/Trash/files) files and folders:<br/>
```sh
trashf titi/ toto.jpg
```
