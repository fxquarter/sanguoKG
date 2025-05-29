import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time

# 初始化ChromeDriver
driver = webdriver.Chrome()

# 先检查文件是否存在，如果不存在则创建，并写入表头（这里假设表头为['人物1', '人物2', '关系']，可根据实际情况调整）
csv_file_name = '人物关系.csv'
if not os.path.exists(csv_file_name):
    with open(csv_file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['人物1', '人物2', '关系'])

# 函数用于爬取特定lemmaId的人物关系，将relationships_list作为参数传入
def crawl_person_relationships(lemma_id, relationships_list):
    url = f"https://baike.baidu.com/starmap/view?lemmaId={lemma_id}&pageType=relation&starMapFrom=lemma_relation_starMap"
    driver.get(url)
    time.sleep(0.3)  # 等待时间，确保页面加载

    # 检查页面是否包含loading
    loading = driver.find_elements(By.CSS_SELECTOR, "div#loading")
    if loading:
        print(f"Skipping lemma_id {lemma_id} due to loading.")
        return relationships_list  # 返回原列表，而不是直接返回

    # 检查页面是否包含“三国”
    if "三国" not in driver.page_source:
        print(f"Skipping lemma_id {lemma_id} as it does not contain '三国'.")
        return relationships_list 

    try:
        # 获取人物1的名称
        person1_elem = driver.find_element(By.CSS_SELECTOR, ".title-name_DFPbv")
        person1 = person1_elem.text.replace("的人物关系", "")

        # 找到所有人物关系元素
        relationships = driver.find_elements(By.CSS_SELECTOR, ".item-title_XjKik")
        for relation in relationships:
            # 获取关系
            relation_text = relation.find_element(By.CSS_SELECTOR, ".item-desc_tyVBq").text
            # 获取人物2的名称
            person2 = relation.find_element(By.CSS_SELECTOR, ".item-name_brp4I").text
            # 输出三元组
            print(person1, person2, relation_text)
            # 存储三元组
            relationships_list.append([person1, person2, relation_text])
            # 每1000次爬取后向CSV文件中添加数据
        if (lemma_id + 1) % 30565 == 0:
            with open(csv_file_name, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(relationships_list)
            relationships_list = []  # 清空列表以准备下一段数据的存储
    except Exception as e:
        print(f"Error occurred while crawling lemma_id {lemma_id}: {e}")
    return relationships_list


# 存储三元组的列表，初始化为空列表
relationships_list = []

# 爬取多个lemmaId的人物关系
lemma_ids = range(30560, 30565)  # 假设lemmaId从到10000
for i, lemma_id in enumerate(lemma_ids):
    relationships_list = crawl_person_relationships(lemma_id, relationships_list)

# 将剩余的数据添加到CSV文件
if relationships_list:
    with open(csv_file_name, 'a', newline='', encoding='GB2312') as file:
        writer = csv.writer(file)
        writer.writerows(relationships_list)

# 关闭浏览器
driver.quit()