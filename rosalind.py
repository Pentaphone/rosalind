# Rosalind
# basic tools for genetic sequences


from codon_table import codon_table
import commands as cmds

import random
import re

seq: str
seq_type: str = None
is_forward: bool = None
seq_length: int

seq_history = []        # [ (seq, seq_type, is_forward) ]
undone_history = []     # [ (seq, seq_type, is_forward) ]


# --- Utility ---
def nucleotides(seq_type: str = None) -> str:
    if seq_type == None: seq_type = globals()['seq_type']

    if seq_type == "DNA": return "ATGC"
    elif seq_type == "RNA": return "AUGC"
    else: return None

AMINO_ACIDS = "ACDEFGHIKLMNPQRSTVWY"

def random_seq(seq_type: str, length: int = 100) -> str:
    if seq_type == "DNA": return ''.join(random.choices(nucleotides("DNA"), k=length))
    elif seq_type == "RNA": return ''.join(random.choices(nucleotides("RNA"), k=length))
    elif seq_type == "Protein": return ''.join(random.choices(AMINO_ACIDS, k=length))
    else: return None


# --- Sequence Type Detection ---
def is_dna(seq: str) -> bool:
    if re.fullmatch(r"^((3|5)'?\-)?(A|T|G|C)+(\-(5|3)'?)?$", seq, re.IGNORECASE):
        return True
    else: return False

def is_rna(seq: str) -> bool:
    if re.fullmatch(r"^((3|5)'?\-)?(A|U|G|C)+(\-(5|3)'?)?$", seq, re.IGNORECASE):
        return True
    else: return False

def is_protein(seq: str) -> bool:
    if re.fullmatch(r"^((N|C)'?\-)?([ACDEFGHIKLMNPQRSTVWY])+(\-(N|C)'?)?$", seq, re.IGNORECASE):
        return True
    else: return False


# --- Sequence ---
def new_seq() -> None:
    global seq, seq_type, is_forward, seq_length

    input_str = input("Enter sequence:\n").lower()
    input_split = input_str.split()

    if is_dna(input_str):
        seq_type = "DNA"
        if input_str.startswith("5"): is_forward = True
        elif input_str.startswith("3"): is_forward = False
        if 'seq' in globals():  seq_history.append((seq, seq_type, is_forward))
        seq = input_str.strip("35'-").upper()
        seq_length = len(seq)
        print("DNA sequence detected. " \
            +f"Orientation: {'forward' if is_forward == True else 'reverse' if is_forward == False else 'unknown'}, " \
            +f"Length: {seq_length} {'nt' if seq_type in ['DNA', 'RNA'] else 'aa'}" )
        
    elif is_rna(input_str):
        seq_type = "RNA"
        if input_str.startswith("5"): is_forward = True
        elif input_str.startswith("3"): is_forward = False
        if 'seq' in globals():  seq_history.append((seq, seq_type, is_forward))
        seq = input_str.strip("35'-").upper()
        seq_length = len(seq)
        print("RNA sequence detected. " \
            +f"Orientation: {'forward' if is_forward == True else 'reverse' if is_forward == False else 'unknown'}, " \
            +f"Length: {seq_length} {'nt' if seq_type in ['DNA', 'RNA'] else 'aa'}" )
        
    elif is_protein(input_str):
        seq_type = "Protein"
        if input_str.startswith(("N'-", "N-")): is_forward = True
        elif input_str.startswith(("C'-", "C-")): is_forward = False
        if 'seq' in globals():  seq_history.append((seq, seq_type, is_forward))
        seq = input_str.strip("NC'-").upper()
        seq_length = len(seq)
        print("Protein sequence detected. " \
            +f"Orientation: {'forward' if is_forward == True else 'reverse' if is_forward == False else 'unknown'}, " \
            +f"Length: {seq_length} {'nt' if seq_type in ['DNA', 'RNA'] else 'aa'}" )

    # random sequence
    elif input_split[0] in cmds.random:

        if len(input_split) == 3 \
            and input_split[1] in ["rna", "dna", "protein"] \
            and input_split[2].isdigit():
                if 'seq' in globals(): seq_history.append((seq, seq_type, is_forward))
                seq_type = input_split[1].replace("dna", "DNA").replace("rna", "RNA").replace("protein", "Protein")
                seq_length = int(input_split[2])
                seq = random_seq(seq_type, seq_length)
                is_forward = True
                print(f"Random {seq_type} sequence generated:")
                print_seq(blank_line=False)

        elif len(input_split) == 2 \
            and input_split[1] in ["rna", "dna", "protein"]:
                if 'seq' in globals(): seq_history.append((seq, seq_type, is_forward))
                seq_type = input_split[1].replace("dna", "DNA").replace("rna", "RNA").replace("protein", "Protein")
                seq = random_seq(seq_type)
                is_forward = True
                seq_length = len(seq)
                print_seq(blank_line=False)
                print(f"Length: {seq_length} {'nt' if seq_type in ['DNA', 'RNA'] else 'aa'}")

        elif len(input_split) == 1:
            input_str = input("Sequence Type (DNA / RNA / Protein):\n>>  ").lower()
            if input_str not in ["rna", "dna", "protein"]:
                print("Invalid sequence type.")
                new_seq()
                return
            else:
                seq_type = input_str.replace("dna", "DNA").replace("rna", "RNA").replace("protein", "Protein")
                input_str = input("Sequence length (default = 100):\n>>  ")
                if not input_str.isdigit() and input_str != "":
                    print("Invalid sequence length.")
                    new_seq()
                    return
                elif input_str == "":
                    seq_length = 100
                else:
                    seq_length = int(input_str)
                seq = random_seq(seq_type, seq_length)
                is_forward = True
                print_seq(blank_line=False)
                print(f"Length: {seq_length} {'nt' if seq_type in ['DNA', 'RNA'] else 'aa'}")

        else:
            print("Invalid random sequence command.")
            new_seq()
            return
        
    else:
        print("Invalid sequence. Please enter a valid DNA, RNA or protein sequence.")
        new_seq()
        return
    
    print()
    

def print_seq(blank_line: bool = True):
    global seq, seq_type, is_forward
    if seq_type in ['DNA', 'RNA']:
        if is_forward == True: print(f"5'-{seq}-3'")
        elif is_forward == False: print(f"3'-{seq}-5'")
        else: print(seq)
    else:
        if is_forward == True: print(f"N'-{seq}-C'")
        elif is_forward == False: print(f"C'-{seq}-N'")
        else: print(seq)
    if blank_line: print()


def count() -> None:
    global seq, seq_type, seq_length

    if seq_type in ['DNA', 'RNA']:
        counts = {nt: seq.count(nt) for nt in nucleotides() if nt in seq}
        portions = {nt: counts[nt] / seq_length for nt in counts}
        print("Nucleotide counts:")
        for nt, count in counts.items():
            print(f"{nt}: {count:>4}  {portions[nt]:.1%}")

    elif seq_type == "Protein":
        counts = {aa: seq.count(aa) for aa in AMINO_ACIDS if aa in seq}
        portions = {aa: counts[aa] / seq_length for aa in counts}
        print("Amino acid counts:")
        for aa, count in counts.items():
            print(f"{aa}: {count:>4}  {portions[aa]:.1%}")

    else:
        print("No sequence to count.")
    print()


# --- Sequence Editing ---
def reverse() -> None:
    global seq, seq_type, is_forward
    seq_history.append((seq, seq_type, is_forward))
    seq = seq[::-1]
    is_forward = not is_forward if is_forward != None else None


def complement() -> bool:
    global seq, seq_type, is_forward
    if seq_type == "DNA":
        complement_transl_table = str.maketrans("ATGC", "TACG")
        return True
    elif seq_type == "RNA":
        complement_transl_table = str.maketrans("AUGC", "UACG")
        return True
    else:
        print("Complement is only applicable to DNA and RNA sequences.")
        print()
        return False
    
    seq_history.append((seq, seq_type, is_forward))
    seq = seq.translate(complement_transl_table)
    is_forward = not is_forward if is_forward != None else None


def transcribe() -> bool:
    global seq, seq_type, is_forward

    if seq_type == "DNA":
        seq_history.append((seq, seq_type, is_forward))
        seq = seq.replace("T", "U")
        seq_type = "RNA"
        return True

    elif seq_type == "RNA":
        seq_history.append((seq, seq_type, is_forward))
        seq = seq.replace("U", "T")
        seq_type = "DNA"
        return True

    else:
        print("Transcription is only applicable to DNA and RNA sequences.")
        print()
        return False



def translate() -> bool:
    global seq, seq_type, is_forward, seq_length

    if seq_type == "DNA":
        translation = ""
        for i in range(0, len(seq), 3):
            try: translation += codon_table[seq[i:i+3]]
            except KeyError: pass

        seq_history.append((seq, seq_type, is_forward))
        seq = translation
        seq_type = "Protein"; seq_length = len(seq)
        return True

    elif seq_type == "RNA":
        transcribe()
        translate()
    else:
        print("Translation is only applicable to DNA and RNA sequences.")
        print()
        return False


# --- Other ---
def undo() -> bool:
    global seq, seq_type, is_forward, seq_length
    if len(seq_history) > 0:
        undone_history.append((seq, seq_type, is_forward))
        seq, seq_type, is_forward = seq_history.pop()
        seq_length = len(seq)
        return True
    else: return False


def redo() -> bool:
    global seq, seq_type, is_forward, seq_length
    if len(undone_history) > 0:
        seq_history.append((seq, seq_type, is_forward))
        seq, seq_type, is_forward = undone_history.pop()
        seq_length = len(seq)
        return True
    else: return False

def help():
    print("For instructions please see 'README.md'.")
    print()


# --- Main ---
new_seq()

while True:
    input_str = input(">>  ").lower()

    # --- Sequence ---
    if input_str in cmds.print_seq: print_seq()
    elif input_str in cmds.new: new_seq()
    elif input_str in cmds.length: print(f"{seq_length} {'nt' if seq_type in ['DNA', 'RNA'] else 'aa'}.")
    elif input_str in cmds.count: count()

    # --- Sequence Editing ---
    elif input_str in cmds.reverse:
        reverse()
        print("Sequence reversed:")
        print_seq()

    elif input_str in cmds.complement:
        if complement():
            print("Complement sequence generated:")
            print_seq()

    elif input_str in cmds.reverse_complement:
        reverse()
        if complement():
            print("Reverse complement sequence generated:")
            print_seq()

    elif input_str in cmds.transcribe:
        if transcribe():
            print(f"Sequence transcribed into {seq_type}:")
            print_seq()

    elif input_str in cmds.rna:
        if seq_type == "DNA":
            transcribe()
            print("Sequence transcribed into RNA:")
            print_seq()
        elif seq_type == "RNA":
            print_seq()
        else: transcribe()  # protein, prints error message

    elif input_str in cmds.dna:
        if seq_type == "RNA":
            transcribe()
            print("Sequence transcribed into DNA:")
            print_seq()
        elif seq_type == "DNA":
            print_seq()
        else: transcribe()  # protein, prints error message

    elif input_str in cmds.translate:
        if translate():
            print("Sequence translated:")
            print_seq()

    # --- Other ---
    elif input_str in cmds.undo:
        if undo():
            print(f"Undone. {seq_type} sequence:")
            print_seq()
        else:
            print("Nothing to undo.")
            print()

    elif input_str in cmds.redo:
        if redo():
            print(f"Redone. {seq_type} sequence:")
            print_seq()
        else:
            print("Nothing to redo.")
            print()

    elif input_str in cmds.help: help()