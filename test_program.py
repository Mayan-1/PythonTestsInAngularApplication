import os
import time

import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def get_path_with_file_name(filename: str) -> str:
    return os.getcwd() + filename


def configure_selenium() -> webdriver:
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", False)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("http://localhost:4200/cadastro")
    return driver


def test_password_minimum_length_invalid():
    # Assert
    driver: webdriver = configure_selenium()
    element_password_field = driver.find_element(By.ID, "senha")
    element_password_field.send_keys("1234")
    element_button_submit_search = driver.find_element(By.ID, "btn-cadastrar")

    # Act
    element_button_submit_search.click()

    # Assert
    element_message_feedback = driver.find_element(
        By.ID, "mensagemErroTamanhoSenha").text
    assert element_message_feedback == "A senha deve conter no mínimo 6 caracteres"
    time.sleep(5)

def test_password_minimum_length_valid():
    # Assert
    driver: webdriver = configure_selenium()
    element_password_field = driver.find_element(By.ID, "senha")
    element_password_field.send_keys("123456")
    element_button_submit_search = driver.find_element(By.ID, "btn-cadastrar")

    # Act
    element_button_submit_search.click()

    with pytest.raises(NoSuchElementException):
        element_message_feedback = driver.find_element(
            By.ID, "mensagemErroTamanhoSenha").text
        assert element_message_feedback != "A senha deve conter no mínimo 6 caracteres"
    time.sleep(5)

def test_phone_is_valid():
    # Assert
    driver: webdriver = configure_selenium()
    element_phone_field = driver.find_element(By.ID, "telefone")
    element_phone_field.send_keys("(75) 91234-5678")
    element_button_submit = driver.find_element(By.ID, "btn-cadastrar")

    element_button_submit.click()

    with pytest.raises(NoSuchElementException):
        element_message_feedback = driver.find_element(By.ID, "telefoneInvalido").text
        assert element_message_feedback != "Telefone inválido."
    time.sleep(5)

def test_phone_is_invalid():
    # Assert
    driver: webdriver = configure_selenium()
    element_phone_field = driver.find_element(By.ID, "telefone")
    element_phone_field.send_keys("(75) ")
    element_button_submit = driver.find_element(By.ID, "btn-cadastrar")

    element_button_submit.click()


    element_message_feedback = driver.find_element(By.ID, "mensagemTelefoneInvalido").text
    assert element_message_feedback == "Telefone inválido."
    time.sleep(5)

def test_cpf_is_valid():
    driver: webdriver = configure_selenium()
    element_cpf_field = driver.find_element(By.ID, "cpf")
    element_cpf_field.send_keys("123.456.789-10")
    element_button_submit = driver.find_element(By.ID, "btn-cadastrar")

    element_button_submit.click()

    with pytest.raises(NoSuchElementException):
        element_message_feedback = driver.find_element(By.ID, "mensagemCpfInvalido").text
        assert  element_message_feedback != "Cpf inválido"
    time.sleep(5)

def test_cpf_is_invalid():
    driver: webdriver = configure_selenium()
    element_cpf_field = driver.find_element(By.ID, "cpf")
    element_cpf_field.send_keys("123.456.789-1")
    element_button_submit = driver.find_element(By.ID, "btn-cadastrar")

    element_button_submit.click()

    element_message_feedback = driver.find_element(By.ID, "mensagemCpfInvalido").text
    assert element_message_feedback == "Cpf inválido."
    time.sleep(5)

def test_email_is_valid():
    driver: webdriver = configure_selenium()
    element_email_field = driver.find_element(By.ID, "email")
    element_email_field.send_keys("teste@gmail.com")
    element_button_submit = driver.find_element(By.ID, "btn-cadastrar")

    element_button_submit.click()

    with pytest.raises(NoSuchElementException):
        element_message_feedback = driver.find_element(By.ID, "mensagemEmailInvalido").text
        assert element_message_feedback != "Por favor, digite um email válido."
    time.sleep(5)

def test_email_is_invalid():
    driver: webdriver = configure_selenium()
    element_email_field = driver.find_element(By.ID, "email")
    element_email_field.send_keys("testegmail.com")
    element_button_submit = driver.find_element(By.ID, "btn-cadastrar")

    element_button_submit.click()

    element_message_feedback = driver.find_element(By.ID, "mensagemEmailInvalido").text
    assert element_message_feedback == "Por favor, digite um email válido."
    time.sleep(5)

def test_confirmations_fields_is_valid():
    driver: webdriver = configure_selenium()
    # Fields email and password configuration
    element_email_field = driver.find_element(By.ID, "email")
    element_email_field.send_keys("teste@gmail.com")
    element_password_field = driver.find_element(By.ID, "senha")
    element_password_field.send_keys("123456")


    # Confirmations fields configuration
    element_confirmation_email_field = driver.find_element(By.ID, "confirmacaoEmail")
    element_confirmation_email_field.send_keys("teste@gmail.com")
    element_confirmation_password_field = driver.find_element(By.ID, "confirmacaoSenha")
    element_confirmation_password_field.send_keys("123456")

    element_button_submit = driver.find_element(By.ID, "btn-cadastrar")
    element_button_submit.click()

    with pytest.raises(NoSuchElementException):
        element_message_email_feedback = driver.find_element(By.ID, "mesmoEmailCampoAnterior").text
        assert element_message_email_feedback != "Por favor, digite o mesmo email do campo anterior"

    with pytest.raises(NoSuchElementException):
        element_message_password_feedback = driver.find_element(By.ID, "mesmaSenhaCampoAnterior").text
        assert element_message_password_feedback != "Por favor, digite a mesma senha do campo anterior"
    time.sleep(5)

def test_confirmations_fields_is_invalid():
    driver: webdriver = configure_selenium()
    # Fields email and password configuration
    element_email_field = driver.find_element(By.ID, "email")
    element_email_field.send_keys("teste@gmail.com")
    element_password_field = driver.find_element(By.ID, "senha")
    element_password_field.send_keys("123456")


    # Confirmations fields configuration
    element_confirmation_email_field = driver.find_element(By.ID, "confirmacaoEmail")
    element_confirmation_email_field.send_keys("teste1@gmail.com")
    element_confirmation_password_field = driver.find_element(By.ID, "confirmacaoSenha")
    element_confirmation_password_field.send_keys("1234566")

    element_button_submit = driver.find_element(By.ID, "btn-cadastrar")
    element_button_submit.click()


    element_message_email_feedback = driver.find_element(By.ID, "mesmoEmailCampoAnterior").text
    assert element_message_email_feedback == "Por favor, digite o mesmo email do campo anterior."


    element_message_password_feedback = driver.find_element(By.ID, "mesmaSenhaCampoAnterior").text
    assert element_message_password_feedback == "Por favor, digite a mesma senha do campo anterior."
    time.sleep(5)

def test_all_fields_filled_correctly():
    driver: webdriver = configure_selenium()
    # Fields
    element_name_field = driver.find_element(By.ID, "nome")
    element_email_field = driver.find_element(By.ID, "email")
    element_confirmation_email_field = driver.find_element(By.ID, "confirmacaoEmail")
    element_password_field = driver.find_element(By.ID, "senha")
    element_confirmation_password_field = driver.find_element(By.ID, "confirmacaoSenha")
    element_phone_field = driver.find_element(By.ID, "telefone")
    element_cpf_field = driver.find_element(By.ID, "cpf")
    element_subject_field = driver.find_element(By.ID, "materia")

    element_name_field.send_keys("Jefte Goes")
    element_email_field.send_keys("jefte@gmail.com")
    element_confirmation_email_field.send_keys("jefte@gmail.com")
    element_password_field.send_keys("123456")
    element_confirmation_password_field.send_keys("123456")
    element_phone_field.send_keys("(75) 91234-5678")
    element_cpf_field.send_keys("123.456.789-10")

    element_subject_field.click()

    subject_option = driver.find_element(By.ID, 'opcao4')
    subject_option.click()

    element_button_submit = driver.find_element(By.ID, "btn-cadastrar")
    element_button_submit.click()

    time.sleep(5)

    current_url = driver.current_url
    assert current_url == "http://localhost:4200/", f"Expected URL to be http://localhost:4200/ but got {current_url}"






