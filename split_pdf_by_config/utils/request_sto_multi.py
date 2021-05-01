import requests
import json

from loguru import logger


def extract_file_raw(file_path):
    """不提取其中的text_lines"""
    url = " http://139.155.249.104:7021/text_extract"
    data = {"file_path": file_path}
    response = requests.post(url, data=data)
    logger.info(response.status_code)
    # print(response.text)
    result = response.json()
    # bo = BaseJsonOperation()
    # fp = Path(file_path)
    # fp_suffix = fp.suffix
    # json_suffix = '.json'
    # json_path = os.path.basename(file_path.replace(fp_suffix, json_suffix))
    # bo.save_json(result, json_path)

    return_code = result['error_code']
    if return_code == 0:
        return result
    elif return_code == 1:
        logger.error('合合ocr参数出错')
        return False
    elif return_code == 2:
        logger.error('被识别的文件格式不对，只能是pdf或img')
        return False
    elif return_code == 40010:
        logger.error('提取图像裸数据失败')
        return False
    elif return_code == 50004 or return_code == 50001:
        logger.error(' 后台服务器宕机或请求数据超时')
        return False
    else:
        logger.error('未知错误导致的请求失败')
        return False


def get_docu_type(file_path):
    url = "http://121.5.100.192:7011/predictor/get_doc_type"

    headers = {
        'Content-Type': 'application/json'
    }
    # bo = BaseJsonOperation()
    # json_data = bo.load_json('4000645219.json')
    json_data = extract_file_raw(file_path)
    if not json_data:
        logger.critical('ocr 请求失败')
        return
    payload = json.dumps({
        "json_dict": json_data
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    divide_json_data = response.json()
    logger.info(divide_json_data)
    return divide_json_data


if __name__ == '__main__':
    file_path = "/home/ubuntu/data/raw_file/invista/invista2021-04-02T110226Fw__进口_客户-chris519/coo.pdf"
    get_docu_type(file_path)
