from src.sequence import Sequence
from src.sequtil import score_as_int

def read_fastq(io_buffer):
    """Returns a generator of Sequence objects"""
    scores_are_next = False
    header = ''
    bases = ''
    scores = []
    for line in io_buffer:
        if line[0] == '@' and not scores_are_next:
            if len(header) > 0:
                # Yield the previous Sequence
                yield Sequence(header, bases, scores)
            header = line[1:].strip()  # Get the next header
            bases = ""
        elif line[0] == '+':
            scores_are_next = True
        else:
            if scores_are_next:
                scores = translate_scores(line.strip())
                scores_are_next = False
            else:
                bases += line.strip()
    # Add the last sequence
    yield Sequence(header, bases, scores)

def translate_scores(scorestring):
    """Translates a string of phred scores to a list of integers"""
    return [score_as_int(score) for score in scorestring]

def get_seq_coverage(seqs):
    coverage = {}
    for seq in seqs:
        if seq.bases in coverage:
            coverage[seq.bases] += 1
        else:
            coverage[seq.bases] = 1
    return coverage

def get_avg_seq_coverage(coverage):
    return sum(coverage.values())/len(coverage.values())
