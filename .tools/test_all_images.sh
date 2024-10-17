# Function for the progress bar
bar_size=40
bar_char_done="#"
bar_char_todo="-"
bar_percentage_scale=2

function show_progress {
    current="$1"
    total="$2"

    # calculate the progress in percentage 
    percent=$(bc <<< "scale=$bar_percentage_scale; 100 * $current / $total" )
    # The number of done and todo characters
    done=$(bc <<< "scale=0; $bar_size * $percent / 100" )
    todo=$(bc <<< "scale=0; $bar_size - $done" )

    # build the done and todo sub-bars
    done_sub_bar=$(printf "%${done}s" | tr " " "${bar_char_done}")
    todo_sub_bar=$(printf "%${todo}s" | tr " " "${bar_char_todo}")

    # output the bar
    echo -ne "\rProgress : [${done_sub_bar}${todo_sub_bar}] ${percent}%"

    if [ $total -eq $current ]; then
        echo -e "\nDONE"
    fi
}

# Clone and add the catalog to you album collection
album clone template:catalog git@github.com:HenriquesLab/DL4MicEverywhere-album.git DL4MicEverywhere_album
album add-catalog git@github.com:HenriquesLab/DL4MicEverywhere-album.git

# Create an empty file where successfull and failing solutions are stored
mkdir -p .temp/success
mkdir -p .temp/fail

# Folder where source folder where solutions are

# Count the nomber of solutions
solution_num=$(find "../src/" -type d -name "*" | wc -l)
idx=0

# Test all the solutions 
for f in ../src/*; do
  # Show the progressbar
  show_progress $idx $solution_num

  filename=".temp/$(basename ${f}).txt"

  # Install the solution
  album install "$f/solution.py" &> $filename
  install_output=$?
  # echo "Analyzing $filename"
  
  # Check if the command correctly runs and save the output in the corresponding folder
  if [[ $install_output -eq 0 ]]; then
    mv $filename .temp/success
  else
    mv $filename .temp/fail
  fi

  # Increase the index
  idx=$(expr $idx + 1)
done