import json
from pathlib import Path


def main():
    source = r'C:\Users\Tesla\AppData\Roaming\Code\User\profiles\-354f4048\settings.json'
    src = Path(source)
    dst = Path(__file__).parent / 'config_json.jsonc'
    data = None
    with src.open('rb') as reader:
        data = json.load(reader)
        reader.close()

    with dst.open('w', encoding='utf-8', newline='\n') as writer:
        json.dump(data, writer, indent=2, sort_keys=True)
        writer.flush()
        writer.close()


if __name__ == '__main__':
    main()
