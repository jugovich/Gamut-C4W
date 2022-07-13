import itertools
import os
import glob
from time import sleep

import pandas as pd
import requests
import requests, zipfile, io


df = pd.read_excel('/Users/mjugovi@us.ibm.com/Downloads/C4W_2022 Submissions.xlsx')

if not os.path.isdir('/Users/mjugovi@us.ibm.com/Data/gamut'):
    os.makedirs('/Users/mjugovi@us.ibm.com/Data/gamut')
    os.makedirs('/Users/mjugovi@us.ibm.com/Data/gamut_final')

_parsed_files = glob.glob("/Users/mjugovi@us.ibm.com/Data/gamut_final/*")

def parse(row):
    _name = '{} {}'.format(row['Name-First'], row['Name-Last'])

    if _name in list(itertools.chain.from_iterable( [_.replace('/Users/mjugovi@us.ibm.com/Data/gamut_final/', '').split('__') for _ in _parsed_files])):
        print(f'skipping {_name}')
        return
    else:
        print(f'processing {_name}')

    for x in range(5):
        #1 - Title	#1 - Media	#1 - Dimensions	#1 - Year Created	#1 - Price
        fp = '{} {}__{}__{}__{}'.format(row['Name-First'], row['Name-Last'], row['#{} - Title'.format(x+1)],
                                        row['#{} - Dimensions'.format(x + 1)], row['Entry ID']).replace('/', '-')
        print(fp)

        if pd.isnull(row['Submission #{} - File Upload'.format(x+1)]):
            return

        r = requests.get(row['Submission #{} - File Upload'.format(x+1)])
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall("/Users/mjugovi@us.ibm.com/Data/gamut")
        _download_files = glob.glob("/Users/mjugovi@us.ibm.com/Data/gamut/*")
        for i, _download_file in enumerate(_download_files):
            fp = fp + '__{}'.format(str(i+1))
            _known_ext = False
            for _ext in ['png', 'jpg', 'jpeg', 'pdf', 'mp4', 'jfif', 'mov', 'tif', 'tiff', 'docx', 'doc', 'gif', 'heic']:
                if _download_file.lower().endswith(f'.{_ext}'):
                    _final_fp = f"/Users/mjugovi@us.ibm.com/Data/gamut_final/{fp}.{_ext}"
                    _known_ext = True
                    break
                elif _download_file.lower().endswith(('1', '2', '3', '4', '5')):
                    _final_fp = f"/Users/mjugovi@us.ibm.com/Data/gamut_final/{fp}"
                    _known_ext = True
                    print('Did not detect ext saving without')
                    break
            if not _known_ext:
                print('UNKOWN FP')
                print(_download_file)

                raise AssertionError

            print('renaming')
            print(_download_file, _final_fp)
            os.rename(_download_file, _final_fp)
            print('done')

df.apply(parse, axis=1)
