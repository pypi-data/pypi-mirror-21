import random

from Bio.Seq import Seq
from Bio.Alphabet import IUPAC, generic_dna

class CodonShuffler:
    """
    Class to shuffle codons within an ORF, without changing the overall
    codon frequency.
    """
    def __init__(self):
        pass

    def make_lookup_table(self, seq):
        """
        Make a reverse codon lookup table that lists codons used in seq for
        each amino acid. The same codon may be listed more than once for each
        amino acid.
        """
        codons = {}

        for i in range(int(len(seq)/3)):
            codon = seq[3*i:3*i+3]
            amino_acid = str(Seq.translate(codon))
            if amino_acid in codons:
                codons[amino_acid].append(str(codon))
            else:
                codons[amino_acid] = [str(codon)]

        return codons

    def shuffle_codons(self, seq, start_window = 0, end_window = 0):
        """
        Shuffle codons in a sequence without changing codon frequencies.
        """
        # Trim sequence based on start and end windows
        start = start_window*3
        end = len(seq) - end_window*3
        seq_trim = seq[start:end]

        # Make sure sequence doesn't have any partial codons
        assert len(seq_trim) % 3 == 0

        # Construct dictionary of all codons present in the sequence
        codons = self.make_lookup_table(seq_trim)
        # Shuffle codons
        for amino_acid in codons:
            random.shuffle(codons[amino_acid])
        # Translate original sequence
        seq_aa = seq_trim.translate()
        shuffled_seq = seq[0:start]
        # Reconstruct sequence with codons shuffled
        for amino_acid in str(seq_aa):
            shuffled_seq += codons[amino_acid].pop()
        shuffled_seq += seq[end:]
        return shuffled_seq
