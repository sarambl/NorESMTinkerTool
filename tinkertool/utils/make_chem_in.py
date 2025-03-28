import sys
from pathlib import Path

def generate_chem_in_ppe(scale_factor,
                          outfolder_base = '', outfolder_name = 'chem_mech_files',input_file = None,
                         silent=True):
    """
    Generate a chemistry namelist file for a given scale factor and input file.
    Command line usage example:
    python tinkertool/utils/make_chem_in.py 0.5

    Parameters:
    -----------
    scale_factor : float
        The scale factor to use for the chemistry file.
    outfolder : str
        The name of the output folder to use.
    input_file : str
        The name of the input file to use.
    """
    if input_file is None:
        input_file = "config/chem_mech_default.in"

    outfolder = outfolder_base + outfolder_name
    if not Path(outfolder).exists():
        Path(outfolder).mkdir(parents=True)
    print(scale_factor)
    outputfile = Path(outfolder)/f'chem_mech_scale_{scale_factor:.3f}.in'

    with open(input_file, 'r') as f:
        lines = f.readlines()

    with open(outputfile, 'w') as outfile:
        for i, line in enumerate(lines):
            replace = False
            if 'monoterp' in line or 'isoprene' in line:
                if '->' in line:
                    if '+' in line:
                        if ';' in line:
                            replace = True
            if replace:

                yld= line.split('->')[1].split('*')[0].strip()
                new_yld = float(yld)*scale_factor
                new_yld = f'{new_yld:.3f}'
                replacement_text = line.replace(yld, new_yld)
                if not silent:
                    print(f'Replacing \n {line} \n with \n {replacement_text}')
                outfile.write(replacement_text )

            else:
                    outfile.write(line)

    return str(outputfile)


if __name__ == '__main__':
    args = sys.argv[1:]
    generate_chem_in_ppe(*args)