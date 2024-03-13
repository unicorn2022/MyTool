# 问卷星地址连接
url = 'https://www.wjx.cn/vm/exR61ZI.aspx'
# 问卷中可能的内容及回答
content = {
    "姓名" : "李四",
    "学号" : "123456789",
    "手机号" : "1910000000",
    "电话" : "1910000000",
    "QQ" : "123456789",
    "qq" : "123456789",
    "邮箱" : "123456789@qq.com",
    "email" : "123456789@qq.com",
    "微信" : "123456789",
    "wechat" : "123456789",
}


from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from random import choice

def FillElement(qa_tmp) : 
    try: 
        qa_title = qa_tmp.find_element(By.CLASS_NAME, "topichtml").text
        print("找到问题: " + qa_title)
    except NoSuchElementException:
        print("未找到问题标题, 跳过")
        return
    
    # 填空题
    for question, answer in content.items():
        if question in qa_title:
            try:
                input = qa_tmp.find_element(By.TAG_NAME, "input")
                input.send_keys(answer)
                print("填写了" + question + ": " + answer)
                return
            except NoSuchElementException:
                print("未找到输入框, 跳过")
                return
            
    # 选择题
    try:
        answers = qa_tmp.find_elements(By.CLASS_NAME, "ui-radio")
        if answers:
            print("选项个数为: " + answers.__len__().__str__())
            answer = choice(answers)
            answer.click()
            print("选择的选项为: " + answer.find_element(By.CLASS_NAME, "label").text)
            return
    except NoSuchElementException:
        return


if __name__ == '__main__':
    # 绕过问卷星的智能检测, 将webdriver属性设置为undefined
    option = Options()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    web = Chrome(options=option)
    web.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    # 打开问卷星的网页
    web.get(url)
    while True:
        try:
            # 含有id为divstarttime的元素, 说明问卷还未开始
            web.find_element(By.ID, "divStartTimeTip")
            print("未开始填写问卷, 等待中")
            sleep(0.5)
        except NoSuchElementException:
            # 问卷已经开始
            print("开始填写问卷")
            sleep(0.1)
            web.refresh()
            break
                
            

    # 填写问卷
    for i in range(1,10):
        try:
            qa_tmp = web.find_element(By.ID, f"div{str(i)}")
            FillElement(qa_tmp)
        except NoSuchElementException:
            continue
    
    # 点击提交按钮
    print("答案填写完成, 点击提交按钮")
    submit = web.find_element(By.ID, "ctlNext").click()
    sleep(5)
    web.close()
    print("提交成功")

    
