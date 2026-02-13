import re
from playwright.sync_api import sync_playwright, Page
import time
from src.model.Alumno import Alumno

class RobotPandora:
    def __init__(self):
        # Usamos la URL que el otro código usa para el Login (importante para el TARGET)
        self.url_login_target = "https://pandora.pucp.edu.pe/pucp/login?TARGET=https%3A%2F%2Feros.pucp.edu.pe%2Fpucp%2Fjsp%2FIntranet.jsp"
        self.browser = None
        self.page: Page = None
        self.playwright = None
        self.context = None

    def iniciar(self):
        self.playwright = sync_playwright().start()
        # Headless=False para debug, cámbialo a True para producción
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def login(self, username, password):
        try:
            print("Iniciando sesión...")
            self.page.goto(self.url_login_target)
            self.page.locator("#username").fill(username)
            self.page.locator("#password").fill(password)
            
            # El truco del código funcional: presiona Enter en un rol de link vacío
            self.page.get_by_role("link").filter(has_text=re.compile(r"^$")).press("Enter")
            
            # Esperar a que la sesión se asiente
            self.page.wait_for_load_state("networkidle")
            print("✓ Login exitoso.")
            
            # Navegación intermedia obligatoria para "engañar" al sistema
            self.page.goto("https://ares.pucp.edu.pe/pucp/jsp/Intranet.jsp?url=%2Fpucp%2Fidiomas%2Fidwpanal%2FidwpanalPucpQuestionaccion%3DVerPanel")
            
        except Exception as e:
            print(f"X Error en login: {e}")

    def clasificador_alumnos(self, lista_alumnos):
        url_clasificacion = "https://ares.pucp.edu.pe/pucp/jsp/Intranet.jsp?url=%2Fpucp%2Fidiomas%2Fidwclasf%2FidwclasfPucpQuestionaccion%3DMostrarClasificacion"
        self.page.goto(url_clasificacion)

        for alu in lista_alumnos:
            try:
                print(f"Registrando: {alu.codigo} - {alu.curso}")
                
                # Definición del frame tal cual el código exitoso
                frame_mid = self.page.locator('iframe[name="frame_mid"]').content_frame

                # 1. Buscar Alumno
                frame_mid.locator("#codAlumno").fill(alu.codigo)
                frame_mid.locator("#codAlumno").press("Tab")
                time.sleep(2) # Tiempo vital para que Ares cargue los datos del alumno

                # 2. Habilitar Edición (Selector de texto exacto del código exitoso)
                frame_mid.locator("div").filter(has_text="Grabar Buscar Editar Regresar").locator("button[name=\"btnEditar\"]").click()

                # 3. Obtener código de curso mediante evaluación (imprescindible en Ares)
                print("Obteniendo opciones de cursos...")
                options = frame_mid.locator("#cmbCurso").evaluate(
                    "sel => Array.from(sel.options).map(o => ({ value: o.value, text: o.text.trim() }))"
                )
                
                codigo_curso = None
                for opt in options:
                    if alu.curso in opt["text"]:
                        codigo_curso = str(opt["value"])
                        print(f"✓ Curso encontrado: {opt['text']} (ID: {codigo_curso})")
                        break
                
                if not codigo_curso:
                    raise Exception(f"No se encontró el curso {alu.curso} en el combo")

                # 4. Llenado de datos
                frame_mid.locator("#cmbCurso").select_option(codigo_curso)
                frame_mid.locator("#cmbLocal").select_option("5")
                frame_mid.locator("textarea[name='observaciones']").fill(alu.observacion)

                # 5. Aceptar el diálogo de confirmación
                self.page.once("dialog", lambda dialog: dialog.accept())

                # 6. Grabar
                print("Guardando registro...")
                frame_mid.get_by_role("cell", name="Grabar Buscar Editar Regresar").locator("button[name=\"btnGrabar\"]").click()
                time.sleep(2)
                print(f"✓ Registro completado para {alu.codigo}")

            except Exception as e:
                print(f"X Error con alumno {alu.codigo}: {e}")
                # Reset de navegación en caso de error
                self.page.goto(url_clasificacion)

    def cerrar(self):
        if self.browser: self.browser.close()
        if self.playwright: self.playwright.stop()

def main():
    USERNAME_TEST = "W0026391"
    PASS_TEST = "TyS.Idiomas_26_01"

    # Instancia el robot
    robot = RobotPandora()
    
    try:
        robot.iniciar()
        robot.login(USERNAME_TEST, PASS_TEST)
        robot.clasificador_alumnos([
            Alumno("II169157", "Inglés Básico 2", "Observación de prueba para alumno 1 II169157"),
            Alumno("II169157", "Inglés Básico 2", "Observación de prueba para alumno 2 II169157")
        ])
        time.sleep(3) 
    finally:
        robot.cerrar()

# CORRECCIÓN: Doble guion bajo en __name__ y "__main__"
if __name__ == "__main__":
    main()