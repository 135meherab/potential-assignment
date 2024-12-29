#!/bin/bash
echo "#!/bin/sh
isort . --gitignore --profile black
black .
git add -A" > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit