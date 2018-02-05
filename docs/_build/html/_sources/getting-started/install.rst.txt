***************
Install & run
***************


- Download & install `Anaconda <https://www.anaconda.com/download/>`_ or `Miniconda <https://conda.io/miniconda.html>`_.
- Download and uncompress the `py3dsceneeditor repository <https://github.com/UmSenhorQualquer/py3dsceneeditor/archive/master.zip>`_.
- Open the terminal and go to the previous uncompressed directory.
- Excute in the terminal the next command to install the Anaconda/Miniconda environment.

  .. code-block:: bash

	 conda env create -f environment-ubuntu17.yml

- Activate the environment by executing the command:

  .. code-block:: bash

     source activate videoannotator

- Excute in the terminal the next command to update the code:
	
  .. code-block:: bash

     python install.py