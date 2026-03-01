# Rosalind
# basic tools for genetic sequences


from codon_table import codon_table
import commands as coms
import re

seq: str
seq_type: str
is_forward: bool = None
seq_length: int

seq_history = []        # [ (seq, seq_type, is_forward) ]
undone_history = []     # [ (seq, seq_type, is_forward) ]


# --- Sequence Type Detection ---
def is_dna(seq: str) -> bool:
    if re.fullmatch(r"^((3|5)'?\-)?(A|T|G|C)+(\-(5|3)'?)?$", seq):
        return True
    else: return False

def is_rna(seq: str) -> bool:
    if re.fullmatch(r"^((3|5)'?\-)?(A|U|G|C)+(\-(5|3)'?)?$", seq):
        return True
    else: return False

def is_protein(seq: str) -> bool:
    if re.fullmatch(r"^((N|C)'?\-)?([ACDEFGHIKLMNPQRSTVWY])+(\-(N|C)'?)?$", seq):
        return True
    else: return False


# --- Sequence ---
def new_seq() -> None:
    global seq, seq_type, is_forward

    input_str = input("Enter sequence:\n").upper()

    if is_dna(input_str):
        seq_type = "DNA"
        if input_str.startswith("5"): is_forward = True
        elif input_str.startswith("3"): is_forward = False
        try: seq_history.append((seq, seq_type, is_forward))
        except NameError: pass
        seq = input_str.strip("35'-").upper()
        
    elif is_rna(input_str):
        seq_type = "RNA"
        if input_str.startswith("5"): is_forward = True
        elif input_str.startswith("3"): is_forward = False
        try: seq_history.append((seq, seq_type, is_forward))
        except NameError: pass
        seq = input_str.strip("35'-").upper()
        
    elif is_protein(input_str):
        seq_type = "Protein"
        if input_str.startswith(("N'-", "N-")): is_forward = True
        elif input_str.startswith(("C'-", "C-")): is_forward = False
        try: seq_history.append((seq, seq_type, is_forward))
        except NameError: pass
        seq = input_str.strip("NC'-").upper()

    else:
        print("Invalid sequence. Please enter a valid DNA, RNA or protein sequence.")
        new_seq()
        return
    
    length = len(seq)
    print(f"{seq_type} sequence detected. " \
        + f"Orientation: {'forward' if is_forward == True else 'reverse' if is_forward == False else 'unknown'}. " \
        + f"Length: {length} {'nt' if seq_type in ['DNA', 'RNA'] else 'aa'}." )
    print()
    

def print_seq():
    global seq, seq_type, is_forward
    if seq_type in ['DNA', 'RNA']:
        if is_forward == True: print(f"5'-{seq}-3'")
        elif is_forward == False: print(f"3'-{seq}-5'")
        else: print(seq)
    else:
        if is_forward == True: print(f"N'-{seq}-C'")
        elif is_forward == False: print(f"C'-{seq}-N'")
        else: print(seq)
    print()


# --- Sequence Editing ---
def reverse() -> None:
    global seq, seq_type, is_forward
    seq_history.append((seq, seq_type, is_forward))
    seq = seq[::-1]
    is_forward = not is_forward if is_forward != None else None

def complement() -> None:
    global seq, seq_type, is_forward
    if seq_type == "DNA":
        complement_transl_table = str.maketrans("ATGC", "TACG")
    elif seq_type == "RNA":
        complement_transl_table = str.maketrans("AUGC", "UACG")
    else:
        print("Complement is only applicable to DNA and RNA sequences.")
        print()
        return None
    
    seq_history.append((seq, seq_type, is_forward))
    seq = seq.translate(complement_transl_table)
    is_forward = not is_forward if is_forward != None else None

def transcribe() -> None:
    global seq, seq_type, is_forward

    if seq_type == "DNA":
        seq_history.append((seq, seq_type, is_forward))
        seq = seq.replace("T", "U")
        seq_type = "RNA"

    elif seq_type == "RNA":
        seq_history.append((seq, seq_type, is_forward))
        seq = seq.replace("U", "T")
        seq_type = "DNA"

    else:
        print("Transcription is only applicable to DNA and RNA sequences.")
        print()

def translate() -> None:
    global seq, seq_type, is_forward, seq_length

    if seq_type == "DNA":
        translation = ""
        for i in range(0, len(seq), 3):
            try: translation += codon_table[seq[i:i+3]]
            except KeyError: pass

        seq_history.append((seq, seq_type, is_forward))
        seq = translation
        seq_type = "Protein"; seq_length = len(seq)

    elif seq_type == "RNA":
        transcribe()
        translate()
    else:
        print("Translation is only applicable to DNA and RNA sequences.")
        print()


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
    if input_str in coms.print_seq: print_seq()
    elif input_str in coms.new: new_seq()
    elif input_str in coms.length: print(f"{seq_length} {'nt' if seq_type in ['DNA', 'RNA'] else 'aa'}.")

    # --- Sequence Editing ---
    elif input_str in coms.reverse:
        reverse()
        print("Sequence reversed:")
        print_seq()
    elif input_str in coms.complement:
        complement()
        print("Complement sequence generated:")
        print_seq()
    elif input_str in coms.reverse_complement:
        reverse()
        complement()
        print("Reverse complement sequence generated:")
        print_seq()
    elif input_str in coms.transcribe:
        transcribe()
        print("Sequence transcribed:")
        print_seq()
    elif input_str in coms.translate:
        translate()
        print("Sequence translated:")
        print_seq()

    # --- Other ---
    elif input_str in coms.undo:
        if undo():
            print("Undone. Sequence:")
            print_seq()
        else:
            print("Nothing to undo.")
            print()
    elif input_str in coms.redo:
        if redo():
            print("Redone. Sequence:")
            print_seq()
        else:
            print("Nothing to redo.")
            print()
    elif input_str in coms.help: help()