from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException, ElementNotVisibleException
from time import sleep
from pyvirtualdisplay import Display
import sys, traceback


def get_answer(question):
    question = question.encode("utf-8")
    if question in questions:
        answer = questions[question]
    else:
        print question
        answer = raw_input('WHAT IS THE ANSWER? ')
        questions[question] = answer
        f = open('answers', 'a')
        f.write(question + '\t' + answer + '\n')
        f.close()
    return answer

questions = {}
f = open('answers', 'r')
for line in f:
    line = line.strip()
    question, answer = line.split('\t')
    questions[question] = answer
f.close()


def vote(driver):
    url = "http://www.jjhuddle.com/forums/forum/high-school-sports-talk/everything-else/1205764-jjhuddle-bucknuts-week-6-ohio-hs-boys-swimming-team-of-the-week-vote-now"
    url = "http://www.jjhuddle.com/forums/forum/high-school-sports-talk/everything-else/1210542-jjhuddle-bucknuts-week-9-ohio-hs-boys-swimming-athlete-of-the-week-vote-now"
    driver.get(url)
    driver.execute_script("window.scrollTo(0, 100)")

    # Find Link
    xpath = "/html/body/div[3]/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[1]/div[3]/div[1]/div[3]/ul/li/div/div[2]/div/div[2]/form/ul/li[2]/label/input"
    xpath = "/html/body/div[3]/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[1]/div[3]/div[1]/div[3]/ul/li/div/div[2]/div/div[2]/form/ul/li[2]/label/input"
    radio_button = driver.find_element_by_xpath(xpath).click()

    question_xpath = "/html/body/div[3]/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[1]/div[3]/div[1]/div[3]/ul/li/div/div[2]/div/div[2]/div[4]/div/p"
    question = driver.find_element_by_xpath(question_xpath).text

    print 'QUESTION', question
    answer = get_answer(question)
    print 'ANSWER', answer

    human_verify_xpath = "/html/body/div[3]/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[1]/div[3]/div[1]/div[3]/ul/li/div/div[2]/div/div[2]/div[4]/div/input[1]"
    elem = driver.find_element_by_xpath(human_verify_xpath)
    elem.send_keys(answer)

    submit_xpath = "/html/body/div[3]/div[1]/div[4]/div[1]/div/div[2]/div[2]/div[1]/div[3]/div[1]/div[3]/ul/li/div/div[2]/div/div[2]/form/div/button[1]"
    submit = driver.find_element_by_xpath(submit_xpath).click()


if __name__ == '__main__':
    display = Display(visible=0, size=(800, 600))
    display.start()
    successes = 0
    for ind in xrange(5000):
        driver = webdriver.Firefox()
        driver.set_page_load_timeout(30)
        try:
            vote(driver)
            successes += 1
            print 'Voted %d times and tried %d times' % (successes, ind + 1)
        except Exception as e:
            print e
            traceback.print_exc(file=sys.stdout)
            continue
        finally:
            driver.close()

    display.stop()
