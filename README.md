# MarkovMusic
Markov model for music generation

Usage:

1) Building the corpus

Creates a new folder (destination_dataset_folder) containing transpositions of any midi file on the original_data_folder

python transpose_to_C_or_Am.py original_data_folder destination_dataset_folder

or

python transpose_all_keys.py original_data_folder destination_dataset_folder


2) Extracting transition matrix

Analyze of all midi files in all subfolders of dataset_folder and creates two files on the dataset_folder folder, init_symbols.p and symbol_transition_count.p

python extract_matrix.py dataset_folder


3) Generate new harmony

python sequence_generator.py dataset_folder output_file_name.mid number_of_chords 



Code based on this paper:

MEDEIROS, R. J. V. ; SANTOS, R. S. ; PITOMBEIRA, Liduino . Modelagem Sistêmica baseada em Cadeias de Markov. In: XXI Congresso da ANPPOM, 2011, Uberlândia. Anais do XXI Congresso da ANPPOM, 2011.

https://anppom.com.br/congressos/index.php/21anppom/Uberlandia2011/rt/printerFriendly/681/0
