Setting up Python using ASDF:


# Installing ASDF

Run the steps outlined here

For all systems:
`git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.4.2`

Then add ASDF to your path. For Linux/Ubuntu:

```bash
echo -e '\n. $HOME/.asdf/asdf.sh' >> ~/.bashrc
echo -e '\n. $HOME/.asdf/completions/asdf.bash' >> ~/.bashrc
```

For other systems, see: https://github.com/asdf-vm/asdf#setup

# Installing Python

```bash
asdf plugin-add python
asdf install python 3.4

# Run this from within the project folder; it probably is already set to 3.4 by the `.tool-versions`-file that is there
asdf local python 3.4 

```

# Installing Flask

```bash
pip install flask
asdf reshim python
```

# Running Flask

```bash
FLASK_APP=hello.py flask run
```
