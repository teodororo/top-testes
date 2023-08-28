"""
EXECUTADO COM SELENIUM 3.7.0
----------------------------------------------------------------
GIOVANNA SOUZA TEODORO
gst.eng19@uea.edu.br
"""

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

URL = "https://lovemaze.com.br/"

class TestShoppingSite(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.get(URL)
        
    def test_CT01(self): # Testar o login com um usuário válido e senha correta
        self.driver.get(URL+'/account/login')
        self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[1]/input').send_keys("giovanna.teod@gmail.com")
        self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[2]/input').send_keys("SenhaTeste123")
        new_url = URL+'account' # Sai da pagina de login para o perfil do usuario 
        self.driver.implicitly_wait(5)  # Espera o redirecionamento 
        self.assertIn(new_url, self.driver.current_url)

    def test_CT02(self): # Testar o login com um usuário inválido
        self.driver.get(URL+'/account/login')
        self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[1]/input').send_keys("emailfalso@gmail.com")
        self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[2]/input').send_keys("SenhaTeste123")
        self.driver.find_element(By.XPATH, '//*[@id="login-form"]/button').click()
        error = self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[3]')
        self.assertTrue(error.is_displayed()) # Checa se a mensagem de erro aparece

    def test_CT03(self): # Testar o login com um usuário válido e senha inválida
        self.driver.get(URL+'/account/login')
        self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[1]/input').send_keys("giovanna.teod@gmail.com")
        self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[2]/input').send_keys("SenhaTeste123Errada")
        self.driver.find_element(By.XPATH, '//*[@id="login-form"]/button').click()
        error = self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[3]')
        self.assertTrue(error.is_displayed()) # Checa se a mensagem de erro aparece

    #def test_CT04(self): # Testar o login com um usuário válido e senha inválida
    #    --- SELENIUM NAO PEGA A MENSAGEM DE ERRO DO PROMPT ALERT ---
    #    self.driver.get(URL+'/account/login')
    #    self.driver.find_element(By.XPATH, '//*[@id="login-form"]/button').click() # Botao de "Login"
    #    error = self.driver.switch_to.alert.text # o alert de erro aparece, mas o selenium nao pega
    #    error_expected = "Preencha este campo." 
    #    assert error == error_expected

    def test_CT05(self): # Pesquisar produto existente
        self.driver.find_element(By.XPATH, '/html/body/header/div/div[1]/div[3]/form/div/input').send_keys("NEWJEANS")
        self.driver.find_element(By.XPATH, '/html/body/header/div/div[1]/div[3]/form/div/button').click()
        new_url = URL+'search/?q=NEWJEANS' # Sai da pagina de login para o perfil do usuario 
        self.driver.implicitly_wait(5)  # Espera o redirecionamento 
        self.assertIn(new_url, self.driver.current_url)

    def test_CT06(self): # Pesquisar produto inexistente
        self.driver.find_element(By.XPATH, '/html/body/header/div/div[1]/div[3]/form/div/input').send_keys("Arduino")
        self.driver.find_element(By.XPATH, '/html/body/header/div/div[1]/div[3]/form/div/button').click()
        error = self.driver.find_element(By.XPATH, '/html/body/div[12]/section[2]/div/p')
        self.assertTrue(error.is_displayed()) # Checa se a mensagem de erro aparece

    def test_CT07(self): # Pesquisar produto por categoria
        self.driver.find_element(By.XPATH, '/html/body/header/div/div[2]/div[3]/div/ul/li[2]/div[1]/a').click() # botao de produtos
        self.driver.find_element(By.XPATH, '/html/body/div[12]/section[4]/div/div/div[1]/div[1]/div/ul/li[1]/a').click() # botao de 'Papelaria'
        papelaria = self.driver.find_element(By.XPATH, '/html/body/div[12]/section[4]/div/div/div[1]/div[1]/div/h3').text
        assert papelaria == "Papelaria"

    def test_CT08(self): # Adicionar produto ao carrinho
        self.driver.find_element(By.XPATH, '/html/body/header/div/div[1]/div[3]/form/div/input').send_keys("NEWJEANS")
        self.driver.find_element(By.XPATH, '/html/body/header/div/div[1]/div[3]/form/div/button').click() # botao da lupa
        produto = self.driver.find_element(By.XPATH, '//*[@id="quick167512171"]/div[2]') # hover para aparecer o botao de comprar
        actions = ActionChains(self.driver)
        actions.move_to_element(produto).perform()
        self.driver.find_element(By.XPATH, '//*[@id="quick167512171"]/div[3]/div[1]/form/input[2]').click() # botao de comprar
        self.driver.implicitly_wait(10)  # Espera ser adicionado ao carrinho 
        self.driver.find_element(By.XPATH, '//*[@id="ajax-cart"]/a/span[1]').click() # botao do carrinho
        produto = self.driver.find_element(By.XPATH, '//*[@id="modal-cart"]/form/div[2]/div[1]/div/div[2]/div/h6/a') # nome do produto
        self.assertTrue(produto.is_displayed()) # Checa se o produto aparece

    #def test_CT09(self): # Acesso as redes sociais 
    #    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #    self.driver.find_element(By.XPATH, '/html/body/section[8]/div/div/div/a/div[2]/span').click()
    #    new_url = 'https://www.instagram.com/lovemazeart/' # Sai da pagina de login para o perfil do usuario 
    #    self.driver.implicitly_wait(20)  # Espera o redirecionamento 
    #    self.assertIn(new_url, self.driver.current_url)


    def test_CT10(self): # Sobre a loja
        self.driver.find_element(By.XPATH, '/html/body/footer/div[1]/div[1]/div[1]/ul/li[4]/a').click() 
        new_url = URL+'sobrealm/' # Sai da pagina de login para o perfil do usuario 
        self.driver.implicitly_wait(10)  # Espera o redirecionamento 
        self.assertIn(new_url, self.driver.current_url)

    def test_CT11(self): # Contato da loja
        self.driver.find_element(By.XPATH, '/html/body/footer/div[1]/div[1]/div[1]/ul/li[3]/a').click() 
        new_url = URL+'contato/' # Sai da pagina de login para o perfil do usuario 
        self.driver.implicitly_wait(10)  # Espera o redirecionamento 
        self.assertIn(new_url, self.driver.current_url)

    def test_CT12(self): # Contato da loja
        self.driver.find_element(By.XPATH, '/html/body/footer/div[1]/div[1]/div[1]/ul/li[3]/a').click() 
        self.driver.find_element(By.XPATH, '//*[@id="logo"]/a/img').click()
        self.driver.implicitly_wait(10)  # Espera o redirecionamento 
        self.assertIn(URL, self.driver.current_url)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()