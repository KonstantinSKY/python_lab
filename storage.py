import argparse
import os
import tempfile
import json

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

parser = argparse.ArgumentParser()
parser.add_argument("--key", help="key of elements")
parser.add_argument("--value", help="value of elements")
args = parser.parse_args()

data = []
if os.path.exists(storage_path) and os.stat(storage_path).st_size != 0:
    with open(storage_path, 'r') as f:
        data = json.loads(f.read())

if args.key and args.value:
    data.append({args.key: args.value})
    with open(storage_path, 'w') as f:
        f.write(json.dumps(data))
elif args.key:
    result_list = [item[args.key] for item in data if args.key in item]
    print(*result_list, sep=', ')
else:
    print('The program is called with invalid parameters.')



