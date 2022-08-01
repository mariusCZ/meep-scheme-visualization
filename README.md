## Project no longer of any use. MEEP with Python has the same performance as with Scheme and Python interface includes all needed visualization.

# MEEP Scheme structure Python base visualization tool
This project's purpose is to create a visualization tool for Meep's Scheme interface which is deprecated.

The forked meep repository that contains the visualization function can be found [here](https://github.com/mariusCZ/meep).

## Set up
1. Begin by copying the files to your simulation directory.

2. Make the files executable:
  ```
  chmod u+x grabstruc.sh visualize.py
  ```
  
3. Run the script:
  ```
  ./grabstruc.sh
  ```
  
4. Enter the filename once prompted.

In the case of the system being used not having `mpirun`, open the *grabstruc.sh* file and remove the `mpirun` command.
