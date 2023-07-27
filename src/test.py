import yara
import os

def scan_dir(rule_file, dir_path):
    # 將主規則檔案所在的目錄加入到尋找包含檔案的路徑中
    include_path = os.path.dirname(rule_file)

    # 載入 YARA 規則，並提供包含檔案的路徑 直接給
    rules = yara.compile(filepath=rule_file)
    
    print(rules)

    # ...其餘代碼...

# 你的主規則檔案
rule_file = './rules/index.yar'
# 要掃描的資料夾
dir_path = './test.txt'

scan_dir(rule_file, dir_path)
