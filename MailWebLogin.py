# -*- coding: UTF-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from ParamParser import ParamParser
from LogWriter import LogFileWriter

import time
import sys
import os


def set_function_timeout(driver, timeout, func):
    return WebDriverWait(driver, timeout).until(func)


def open_browser():

    os.system("taskkill /F /IM chromedriver.exe")
    return webdriver.Chrome()


def open_login_page(driver, args_dict):

    driver.get(args_dict['url'])
    driver.maximize_window()

    normal_login_tab = set_function_timeout(driver, 10, lambda d: driver.find_element_by_id(args_dict['loginPageID']))
    normal_login_tab.click()


def find_element(driver, args_dict):

    result = str(args_dict['url']).find("163")
    if result != -1:
        driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@id,'x-URS-iframe')]"))
    try:
        username = driver.find_element_by_xpath(args_dict['usernameInputXpath'])
        password = driver.find_element_by_xpath(args_dict['passwordInputXpath'])
        login_button = driver.find_element_by_xpath(args_dict['loginSubmitXpath'])
        return username, password, login_button
    except NoSuchElementException, e:
        print "Login credentials components can't be found so exit browser"
        driver.quit()


def send_values(elements_list, args_dict):

    i = 0
    step_keys = ['username', 'password']
    for key in step_keys:
        elements_list[i].clear()
        elements_list[i].send_keys(args_dict[key])
        i = i + 1
    elements_list[2].click()


def check_result(driver, args_dict, log_writer):

    try:
        error_notifications = set_function_timeout(driver, 5,
                                                   lambda d: driver.find_elements_by_xpath(args_dict['loginFailXpath']))
        error_msg = ""
        if len(error_notifications) == 0:
            error_msg = "No error messages have been matched"
            print error_msg
        elif len(error_notifications) == 1:
            error_msg = error_notifications[0].text
            print error_msg
        else:
            print len(error_notifications)
            for error in error_notifications:
                if "display: block;" in error.get_attribute("style"):
                    error_msg = error.text
                    print(error.text)
                    break
        print "Account or password error:"
        log_writer.log_write("%s:%s:%s:ERROR:%s\n" % (args_dict['url'], args_dict['username'], args_dict['password'],
                                                      error_msg.encode('gbk').decode('gbk')))
    except TimeoutException, e:
        print(e)
        print("Account or password right")

        driver.switch_to.default_content()
        time.sleep(10)
        name = driver.find_element_by_xpath(args_dict['loginPassXpath']).text
        print(name)

        driver.find_element_by_xpath(args_dict['logoutXpath']).click()
        time.sleep(10)

        log_writer.log_write("%s:%s:%s:SUCCESSFUL\n" % (args_dict['url'], args_dict['username'], args_dict['password']))


def login_test(args_dict_list):

    log_writer = LogFileWriter()

    for args_dict in args_dict_list:
        driver = open_browser()

        open_login_page(driver, args_dict)

        elements_list = find_element(driver, args_dict)

        send_values(elements_list, args_dict)

        check_result(driver, args_dict, log_writer)

        driver.quit()

    log_writer.log_close()


if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')

    path = ".\datafile.txt"
    parser = ParamParser()
    dict_list = parser.get_args(path)
    login_test(dict_list)
