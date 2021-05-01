import json


class BaseJsonOperation:

    def save_json(self, data: dict, out_path: str):
        with open(out_path, 'w', encoding="utf-8") as fw:
            json.dump(data, fw, indent=4, ensure_ascii=False)

    def load_json(self, in_path):
        with open(in_path, 'r', encoding="utf-8") as fr:
            temp = json.load(fr)
            return temp
