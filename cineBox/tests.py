from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.urls import reverse
from django.contrib.auth import get_user_model
from cineBox.models import Sala, Reserva
from selenium.common.exceptions import TimeoutException  # Asegúrate de importar TimeoutException correctamente

class DetalleSalaSeleniumTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        User = get_user_model()
        self.usuario = User.objects.create_user(email='testuser@gmail.com', password='123456789')
        self.sala = Sala.objects.create(nombre='Sala Test', capacidad=10)

        # Crear reserva con el campo 'horario'
        Reserva.objects.create(
            sala=self.sala,
            usuario=self.usuario,
            horario='14:00 - 16:00'
        )

    def test_horarios_ocupados_selenium(self):
        url = reverse('detalle_sala', args=[self.sala.id])
        self.driver.get(f'{self.live_server_url}{url}')

        # Espera explícita para el elemento
        try:
            ocupado_element = WebDriverWait(self.driver, 40).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '15:00')]"))
            )
            print("Elemento encontrado:", ocupado_element.text)
            # Verifica si el elemento tiene la clase 'ocupado'
            self.assertIn('ocupado', ocupado_element.get_attribute('class'))
        except TimeoutException:
            print("El elemento no se encontró en el tiempo esperado.")
            self.fail("El horario ocupado no se mostró en la página a tiempo.")
