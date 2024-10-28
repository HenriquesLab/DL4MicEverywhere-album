for f in ../src/*; do
  echo Deploying $f
  album deploy "$f/solution.py" --name DL4MicEverywhere_album --changelog ../CHANGELOG.md
done

# Clone and add the catalog to you album collection
album clone template:catalog git@github.com:HenriquesLab/DL4MicEverywhere-album.git DL4MicEverywhere_album
album add-catalog git@github.com:HenriquesLab/DL4MicEverywhere-album.git

# Create the CHANGELOG file
echo "New version of this solution" > CHANGELOG.md

# Deploy all the solutions
for f in ../src/*; do
  echo Deploying $f
  album deploy "$f/solution.py" --name DL4MicEverywhere_album --changelog ../CHANGELOG.md
done

# Remove the CHANGELOG file
rm CHANGELOG.md