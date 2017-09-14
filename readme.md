# Setup

```sh
# Install dependencies
pip install --target=. Alfred-Workflow
pip install -t lib -r req.txt

# Create symlink
export workflowsdir='/Users/'$(whoami)'/Library/Application Support/Alfred 3/Alfred.alfredpreferences/workflows'
ln -s .  $workflowsdir/cheatsheets-workflow
```

