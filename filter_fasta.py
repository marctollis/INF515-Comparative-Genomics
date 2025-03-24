import sys

def filter_fasta(input_file, output_file):
    entries = {}  # Dictionary to track species and their preferred entries
    sequence_lengths = {}  # Track sequence lengths for all entries

    with open(input_file, 'r') as infile:
        current_entry = []
        current_species = None
        current_gene = None
        current_has_transcript_X1 = False

        for line in infile:
            if line.startswith(">"):
                # Process the previous entry if present
                if current_entry:
                    sequence_length = sum(len(seq) for seq in current_entry[1:])  # Sequence length
                    
                    # Prioritize [transcript=X1] if available, otherwise keep longest sequence
                    if current_has_transcript_X1 or current_species not in entries:
                        entries[current_species] = current_entry
                        sequence_lengths[current_species] = sequence_length
                    elif sequence_length > sequence_lengths[current_species]:
                        entries[current_species] = current_entry
                        sequence_lengths[current_species] = sequence_length

                # Reset conditions for new entry
                current_entry = []
                current_has_transcript_X1 = "[transcript=X1]" in line

                # Extract species and gene
                try:
                    species = line.split("[organism=")[1].split("]")[0].replace(" ", "_")
                    gene_name = line.split(" ")[1].strip()
                    current_species = f"{species}_{gene_name}"
                    current_entry.append(f">{current_species}")
                except IndexError:
                    current_species = None

            else:
                if current_entry:
                    current_entry.append(line.strip())

        # Final entry processing
        if current_entry:
            sequence_length = sum(len(seq) for seq in current_entry[1:])
            if current_has_transcript_X1 or current_species not in entries:
                entries[current_species] = current_entry
                sequence_lengths[current_species] = sequence_length
            elif sequence_length > sequence_lengths[current_species]:
                entries[current_species] = current_entry
                sequence_lengths[current_species] = sequence_length

    # Write results to file
    with open(output_file, 'w') as outfile:
        for entry in entries.values():
            outfile.write("\n".join(entry) + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python filter_fasta.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    filter_fasta(input_file, output_file)

